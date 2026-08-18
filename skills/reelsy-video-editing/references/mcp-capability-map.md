# Reelsy Editing MCP Capability Map

## Read and discovery

| Goal | Tool |
| --- | --- |
| Read owner-scoped Project facts | `read_reelsy_project_snapshot` |
| Read current Timeline and revision | `read_reelsy_timeline` |
| List immutable revisions | `list_reelsy_timeline_revisions` |
| Get the visible Hosted OpenCut handoff | `get_reelsy_editor_url` |
| Create the first editable Timeline after confirmed combination | `submit_reelsy_composition` |
| Discover caption presets and fonts | `list_reelsy_caption_styles` |
| Discover ordinary text styles | `list_reelsy_text_styles` |
| Discover stickers, overlays, visualizers, transitions, and filters | `list_reelsy_editor_visual_catalog` |
| Discover Project music | `list_reelsy_music` |
| Discover licensed library music | `list_reelsy_music_library` |
| Generate an owner-scoped vocal song or source-audio rewrite after lyrics, rights, and 12-credit confirmation | `submit_reelsy_music_generation`, then `get_reelsy_job_status` |
| Generate a legacy owner-scoped instrumental soundtrack after explicit 12-credit confirmation | `submit_reelsy_music_generation`, then `get_reelsy_job_status` |
| Transcribe a ready Project video or audio Artifact after explicit 1-credit confirmation | `submit_reelsy_transcription` |
| Generate a voiceover from approved text and a managed voice preset after explicit 3-credit confirmation | `submit_reelsy_voice_generation` |
| Attach a ready licensed, uploaded, or generated soundtrack | `attach_reelsy_soundtrack` |
| Change Canvas ratio and center video elements | `reframe_reelsy_timeline` |
| Insert 1–50 timed captions or lyric cues | `insert_reelsy_captions` |
| Inspect deterministic frame structure | `render_reelsy_timeline_frames` |
| Import a local media or font file | `create_reelsy_media_import`, then `inspect_reelsy_asset` |
| Produce a trusted transcript for timed captions | `submit_reelsy_transcription`, then `read_reelsy_project_snapshot` |

## Strongly typed common edits

Prefer these tools over generic command construction:

```json
{
  "projectId": "project-from-read",
  "timelineArtifactId": "timeline-from-read",
  "expectedRevision": 1,
  "canvas": { "width": 1080, "height": 1920 },
  "layout": "cover_center",
  "idempotencyKey": "vertical-cover-v1"
}
```

Pass that shape to `reframe_reelsy_timeline`. Use `contain_center` only when letterboxing is acceptable.

For full replacement with a ready vocal song or `voiceover`, pass its Artifact to `attach_reelsy_soundtrack` with `mode="generated"`, `volume=1`, and `muteNativeAudio=true`. This mutes every video track because mixed source audio cannot be separated by the Timeline tool. Keep `muteNativeAudio=false` when the source audio must remain.

For timed lyrics, query `list_reelsy_caption_styles`, then pass 1–50 cues to `insert_reelsy_captions`:

```json
{
  "projectId": "project-from-read",
  "timelineArtifactId": "latest-timeline-from-read",
  "expectedRevision": 3,
  "captionStyleId": "catalog-style-id",
  "cues": [
    {
      "text": "Let the stars map the night",
      "startTime": 2.8,
      "duration": 2.98,
      "words": [
        { "text": "Let", "startTime": 0, "duration": 0.24 },
        { "text": "the stars", "startTime": 0.24, "duration": 0.48 },
        { "text": "map", "startTime": 0.72, "duration": 0.46 },
        { "text": "the night", "startTime": 1.18, "duration": 1.8 }
      ]
    }
  ],
  "idempotencyKey": "lyrics-batch-1-v1"
}
```

Word times are relative to the cue start, ordered, non-overlapping, and bounded by cue duration. The service creates stable caption element IDs. More than 50 cues require multiple revisions; re-read the latest Timeline before each next batch. Without trusted `words[]`, the renderer intentionally falls back to static line-timed captions and the Agent must not claim karaoke behavior.

To enrich existing caption elements without recreating the Timeline, use up to 50 `update_element` commands in one transaction and set each element's cue-relative `words`. Pass `words: null` to explicitly remove stale word timing. Re-read the saved revision before visual verification.

## End-to-end assembly and verification

- After an explicit end-to-end request or “continue”, use one continuous authorization envelope for in-scope reversible edits. Keep separate confirmation only for paid generation, rights, publication, destructive actions, unrequested export, or a materially new creative choice.
- Execute **Structure → Audio → Captions → Structural Verification → Visual Verification**. Timeline is the default deliverable; export is a separate intent.
- Structural Verification must re-read the saved revision and confirm Canvas, tracks, native mute, soundtrack, caption count/style/timing, and word timing. Visual Verification must inspect the visible OpenCut Canvas at representative active-word times.

## Deterministic local import adapter

After `create_reelsy_media_import`, pass the returned `upload` object over stdin to:

```bash
node scripts/upload-media.mjs --file /absolute/path/to/media --expected-bytes 123456
```

The adapter accepts only a non-expired HTTPS PUT descriptor, verifies the exact local size and upload limit, streams the file once, and never prints the presigned URL. Then finalize with `inspect_reelsy_asset`. Do not replace this with ad hoc shell upload code or the browser file picker.

## Persistent Timeline transaction commands

Use these command types inside `apply_reelsy_timeline_transaction`:

- `insert_asset`, `move_elements`, `trim_element`, `split_element`, `reorder_track_elements`, `duplicate_elements`, and `delete_elements`.
- `insert_text`, `insert_caption`, `update_element`, `update_text_style`, and `update_transform`.
- `insert_sticker`, `insert_effect`, `update_effect`, `set_transition`, and `set_filter`.
- `update_track` for name, mute, volume, visibility, lock state, and an audio track role of `voice`, `bgm`, `sfx`, or `ambience`.
- `set_clip_effects` for the catalog-backed treatment stack on a video, text, or sticker element.
- `set_keyframes` for numeric transform, opacity, volume, and text-background animation channels.
- `set_bookmarks` and `update_project_settings` for Timeline markers, Project name, FPS, Canvas size, and Canvas background.
- `set_soundtrack` for an already registered licensed soundtrack or `native_only`.

The public schema is a `type`-discriminated union. Common command shapes are:

```json
{ "type": "update_project_settings", "canvas": { "width": 1080, "height": 1920 } }
{ "type": "update_track", "trackId": "track-from-read", "muted": true, "volume": 0 }
{ "type": "update_transform", "trackId": "track-from-read", "elementId": "element-from-read", "scale": 2.3703703704, "x": 0, "y": 0 }
{ "type": "insert_asset", "assetId": "trusted-timeline-asset-id", "elementId": "new-element-id", "startTime": 0, "duration": 5 }
```

`insert_asset` accepts only an Asset already trusted by the Timeline. Use `attach_reelsy_soundtrack` for an owner-scoped `background_music` or `generated_song` Artifact that is not yet a Timeline Asset. A transaction accepts 1–50 commands. Never send an empty command array or an empty `replace_timeline` to discover the schema.

Use `copy_reelsy_timeline_selection` followed by `paste_reelsy_timeline_selection` when explicit clipboard semantics are useful. The paste operation creates an immutable Timeline revision and survives refresh.

`set_keyframes` replaces the selected element's complete numeric keyframe stack. Keyframe times are relative to the element start and must stay within its duration. Supported properties are `transform.position.x`, `transform.position.y`, `transform.scale`, `transform.rotate`, `opacity`, `volume`, `background.paddingX`, `background.paddingY`, `background.offsetX`, `background.offsetY`, and `background.cornerRadius`. Trimming crops the stack; splitting preserves the boundary value and rebases the right element to time zero.

Insert commands accept an optional `trackId`. Omit it to atomically reuse a non-overlapping compatible track or create one. This is the preferred Agent path for text, captions, stickers, effects, and newly imported media.

## Temporary Hosted OpenCut controls

Use `control_reelsy_editor` for:

- opening Assets, Audio, Text, Elements, Captions, Transitions, Inspector, or Settings;
- opening the system import picker in a live target session;
- selecting elements and opening Inspector;
- play, pause, seek, frame-step, Timeline zoom, Canvas viewport, and focus;
- undo, redo, split, delete, copy, paste, duplicate, snapping, ripple editing, mute, visibility, and bookmarks through the allowlisted action names.

These controls do not replace a Timeline revision. Read the Editor command acknowledgement when an action requires a live browser session.

Use `list_reelsy_editor_sessions` to choose a live owner-scoped browser session, `read_reelsy_editor_state` to inspect its semantic selection and playback state, and `read_reelsy_editor_command` to verify an applied, rejected, or expired command. Never infer persistent success from a UI acknowledgement; confirm the resulting Timeline revision separately.

## Trust boundaries

- Fonts must use a managed font ID or an owner-scoped `source_font` Artifact.
- Stickers, effects, transitions, and filters must use IDs and parameters returned by the visual catalog.
- Licensed and uploaded music must use a registered owner-scoped Artifact with valid rights metadata. A generated instrumental soundtrack uses `background_music`; a vocal or rewritten song uses `generated_song`. Never pass a Provider URL or task ID into a Timeline or local edit.
- Music generation costs 12 credits. Display the approved lyrics and settings when applicable, obtain explicit confirmation for that exact generation, and reuse the existing Job and Artifact during polling or later Codex processing.
- Reelsy generation does not analyze source music, write lyrics, build captions, or edit video. Those steps remain Codex responsibilities under `$reelsy-song-rewrite`.
- Local paths never enter Reelsy MCP. Upload a completed local file through the bundled deterministic media import adapter, then finalize the Source Artifact through the media import flow.
- `set_keyframes` currently accepts numeric channels only. Text and background color animation remains a UI-only capability until the public media contract supports typed color keyframes.
- Ready generated clips remain separate Canvas Artifacts unless the user requests or confirms editing or combination. Multiple clips alone are not permission to create a Timeline.
- Hosted OpenCut owns preview and browser export for edited projects. A downloaded export remains local; do not upload it, call `publish_reelsy_final`, or create a Canvas Final Artifact.
