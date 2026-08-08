---
name: reelsy-video-production
description: "Complete a two-clip AI video production loop through Reelsy MCP. Use when a user asks Codex to generate, recreate, or finish a Reelsy video: validate the Production Plan, submit two paid video clips after confirmation, choose an optional Soundtrack, create the Timeline, compose locally with FFmpeg, upload the result, and publish a playable Final."
---

# Reelsy Video Production

## Boundaries

- Treat a playable Final as the default completion condition. Do not turn Canvas, internal schemas, or review nodes into production gates.
- Show the estimated credit cost and obtain explicit confirmation before paid generation. Reuse the original business `idempotencyKey` when retrying.
- Run FFmpeg only on the Codex host. Reelsy owns Provider access, Project facts, R2 import, Timeline, Final, and Canvas projection; it does not perform composition compute.
- Default to `native_only` and preserve clip audio. Mix music only when the Timeline accepts a licensed library track, a user-uploaded track with confirmed rights, or generated music whose credit cost was explicitly approved.
- Never use a fake Provider, fake URL, or manually fabricated success state.

## Workflow

1. Read the Project snapshot. Require one ready `production_plan` with exactly two valid clip targets.
2. If either target is missing, show the generation cost and obtain confirmation. Then call `submit_reelsy_generation` separately for both targets, using stable and distinct `idempotencyKey` values.
3. Query both Jobs with `get_reelsy_job_status`. If one target fails, retry only that target and preserve the successful clip.
4. After both `generated_clip` artifacts are ready, call `submit_reelsy_composition`. Use `native_only` unless the user explicitly requested a valid Soundtrack.
5. Read clip URLs, order, trims, canvas, FPS, and the optional Soundtrack from the returned `media_editor_project`. Download them into a local temporary directory.
6. Write a `reelsy_local_composition_request_v1` JSON file and run:

   ```bash
   python3 scripts/compose_timeline.py --request /absolute/path/request.json
   ```

7. Read the script's result manifest. Never infer SHA256, duration, dimensions, or FPS from free-form logs.
8. Upload the local Final with `create_reelsy_media_import`, then call `inspect_reelsy_asset`. Pass the manifest's `sha256/durationMs/width/height/fps/codec/hasAudio/toolVersion` fields unchanged as the probe.
9. Call `publish_reelsy_final` with the Timeline Artifact and the uploaded composed-video Artifact. Read the Project snapshot again and verify that it contains one ready `final_video` and its `assembled_into` relations.

## Local Composition Request

```json
{
  "format": "reelsy_local_composition_request_v1",
  "outputPath": "/absolute/path/final.mp4",
  "canvas": { "width": 480, "height": 854 },
  "fps": 30,
  "clips": [
    { "path": "/absolute/path/clip-1.mp4", "trimStartMs": 0, "durationMs": 8000 },
    { "path": "/absolute/path/clip-2.mp4", "trimStartMs": 0, "durationMs": 8000 }
  ],
  "soundtrack": null
}
```

For an accepted Soundtrack, use:

```json
{
  "path": "/absolute/path/music.mp3",
  "volume": 0.25
}
```

The script normalizes canvas size and FPS, emits H.264/AAC, and inserts silence when a generated clip has no audio stream. Therefore `native_only` does not fail merely because one clip is silent.

## Failure Rules

- Provider failure: preserve every successful target and report only the failed Job's public error.
- Soundtrack rejected by Timeline: fall back to `native_only` unless the user asks to fix licensing first.
- Local FFmpeg failure: do not upload and do not call `publish_reelsy_final`; correct the local inputs and rerun the script.
- Upload or publish failure: reuse the existing local Final and business idempotency key; do not regenerate clips.
- Final duration differs from Timeline by more than one second: treat it as a local composition error and do not publish.
