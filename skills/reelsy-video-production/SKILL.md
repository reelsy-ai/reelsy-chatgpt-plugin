---
name: reelsy-video-production
description: "Generate one or more paid AI video assets through Reelsy and show the ready results on the Project Canvas. Use when a user asks to create, generate, recreate, or produce new video media. Choose the fewest valid clips; keep ready clips separate by default, and route to Reelsy Video Editing only when the user already requested editing or combination, or confirms it after seeing multiple results."
---

# Reelsy Video Production

## Required Connector and Canvas Gate

- Before any browser action, call `connector_status` and require the owner-scoped Reelsy Project tools used by this workflow. If the tools are missing from the current task or OAuth is not authenticated, follow [the Connector onboarding reference](references/connector-onboarding.md); preserve the original request, run setup when possible, and create a fresh task after successful authorization when the current snapshot cannot refresh. Do not inspect private implementation routes, open a Reelsy page, or continue with a browser-only fallback.
- Let this Foundation Skill own Connector authorization, Project resolution, and Canvas bootstrap for every Domain Skill that routes here.
- After resolving the Project, call `get_reelsy_project_url`. Open only the exact returned URL, and only when `surface` is `codex_project_canvas`, the returned `projectId` matches the resolved Project, and the URL `project` query parameter contains that same ID.
- Never construct or rewrite the handoff URL. Never open a generic `/dashboard/autonomous-video-agent` route without `project`, and never substitute `reelsy.ai` for `localhost` or `localhost` for `reelsy.ai`.

## Boundaries

- Treat ready generated video Artifacts that are visible on the Project Canvas as the default completion condition.
- Do not create a Timeline or open Hosted OpenCut merely because generation returned more than one clip.
- Route to `$reelsy-video-editing` only when the user explicitly requested editing or combination, or confirms that choice after generation. Do not ask again when the original request already made that intent clear.
- Show the estimated credit cost and obtain explicit confirmation before paid generation. Reuse stable business idempotency keys on retry.
- Preserve every successful target. Retry only failed or missing targets.
- Never fabricate provider results, URLs, probes, credits, Canvas visibility, or success states.

## New User Onboarding

- Treat a natural-language request such as “make this into a short video” as sufficient to begin. Never ask a new user to name a Skill, MCP tool, Project ID, OAuth scope, or URL.
- After the Connector and Canvas Gate passes, resolve or create one owner-scoped Project from the request, then surface the exact Project Canvas handoff before long-running analysis or paid generation. The user should be able to see where work will appear.
- Explain the available path in plain language: Reelsy can generate one or more clips, keep ready clips visible on the Canvas, and optionally open Hosted OpenCut for captions, music, stickers, effects, trimming, ordering, or combination. Ask only for load-bearing choices that cannot be inferred from the request or supplied media.
- If authorization is missing, preserve the original request and tell the user to connect Reelsy in plain language. Do not ask them to repeat the brief after authorization; the host may resume it in the same task or a continuation task.
- A setup or authorization turn is not a production approval. Do not create paid Jobs, import private media, or modify a Timeline until the Connector gate and the user's production intent are both ready.

## Workflow

1. Pass the Required Connector and Canvas Gate. Use `list_reelsy_projects`, `create_reelsy_project`, or `read_reelsy_project_snapshot` to resolve the owner-scoped Project; create a Project when a new user has no target. Get its visible handoff with `get_reelsy_project_url` and open that exact validated URL in the Codex in-app browser before lengthy work.
2. Import and inspect user media with `create_reelsy_media_import` and `inspect_reelsy_asset` when required. Use returned Artifacts as evidence; do not invent unseen product, identity, motion, or narrative facts.
3. Convert the request or active Domain Skill result into a compact production intent: objective, aspect ratio, target duration, continuity anchors, ordered beats, audio policy, and completion criteria. Reuse a `production_plan` returned by `submit_reelsy_analysis` for source-grounded work; otherwise create a zero-credit direct plan with `create_reelsy_production_plan`.
4. Pack adjacent beats into the fewest clips that the selected provider can execute without breaking scene, subject, wardrobe, product, time, or camera continuity. One clip is valid; longer or discontinuous stories may require more.
5. Estimate paid generation from the actual targets and ask for confirmation. Then call `submit_reelsy_generation` once per target with stable, distinct idempotency keys.
6. Poll each Job with `get_reelsy_job_status`. Preserve ready `generated_clip` Artifacts and retry only failed targets.
7. Read the Project snapshot again and verify that every requested ready clip is visible on the Canvas.
8. Apply the handoff decision below. Do not render, upload, publish, or create a Timeline unless the confirmed Editing path requires one.

## Editing Handoff

- One ready clip with no deterministic edit request: stop after the Canvas result is visible.
- Any number of clips with an explicit request for trimming, captions, titles, stickers, visualizers, overlays, transitions, filters, music, ordering, or combination: continue with `$reelsy-video-editing` without another confirmation.
- Multiple ready clips with no explicit combination request: keep every clip visible on the Canvas and ask whether to keep them separate or combine them in Hosted OpenCut.
- Continue with `$reelsy-video-editing` only after the user chooses OpenCut. Keeping separate clips is a complete result.

## Clip Packing Rules

- Split on a real continuity boundary, not merely because the analysis contains another beat.
- Prefer exact text, prices, logos, captions, CTAs, stickers, and visual treatments as optional Editing layers rather than extra paid video targets.
- Do not merge unrelated scenes or incompatible identity states to reduce cost.
- Keep successful generated clips immutable when an Editing-only request follows.

## Failure Rules

- Connector tools unavailable or OAuth unauthenticated: follow [the Connector onboarding reference](references/connector-onboarding.md) before any browser action. Preserve the request and do not replace MCP with source inspection, private HTTP routes, a generic Agent workspace, or a technical prompt that the user must repeat.
- Browser session unavailable: keep polling and settling Project Jobs; reopen the Canvas without resubmitting generation.
- Partial generation failure: preserve ready clips and retry only the failed or missing target after explaining any new cost.
- Canvas projection missing: re-read the Project snapshot and repair the projection path; do not regenerate media that already has a ready Artifact.
