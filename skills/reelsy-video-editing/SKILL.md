---
name: reelsy-video-editing
description: "Edit a Reelsy video project through Hosted OpenCut and owner-scoped Codex MCP. Use when the user explicitly requests or confirms trimming, splitting, joining, ordering, captions, fonts, titles, stickers, overlays, audio visualizers, music, transitions, filters, transforms, or export preparation. Do not invoke only because Production returned multiple clips."
---

# Reelsy Video Editing

## Required Connector and Editor Gate

- Before any browser action, call `connector_status` and require the owner-scoped Reelsy Timeline and editor tools used by this workflow. If the tools are missing from the current task or OAuth is not authenticated, follow [the Connector onboarding reference](../reelsy-video-production/references/connector-onboarding.md); preserve the original request, run setup when possible, and create a fresh task after successful authorization when the current snapshot cannot refresh. Do not inspect private implementation routes or continue with a browser-only fallback.
- Let this Foundation Skill own Connector authorization, Project resolution, and Hosted OpenCut bootstrap for every Domain Skill that routes here.
- Call `get_reelsy_editor_url` only after resolving the Project and Timeline. Open only the exact returned URL for that Project. Never construct, rewrite, or replace it with a generic Reelsy Agent URL, and never switch between `localhost` and `reelsy.ai`.

## Boundaries

- Enter Hosted OpenCut only after the user explicitly requests editing or combination, or confirms an Editing handoff proposed by Production.
- Do not treat multiple ready clips alone as permission to create a Timeline or combine them.
- Open the Reelsy editor in the Codex in-app browser before editing so the user can observe the work.
- Treat the latest Timeline Artifact as the persistent source of truth. UI commands are temporary projection controls, not saved edits.
- Never regenerate a successful video for a Timeline-only change.
- Use one `apply_reelsy_timeline_transaction` call for each coherent atomic edit and include the latest `expectedRevision` plus a stable `idempotencyKey`.
- Query managed catalogs before using font, text style, sticker, effect, transition, filter, or licensed music IDs. Never invent IDs or remote asset URLs. Generated instrumentals use a ready owner-scoped `background_music` Artifact; generated vocal songs use `generated_song`.
- Route lyric-bearing song generation or source-melody rewriting to `$reelsy-song-rewrite`. This Editing Skill keeps only the legacy instrumental soundtrack path and must not ask Reelsy to analyze, rewrite, subtitle, or edit a song.
- Let Hosted OpenCut render and download the edited project. Do not upload that export, call `publish_reelsy_final`, or write a new Final Artifact back to the Canvas.

## New User Onboarding

- Accept natural-language editing requests such as “add captions and music” or “combine these clips”; never require the user to mention Skills, MCP tools, Project IDs, OAuth scopes, or editor URLs.
- When a new user has no target Project, let the Production Foundation establish the Project and visible Canvas first. If the user supplied existing media and clearly asked for editing, establish the Project and Timeline, then surface the exact Hosted OpenCut URL before making substantial edits.
- Describe the editing path in plain language: the user can review the visible Canvas, enter OpenCut when editing is requested, and adjust the Timeline, captions, fonts, music, stickers, effects, and export there. Ask only for decisions that materially affect the edit.
- If authorization is missing, preserve the original editing intent and request a plain-language Reelsy connection. Do not ask the user to repeat the request after authorization or send them to a generic Agent page.

## Workflow

1. Read the Project with `read_reelsy_project_snapshot` and determine whether a ready Timeline already exists. If the Project is not yet established, let the Production Foundation create or resolve it before continuing.
2. If no Timeline exists, require confirmed Editing intent, choose the ready video Artifacts in the requested order, and call `submit_reelsy_composition` once to create the initial editable Timeline. Default to `native_only` unless the user requested licensed, user-owned, or generated music.
3. Pass the Required Connector and Editor Gate. Call `read_reelsy_timeline` and `get_reelsy_editor_url`, then open the exact returned URL in the Codex in-app browser. Do not refresh a live editor unless the user explicitly requests a cold-load persistence check.
4. Query only the catalogs required by the request:
   - `list_reelsy_caption_styles` for caption presets, managed fonts, and owner-scoped uploaded fonts.
   - `list_reelsy_text_styles` for titles, subtitles, lower thirds, offers, badges, quotes, and end cards.
   - `list_reelsy_editor_visual_catalog` for stickers, Atmosphere overlays, audio visualizers, transitions, and filters.
   - `list_reelsy_music` or `list_reelsy_music_library` for licensed audio.
   - `submit_reelsy_music_generation` with `mode="instrumental"` only for a legacy instrumental soundtrack. Show the fixed 12-credit cost and wait for explicit confirmation for this generation before calling it. Reuse one stable `idempotencyKey`, poll only with `get_reelsy_job_status`, and use the ready `background_music` Artifact. Use `$reelsy-song-rewrite` instead when lyrics or a source melody are involved.
   - `create_reelsy_media_import` and `inspect_reelsy_asset` when a local file must become a trusted Project Asset.
   - `submit_reelsy_analysis` and `get_reelsy_job_status` when speech-aligned captions require a trusted transcript from an existing video or audio Artifact.
5. Prefer the strongly typed editing tools for common workflows:
   - Use `reframe_reelsy_timeline` for Canvas ratio changes and centered cover/contain reframing.
   - Use `attach_reelsy_soundtrack` for licensed/uploaded music, `background_music`, or `generated_song`. For a vocal-song replacement, use `mode="generated"`, `volume=1`, and `muteNativeAudio=true` only after the user approves fully muting mixed source audio.
   - Use `insert_reelsy_captions` for 1–50 pre-timed transcript or lyric cues after querying `list_reelsy_caption_styles`.
6. Use `apply_reelsy_timeline_transaction` only for edits not covered by a strongly typed tool. Read [the MCP capability map](references/mcp-capability-map.md) before constructing commands. A transaction accepts at most 50 commands; split independent phases across revisions and re-read after each phase. Never use an empty `replace_timeline` as schema discovery or probing.
7. Apply the edit. On conflict, read the latest Timeline and rebase the intended change; never overwrite an unknown newer revision. Omit `trackId` on inserts when automatic compatible-track placement is preferred; provide it only after reading the Timeline and intentionally targeting that track. Use `copy_reelsy_timeline_selection` followed by `paste_reelsy_timeline_selection` for persistent clipboard semantics.
8. Read the new revision and use `control_reelsy_editor` to select the changed elements, focus the Timeline, seek the playhead, or open the relevant panel. Use `list_reelsy_editor_sessions`, `read_reelsy_editor_state`, and `read_reelsy_editor_command` when live UI state or acknowledgement matters.
9. Use `render_reelsy_timeline_frames` for deterministic structural checks and the visible OpenCut Canvas for visual judgment.
10. When export is requested, use the existing OpenCut Export UI in the in-app browser. The browser download is the result; do not upload it or project it back to the Reelsy Canvas.

## Completion Contract

- Complete an Editing task when the intended Timeline Revision is saved, the changed result is visible in Hosted OpenCut, and the existing Export control is available.
- Do not require an exported file when the user only asked for edits.
- Do not create a Reelsy Final Artifact from an OpenCut browser export.

## Persistent Editing Capabilities

- Basic editing: insert assets, move, trim, split, reorder, duplicate, delete, and persistent semantic copy/paste.
- Text and captions: reuse a trusted transcript when speech alignment is required; insert or rewrite text, choose managed or uploaded fonts, apply full caption styling, and position layers.
- Visual layers: insert and position stickers; insert or update Atmosphere overlays and audio visualizers; set transitions and filters.
- Audio: set element volume and pan, track mute/volume/role, attach licensed, uploaded, or generated instrumental music, or restore native-only audio.
- Layout and Inspector: update transform, rotation, scale, position, opacity, visibility, mute state, blend mode, and catalog-backed clip effects.
- Motion and Project settings: replace numeric keyframe channels, set bookmarks, rename the Project, and update FPS, Canvas size, or Canvas background.

Read [the MCP capability map](references/mcp-capability-map.md) before building a complex transaction.

## Failure Rules

- Connector tools unavailable or OAuth unauthenticated: follow [the Connector onboarding reference](../reelsy-video-production/references/connector-onboarding.md) before any browser action. Preserve the request and do not replace MCP with source inspection, private HTTP routes, a generic Agent workspace, or a technical prompt that the user must repeat.
- Unknown catalog ID or invalid parameter: query the catalog again and correct the command; do not weaken validation.
- Revision conflict: re-read, preserve the newer revision, and reapply only the user's intended delta.
- Browser session unavailable: preserve persistent Timeline work and reopen OpenCut; never treat the missing UI session as lost Project data.
- OpenCut export failure: preserve the saved Timeline Revision and retry only the browser export. Do not regenerate media or create a replacement Final pipeline.
- Generated music succeeded but Timeline attachment failed: preserve the ready `background_music` or `generated_song` Artifact, re-read the latest Timeline revision, and retry only `attach_reelsy_soundtrack`. Never submit another paid music Job for an editing conflict.
- Source video contains narration and old music in one mixed audio track: explain that soundtrack attachment cannot remove only the old music. Do not claim source separation; either mute the mixed native audio with the user's consent or keep it until a separate separation capability exists.
