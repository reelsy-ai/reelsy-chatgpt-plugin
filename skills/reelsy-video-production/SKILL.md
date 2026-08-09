---
name: reelsy-video-production
description: "Generate one or more AI video assets through Reelsy and produce the first playable project timeline and Final. Use when a user asks to create, generate, recreate, or finish a video and new paid media must be produced. Choose the fewest valid clips for the requested duration and story; never assume exactly two clips."
---

# Reelsy Video Production

## Boundaries

- Treat a playable Timeline and Final as the completion condition. Internal plans, schemas, and review nodes are not user-facing gates.
- Show the estimated credit cost and obtain explicit confirmation before paid generation. Reuse stable business idempotency keys on retry.
- Preserve every successful target. Retry only failed or missing targets.
- Run FFmpeg only on the Codex host. Reelsy owns provider access, Project facts, media imports, Timeline revisions, Final publication, and Canvas projection.
- Never fabricate provider results, URLs, probes, credits, or success states.

## Workflow

1. Use `list_reelsy_projects`, `create_reelsy_project`, or `read_reelsy_project_snapshot` to resolve the owner-scoped Project. Get its visible handoff with `get_reelsy_project_url` and open the Canvas in the Codex in-app browser.
2. Import and inspect user media with `create_reelsy_media_import` and `inspect_reelsy_asset` when required. Use returned Artifacts as evidence; do not invent unseen product, identity, motion, or narrative facts.
3. Convert the request or active Domain Skill result into a compact production intent: objective, aspect ratio, target duration, continuity anchors, ordered beats, audio policy, and completion criteria. Reuse a `production_plan` returned by `submit_reelsy_analysis` for source-grounded work; otherwise create a zero-credit direct plan with `create_reelsy_production_plan`.
4. Pack adjacent beats into the fewest clips that the selected provider can execute without breaking scene, subject, wardrobe, product, time, or camera continuity. One clip is valid; two clips are common; longer videos may require more.
5. Estimate paid generation from the actual targets and ask for confirmation. Then call `submit_reelsy_generation` once per target with stable, distinct idempotency keys.
6. Poll each Job with `get_reelsy_job_status`. Preserve ready `generated_clip` Artifacts and retry only failed targets.
7. Call `submit_reelsy_composition` with every ready clip in narrative order. Default to `native_only`; use music only when it is licensed or user-owned and requested.
8. Follow `$reelsy-video-editing` when the request needs captions, titles, stickers, visualizers, overlays, transitions, filters, music, trimming, or revision work.
9. For a requested Final, download the current Timeline media, run `scripts/compose_timeline.py` with a `reelsy_local_composition_request_v1` manifest, upload the rendered file with `create_reelsy_media_import`, inspect it, and call `publish_reelsy_final`.
10. Read the Project snapshot again and verify the ready Final, Timeline revision, relations, and playable Canvas output.

## Clip Packing Rules

- Split on a real continuity boundary, not merely because the analysis contains another beat.
- Prefer exact text, prices, logos, captions, CTAs, stickers, and visual treatments as Editing layers rather than extra paid video targets.
- Do not merge unrelated scenes or incompatible identity states to reduce cost.
- Keep successful generated clips immutable when an Editing-only request follows.

## Local Composition

The request manifest accepts one or more ordered clips:

```json
{
  "format": "reelsy_local_composition_request_v1",
  "outputPath": "/absolute/path/final.mp4",
  "canvas": { "width": 480, "height": 854 },
  "fps": 30,
  "clips": [
    { "path": "/absolute/path/clip-1.mp4", "trimStartMs": 0, "durationMs": 8000 }
  ],
  "soundtrack": null
}
```

Never upload after a failed local render. Reject a Final whose duration differs from the Timeline by more than one second.
