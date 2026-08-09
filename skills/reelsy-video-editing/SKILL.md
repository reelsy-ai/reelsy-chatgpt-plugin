---
name: reelsy-video-editing
description: "Edit an existing Reelsy video project through the Hosted OpenCut Canvas and owner-scoped Codex MCP. Use for trimming, splitting, joining, ordering, captions, fonts, titles, stickers, overlays, audio visualizers, music, transitions, filters, transforms, Timeline revisions, and revised Finals without regenerating successful video clips."
---

# Reelsy Video Editing

## Boundaries

- Open the Reelsy Canvas in the Codex in-app browser before editing so the user can observe the work.
- Treat the latest Timeline Artifact as the persistent source of truth. UI commands are temporary projection controls, not saved edits.
- Never regenerate a successful video for a Timeline-only change.
- Use one `apply_reelsy_timeline_transaction` call for each coherent atomic edit and include the latest `expectedRevision` plus a stable `idempotencyKey`.
- Query managed catalogs before using font, text style, sticker, effect, transition, filter, or music IDs. Never invent IDs or remote asset URLs.

## Workflow

1. Read the Project with `read_reelsy_project_snapshot`, then call `read_reelsy_timeline` and `get_reelsy_editor_url`. Open the returned URL in the Codex in-app browser.
2. Query only the catalogs required by the request:
   - `list_reelsy_caption_styles` for caption presets, managed fonts, and owner-scoped uploaded fonts.
   - `list_reelsy_text_styles` for titles, subtitles, lower thirds, offers, badges, quotes, and end cards.
   - `list_reelsy_editor_visual_catalog` for stickers, Atmosphere overlays, audio visualizers, transitions, and filters.
   - `list_reelsy_music` or `list_reelsy_music_library` for licensed audio.
   - `create_reelsy_media_import` and `inspect_reelsy_asset` when a local file must become a trusted Project Asset.
   - `submit_reelsy_analysis` and `get_reelsy_job_status` when speech-aligned captions require a trusted transcript from an existing video or audio Artifact.
3. Build a minimal command batch. Omit `trackId` on inserts when automatic compatible-track placement is preferred; provide it only after reading the Timeline and intentionally targeting that track.
   - For explicit clipboard semantics, call `copy_reelsy_timeline_selection` and then `paste_reelsy_timeline_selection`; do not rely on a browser-only clipboard action for a persistent edit.
4. Apply the transaction. On conflict, read the latest Timeline and rebase the intended change; never overwrite an unknown newer revision.
5. Read the new revision and use `control_reelsy_editor` to select the changed elements, focus the Timeline, seek the playhead, or open the relevant panel. Use `list_reelsy_editor_sessions`, `read_reelsy_editor_state`, and `read_reelsy_editor_command` when live UI state or acknowledgement matters.
6. Use `render_reelsy_timeline_frames` for deterministic structural checks. Use the visible Canvas for visual judgment.
7. If the user requests a rendered Final, first verify that the available Codex-local renderer supports every Timeline layer in the requested revision. The bundled Production script currently renders ordered clips and an optional soundtrack; do not claim that it baked captions, stickers, transitions, filters, overlays, or visualizers. Upload, inspect, and publish only a fully rendered result, and preserve earlier Finals and revisions.

## Persistent Editing Capabilities

- Basic editing: insert assets, move, trim, split, reorder, duplicate, delete, and persistent semantic copy/paste.
- Text and captions: reuse a trusted transcript when speech alignment is required; insert or rewrite text, choose managed or uploaded fonts, apply full caption styling, and position layers.
- Visual layers: insert and position stickers; insert or update Atmosphere overlays and audio visualizers; set transitions and filters.
- Audio: set element volume and pan, track mute/volume/role, attach licensed music, or restore native-only audio.
- Layout and Inspector: update transform, rotation, scale, position, opacity, visibility, mute state, blend mode, and catalog-backed clip effects.
- Motion and Project settings: replace numeric keyframe channels, set bookmarks, rename the Project, and update FPS, Canvas size, or Canvas background.

Read [the MCP capability map](references/mcp-capability-map.md) before building a complex transaction.

## Failure Rules

- Unknown catalog ID or invalid parameter: query the catalog again and correct the command; do not weaken validation.
- Revision conflict: re-read, preserve the newer revision, and reapply only the user's intended delta.
- Browser session unavailable: continue persistent Timeline work and reopen the Canvas; never treat the missing UI session as lost Project data.
- Local render failure: keep the Timeline revision, do not upload a partial file, and rerun only the local render.
- Unsupported local render layer: keep the saved Timeline and visible Canvas result, report the exact unsupported layers, and do not publish a Final that silently drops them.
