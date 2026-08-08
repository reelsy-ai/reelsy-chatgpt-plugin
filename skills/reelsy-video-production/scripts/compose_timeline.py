#!/usr/bin/env python3
"""Deterministically compose two Reelsy Timeline clips into a local MP4."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


MAX_DURATION_MS = 3_600_000
PROCESS_TIMEOUT_SECONDS = 15 * 60


class ComposeError(Exception):
    """Expose stable error codes to the caller."""


def fail(code: str) -> None:
    raise ComposeError(code)


def require_record(value: Any, code: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(code)
    return value


def require_number(value: Any, code: str, minimum: float, maximum: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        fail(code)
    number = float(value)
    if number < minimum or number > maximum:
        fail(code)
    return number


def require_path(value: Any, code: str, *, must_exist: bool) -> Path:
    if not isinstance(value, str) or not value.strip():
        fail(code)
    path = Path(value).expanduser()
    if not path.is_absolute():
        fail(code)
    if must_exist and (not path.is_file() or path.stat().st_size <= 0):
        fail(code)
    return path


def executable(name: str, environment_name: str) -> str:
    configured = os.environ.get(environment_name, "").strip()
    candidate = configured or shutil.which(name)
    if not candidate:
        fail(f"{name}_not_found")
    return candidate


def probe(ffprobe: str, path: Path) -> dict[str, Any]:
    result = subprocess.run(
        [
            ffprobe,
            "-v", "error",
            "-show_entries", "format=duration:stream=codec_type,codec_name,width,height,avg_frame_rate",
            "-of", "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    value = json.loads(result.stdout)
    return require_record(value, "ffprobe_output_invalid")


def has_audio(metadata: dict[str, Any]) -> bool:
    streams = metadata.get("streams")
    return isinstance(streams, list) and any(
        isinstance(stream, dict) and stream.get("codec_type") == "audio"
        for stream in streams
    )


def parse_request(path: Path) -> dict[str, Any]:
    request = require_record(json.loads(path.read_text(encoding="utf-8")), "request_invalid")
    if request.get("format") != "reelsy_local_composition_request_v1":
        fail("request_format_invalid")
    canvas = require_record(request.get("canvas"), "canvas_invalid")
    width = int(require_number(canvas.get("width"), "canvas_width_invalid", 144, 3840))
    height = int(require_number(canvas.get("height"), "canvas_height_invalid", 144, 3840))
    fps = int(require_number(request.get("fps"), "fps_invalid", 1, 60))
    clips_value = request.get("clips")
    if not isinstance(clips_value, list) or len(clips_value) != 2:
        fail("clips_count_invalid")
    clips: list[dict[str, Any]] = []
    total_duration_ms = 0
    for value in clips_value:
        clip = require_record(value, "clip_invalid")
        duration_ms = int(require_number(clip.get("durationMs"), "clip_duration_invalid", 100, MAX_DURATION_MS))
        trim_start_ms = int(require_number(clip.get("trimStartMs", 0), "clip_trim_invalid", 0, MAX_DURATION_MS))
        clips.append({
            "path": require_path(clip.get("path"), "clip_path_invalid", must_exist=True),
            "durationMs": duration_ms,
            "trimStartMs": trim_start_ms,
        })
        total_duration_ms += duration_ms
    if total_duration_ms > MAX_DURATION_MS:
        fail("timeline_duration_invalid")
    soundtrack = None
    if request.get("soundtrack") is not None:
        value = require_record(request.get("soundtrack"), "soundtrack_invalid")
        soundtrack = {
            "path": require_path(value.get("path"), "soundtrack_path_invalid", must_exist=True),
            "volume": require_number(value.get("volume", 0.25), "soundtrack_volume_invalid", 0, 1),
        }
    output_path = require_path(request.get("outputPath"), "output_path_invalid", must_exist=False)
    if output_path in [clip["path"] for clip in clips] or (soundtrack and output_path == soundtrack["path"]):
        fail("output_overwrites_input")
    return {
        "outputPath": output_path,
        "width": width,
        "height": height,
        "fps": fps,
        "clips": clips,
        "soundtrack": soundtrack,
        "durationMs": total_duration_ms,
    }


def render(ffmpeg: str, ffprobe: str, request: dict[str, Any]) -> None:
    clip_probes = [probe(ffprobe, clip["path"]) for clip in request["clips"]]
    soundtrack = request["soundtrack"]
    if soundtrack and not has_audio(probe(ffprobe, soundtrack["path"])):
        fail("soundtrack_audio_missing")

    args = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y"]
    for clip in request["clips"]:
        args.extend(["-i", str(clip["path"])])
    if soundtrack:
        args.extend(["-stream_loop", "-1", "-i", str(soundtrack["path"])])

    filters: list[str] = []
    concat_inputs: list[str] = []
    for index, clip in enumerate(request["clips"]):
        duration = clip["durationMs"] / 1000
        trim_start = clip["trimStartMs"] / 1000
        filters.append(
            f"[{index}:v]trim=start={trim_start}:duration={duration},setpts=PTS-STARTPTS,"
            f"scale={request['width']}:{request['height']}:force_original_aspect_ratio=decrease,"
            f"pad={request['width']}:{request['height']}:(ow-iw)/2:(oh-ih)/2,"
            f"fps={request['fps']},setsar=1,format=yuv420p[v{index}]"
        )
        if has_audio(clip_probes[index]):
            filters.append(
                f"[{index}:a]atrim=start={trim_start}:duration={duration},asetpts=PTS-STARTPTS,"
                f"aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a{index}]"
            )
        else:
            filters.append(
                f"anullsrc=channel_layout=stereo:sample_rate=48000,atrim=duration={duration},"
                f"asetpts=PTS-STARTPTS[a{index}]"
            )
        concat_inputs.append(f"[v{index}][a{index}]")

    filters.append(f"{''.join(concat_inputs)}concat=n=2:v=1:a=1[vout][native]")
    audio_map = "[native]"
    if soundtrack:
        filters.append(
            f"[2:a]atrim=duration={request['durationMs'] / 1000},asetpts=PTS-STARTPTS,"
            f"aresample=48000,volume={soundtrack['volume']}[music]"
        )
        filters.append("[native][music]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[aout]")
        audio_map = "[aout]"

    output_path: Path = request["outputPath"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    args.extend([
        "-filter_complex", ";".join(filters),
        "-map", "[vout]", "-map", audio_map,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
        "-t", str(request["durationMs"] / 1000),
        str(output_path),
    ])
    subprocess.run(args, check=True, capture_output=True, timeout=PROCESS_TIMEOUT_SECONDS)


def frame_rate(value: Any) -> float:
    if not isinstance(value, str) or not value:
        fail("output_fps_invalid")
    numerator, _, denominator = value.partition("/")
    rate = float(numerator) / float(denominator or "1")
    if rate <= 0:
        fail("output_fps_invalid")
    return round(rate, 3)


def result_manifest(ffprobe: str, request: dict[str, Any]) -> dict[str, Any]:
    output_path: Path = request["outputPath"]
    if not output_path.is_file() or output_path.stat().st_size <= 0:
        fail("output_missing")
    metadata = probe(ffprobe, output_path)
    streams = metadata.get("streams")
    if not isinstance(streams, list):
        fail("output_streams_invalid")
    video = next((stream for stream in streams if isinstance(stream, dict) and stream.get("codec_type") == "video"), None)
    if not isinstance(video, dict):
        fail("output_video_missing")
    format_value = require_record(metadata.get("format"), "output_format_invalid")
    duration_ms = round(float(format_value.get("duration")) * 1000)
    digest = hashlib.sha256()
    with output_path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return {
        "format": "reelsy_local_composition_result_v1",
        "outputPath": str(output_path),
        "contentType": "video/mp4",
        "byteSize": output_path.stat().st_size,
        "sha256": digest.hexdigest(),
        "durationMs": duration_ms,
        "width": int(video.get("width")),
        "height": int(video.get("height")),
        "fps": frame_rate(video.get("avg_frame_rate")),
        "codec": str(video.get("codec_name") or "h264"),
        "hasAudio": has_audio(metadata),
        "toolVersion": "reelsy-compose-timeline/1.0.0",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True)
    args = parser.parse_args()
    try:
        request_path = require_path(args.request, "request_path_invalid", must_exist=True)
        request = parse_request(request_path)
        ffmpeg = executable("ffmpeg", "FFMPEG_PATH")
        ffprobe = executable("ffprobe", "FFPROBE_PATH")
        render(ffmpeg, ffprobe, request)
        print(json.dumps(result_manifest(ffprobe, request), ensure_ascii=False, separators=(",", ":")))
        return 0
    except (ComposeError, json.JSONDecodeError, ValueError, subprocess.SubprocessError) as error:
        code = str(error) if isinstance(error, ComposeError) else "local_composition_failed"
        print(f"reelsy_compose_error:{code}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
