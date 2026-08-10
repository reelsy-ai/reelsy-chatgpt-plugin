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
| Inspect deterministic frame structure | `render_reelsy_timeline_frames` |
| Import a local media or font file | `create_reelsy_media_import`, then `inspect_reelsy_asset` |
| Produce a trusted transcript for timed captions | `submit_reelsy_analysis`, then `get_reelsy_job_status` and `read_reelsy_project_snapshot` |

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
- Music must use a registered owner-scoped Artifact with valid rights metadata.
- Local paths never enter Reelsy MCP. Upload a completed local file through the media import flow.
- `set_keyframes` currently accepts numeric channels only. Text and background color animation remains a UI-only capability until the public media contract supports typed color keyframes.
- Ready generated clips remain separate Canvas Artifacts unless the user requests or confirms editing or combination. Multiple clips alone are not permission to create a Timeline.
- Hosted OpenCut owns preview and browser export for edited projects. A downloaded export remains local; do not upload it, call `publish_reelsy_final`, or create a Canvas Final Artifact.
