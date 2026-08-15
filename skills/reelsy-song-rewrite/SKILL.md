---
name: reelsy-song-rewrite
description: "Rewrite a lyric-bearing song from a user-provided video or audio reference, or generate a new vocal song, while keeping Reelsy limited to paid music generation. Use when the user asks to rewrite lyrics, remake a song, preserve a source melody, create a vocal cover, replace a video's song, or synchronize rewritten lyrics as captions. Codex performs local extraction, analysis, lyric writing, alignment, and video editing."
---

# Reelsy Song Rewrite

## Responsibility Boundary

- Let Codex extract and inspect source audio, analyze song structure, write or revise lyrics, align captions, and edit the final video.
- Use Reelsy only for owner-scoped music generation, credit settlement, Provider recovery, result persistence, and available timed-lyric metadata.
- Do not call Reelsy video generation, Production Plan, media analysis, caption generation, Timeline, or OpenCut tools merely to rewrite a song.
- Let `$reelsy-video-production` own Connector authorization and Project bootstrap when they are missing, but do not enter its paid video-generation path.

## Workflow

1. Inspect the supplied video or audio locally. Extract a clean audio reference with local tools when the source is a video. If dialogue, effects, and music are mixed together, explain the limitation and choose full-audio replacement or a locally available separation path with the user; never claim that Reelsy separates stems.
2. Analyze the source locally for language, sections, pacing, mood, vocal character, and approximate melody structure. Do not submit this analysis to Reelsy.
3. Draft the rewritten lyrics in the conversation. Preserve the requested section and pacing constraints without silently copying protected lyrics. Show the complete proposed lyrics, title, style, vocal gender when relevant, and melody-preservation level.
4. Before a source-based rewrite, obtain explicit confirmation that the user has the right to use the source audio and rewrite its lyrics. Before every paid generation, show the fixed 12-credit cost and obtain explicit confirmation for the exact approved lyrics and settings. OAuth or earlier setup approval is not generation approval.
5. Resolve an owner-scoped Reelsy Project. Import only the extracted audio reference through `create_reelsy_media_import`, upload it, and finalize it with `inspect_reelsy_asset`; do not pass a local path or arbitrary URL to music generation.
6. Call `submit_reelsy_music_generation` once with `mode="rewrite_song"`, the ready `sourceAudioArtifactId`, approved `lyrics`, `title`, `style`, optional `vocalGender`, `melodyPreservation`, `sourceRightsConfirmed=true`, `expectedCredits=12`, and one stable `idempotencyKey`. For a new song without a source melody, use `mode="original_song"` and omit the source fields.
7. Poll only with `get_reelsy_job_status`. On success, use the ready `generated_song` Artifact. Never expose or reuse a Provider task ID, Provider URL, storage key, or raw callback payload.
8. Finish outside Reelsy generation: download or consume the persisted song, use its `timedLyrics` when available, locally align any missing timing, replace or mix the video audio, create lyric captions, and verify the final media. Do not call another paid music Job because captioning or local video editing failed.

## Completion Contract

- The approved lyrics and generation settings are visible to the user before charging.
- One successful paid Job produces one reusable owner-scoped `generated_song` Artifact.
- Codex, not Reelsy generation, completes subtitle construction and final video editing.
- If the user requested only the song, finish when the generated song is ready and accessible; do not create a video or Timeline.

## Failure Rules

- Missing Connector or Project: follow the Production Foundation onboarding path without changing the original song-rewrite intent.
- Missing or invalid source audio Artifact: re-extract/import the audio; never substitute an untrusted URL.
- Copyright or source-conflict rejection: preserve the failed Job and refund result; ask for an authorized source or a more original direction instead of bypassing the Provider check.
- Generation succeeded but local editing failed: reuse the existing `generated_song`; retry only the local processing step.
- Job submission outcome is unknown: do not submit again automatically because that can duplicate charges.
