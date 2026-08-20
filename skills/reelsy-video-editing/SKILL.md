---
name: reelsy-video-editing
description: "Edit a Reelsy video project through Hosted OpenCut and owner-scoped Codex MCP. Use when the user explicitly requests or confirms trimming, splitting, joining, ordering, captions, fonts, titles, stickers, overlays, audio visualizers, music, transitions, filters, transforms, or export preparation. Do not invoke only because Production returned multiple clips."
---

# Reelsy Video Editing

## Required Connector and Editor Gate

- Before any browser action, call `connector_status` and require the owner-scoped Reelsy Timeline and editor tools used by this workflow. If the tools are missing from the current task or OAuth is not authenticated, follow [the Connector onboarding reference](../reelsy-video-production/references/connector-onboarding.md); preserve the original request, run setup when possible, and create a fresh task after successful authorization when the current snapshot cannot refresh. Do not inspect private implementation routes or continue with a browser-only fallback.
- Let this Foundation Skill own Connector authorization, Project resolution, and Hosted OpenCut bootstrap for every Domain Skill that routes here.
- Call `get_reelsy_editor_url` only after resolving the Project and Timeline. Open only the exact returned URL for that Project. Never construct, rewrite, or replace it with a generic Reelsy Agent URL, and never switch between `localhost` and `reelsy.ai`.

## Authentication-first Browser Contract

- The in-app browser is only for the OAuth page launched by the bundled Connector login and the exact owner-scoped editor URL returned by MCP. It is not a fallback API for discovering Reelsy pages or checking whether a user is logged in.
- If MCP tools are missing or `connector_status` is not ready, stop before opening a Reelsy dashboard or generic Agent workspace and follow the Connector onboarding reference. Do not inspect DOM links, guess an editor URL, or ask the user to repeat the editing brief.

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

## Continuous Authorization and Execution Order

- Treat an explicit end-to-end editing request, or “continue” after the edit has been aligned, as continuous authorization for reversible mechanical steps inside that request. Do not repeatedly ask before reframing, muting source audio, attaching an already approved song, inserting approved captions, saving revisions, or running verification when those actions were already requested.
- Continuous authorization never covers a new paid generation, missing source-rights confirmation, publication, deletion, an export that was not requested, or a materially different creative direction. Keep the existing explicit confirmation gates for those actions.
- Execute one requested assembly in this fixed order: **Structure → Audio → Captions → Structural Verification → Visual Verification**. Re-read the latest revision between dependent phases and rebase on conflicts; do not expose each mechanical phase as a separate user decision.
- A Timeline revision is the default Editing deliverable. Export is a separate intent and must not be inferred from “finish”, “continue”, or “end-to-end” unless the user explicitly included export.

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
   - `create_reelsy_media_import` and `inspect_reelsy_asset` when a local file must become a trusted Project Asset. Use the bundled deterministic upload adapter described below; do not improvise a `curl`, Python, or browser-picker upload path.
   - `submit_reelsy_transcription` when speech-aligned captions require a trusted transcript from an existing video or audio Artifact. Show the fixed 1-credit cost and wait for explicit confirmation before calling it with `expectedCredits=1`; use the returned `transcript` Artifact and its `words[]`/`segments[]`.
   - `list_reelsy_tts_voices` before choosing narration. Treat its returned official Gemini voice list and legacy aliases as the only valid choices; do not rely on a stale hard-coded list.
   - `submit_reelsy_voice_generation` when the user requests narration or a voice replacement. Use a voice returned by `list_reelsy_tts_voices`, show the exact approved text, selected voice, and fixed 3-credit cost before calling it with `expectedCredits=3`; use the returned `voiceover` Artifact and never expose Provider errors or raw storage details.
5. Apply the requested structure first, then audio, then captions. Prefer the strongly typed editing tools for common workflows:
   - Use `reframe_reelsy_timeline` for Canvas ratio changes and centered cover/contain reframing.
   - Use `attach_reelsy_soundtrack` for licensed/uploaded music, `background_music`, `generated_song`, or a generated `voiceover`. For a voice replacement, use `mode="generated"`, `volume=1`, and `muteNativeAudio=true` only when fully muting mixed source audio is part of the approved request; do not ask for the same mechanical approval twice.
   - Use `insert_reelsy_captions` for 1–50 pre-timed transcript or lyric cues after querying `list_reelsy_caption_styles`. Include cue-relative `words[]` whenever trusted word timing exists; without `words[]`, describe the result as line-timed captions, never as karaoke highlighting.
6. Use `apply_reelsy_timeline_transaction` only for edits not covered by a strongly typed tool. Read [the MCP capability map](references/mcp-capability-map.md) before constructing commands. A transaction accepts at most 50 commands; split independent phases across revisions and re-read after each phase. Never use an empty `replace_timeline` as schema discovery or probing.
7. Apply the edit. On conflict, read the latest Timeline and rebase the intended change; never overwrite an unknown newer revision. Omit `trackId` on inserts when automatic compatible-track placement is preferred; provide it only after reading the Timeline and intentionally targeting that track. Use `copy_reelsy_timeline_selection` followed by `paste_reelsy_timeline_selection` for persistent clipboard semantics.
8. Read the new revision and use `control_reelsy_editor` to select the changed elements, focus the Timeline, seek the playhead, or open the relevant panel. Use `list_reelsy_editor_sessions`, `read_reelsy_editor_state`, and `read_reelsy_editor_command` when live UI state or acknowledgement matters.
9. Complete Structural Verification by re-reading the persisted revision and using `render_reelsy_timeline_frames` to confirm Canvas, native mute state, soundtrack, caption count, cue timing, style, and `words[]` persistence.
10. Complete Visual Verification in the visible OpenCut Canvas at representative active-word times. Confirm framing, soundtrack presence, caption safe-area position, transparent background, inactive color, yellow current-word color, and real shadow. A structural frame description alone is not visual proof.
11. When export is requested, use the existing OpenCut Export UI in the in-app browser. The browser download is the result; do not upload it or project it back to the Reelsy Canvas.

## Deterministic Local Media Import

1. Probe the local file once, record its exact byte size, MIME type, duration/dimensions when applicable, and SHA-256, then call `create_reelsy_media_import` with the same file metadata and a stable idempotency key.
2. Run `scripts/upload-media.mjs --file <absolute-path> --expected-bytes <exact-byte-size>` and send only the returned `upload` object to the process over stdin. The adapter verifies HTTPS, expiry, upload limit, exact file size, headers, and streams one PUT without printing the presigned URL.
3. Call `inspect_reelsy_asset` with the original `completionToken` and the local probe. Reuse the ready Source Artifact; never pass a local path, presigned URL, or Provider storage identifier into Timeline tools.
4. If upload or finalization fails, retry only the failed import phase with a fresh credential when required. Do not regenerate media, create duplicate Timeline content, or ask the user to operate the system file picker.

## Completion Contract

- Complete an Editing task only when the intended Timeline Revision is saved, its persistent structure has been re-read, and the changed result is visibly verified in Hosted OpenCut. Report both the saved structure and the visible result as one outcome.
- Do not require an exported file when the user only asked for edits.
- Do not create a Reelsy Final Artifact from an OpenCut browser export.
- Do not claim karaoke, active-word color, shadow, or placement from preset metadata alone. Verify the rendered Canvas at a time where a word is active.

## Persistent Editing Capabilities

### Official Gemini TTS voices

`submit_reelsy_voice_generation` accepts the 30 official `gemini-3.1-flash-tts-preview` voices directly: `Zephyr`, `Puck`, `Charon`, `Kore`, `Fenrir`, `Leda`, `Orus`, `Aoede`, `Callirrhoe`, `Autonoe`, `Enceladus`, `Iapetus`, `Umbriel`, `Algieba`, `Despina`, `Erinome`, `Algenib`, `Rasalgethi`, `Laomedeia`, `Achernar`, `Alnilam`, `Schedar`, `Gacrux`, `Pulcherrima`, `Achird`, `Zubenelgenubi`, `Vindemiatrix`, `Sadachbia`, `Sadaltager`, and `Sulafat`. Legacy managed presets remain accepted.

- Basic editing: insert assets, move, trim, split, reorder, duplicate, delete, and persistent semantic copy/paste.
- Text and captions: reuse a trusted transcript when speech alignment is required; insert or rewrite text, choose managed or uploaded fonts, apply full caption styling, and position layers.
- Visual layers: insert and position stickers; insert or update Atmosphere overlays and audio visualizers; set transitions and filters.
- Audio: set element volume and pan, track mute/volume/role, attach licensed, uploaded, generated instrumental music, generated vocal songs, or generated voiceover, or restore native-only audio.
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
