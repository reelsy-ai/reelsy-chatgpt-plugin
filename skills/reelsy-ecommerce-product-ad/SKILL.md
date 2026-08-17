---
name: reelsy-ecommerce-product-ad
description: "Plan and produce evidence-grounded ecommerce product asset suites or single product creatives in Reelsy. Use when a user wants product listing images, gallery images, product detail panels, product ads, product demos, offer videos, conversion creatives, marketplace assets, shop assets, or a coordinated image-and-video package. Preserve product identity and verified claims, propose selling angles when they are missing, and route paid media generation to Reelsy Video Production. Do not use for generic non-commerce image generation or creator-style UGC unless the user explicitly asks for those outcomes."
---

# Reelsy Ecommerce Product Suite

## Outcome and Compatibility

- Support either one requested product creative or a coordinated image-and-video suite. Never expand a single-image or single-video request into a full suite without the user's approval.
- Keep the existing product-video path compatible: a user who asks only for one product video should receive that video through `$reelsy-video-production` without being forced through gallery or detail-panel planning.
- Read [the asset suite workflow](references/asset-suite-workflow.md) when the request includes multiple ecommerce deliverables, missing selling points, product-detail layouts, or a coordinated campaign.

## Progressive Discovery

1. Let the selected Foundation Skill own Connector authorization, Project resolution, and the exact Canvas or Hosted OpenCut handoff. Never open or construct a generic Reelsy Agent URL from this Domain Skill.
2. Route to `$reelsy-video-production` early enough to open the exact Project Canvas and import or inspect the supplied product evidence before lengthy planning.
3. Treat a recognizable product image or product page plus a product name or category as sufficient to start. If both product identity evidence and a useful product name are missing, ask one compact blocking question. Do not begin with a questionnaire.
4. When the request includes detail panels or a listing package, create a concise Product Fact Sheet before proposing paid Jobs. Extract product identity, visible attributes, source-backed facts, missing fields, and confidence without inventing specifications.
5. Do not require the user to provide selling points before planning. When selling points are missing or the user asks Codex to devise them, enrich the Product Fact Sheet with candidate headlines, user pain points, benefits, and visual directions. Mark every inferred item as a proposal.
6. Show the Product Fact Sheet and proposed detail-panel content to the user for confirmation or edits. Treat approval as copy and planning approval only; do not submit paid Jobs until the combined asset and credit review is accepted.
7. Infer non-blocking choices such as the initial asset count, the `9:16` detail-panel ratio, visual direction, and short-video duration. Show them as editable defaults instead of asking for each choice separately.
8. Ask progressively for optional inputs only when they materially improve a planned deliverable: brand assets for branded layouts, offer details for promotional creatives, or exact specifications for specification panels.
9. For regulated, safety-critical, medical, financial, ingredient, origin, certification, or performance claims, require a reliable user-provided or source-backed fact. User approval alone does not turn an unsupported regulated claim into evidence.

### Connector and Browser Boundary

- Do not invoke a browser search, dashboard inspection, or generic Agent workspace from this Domain Skill. Authentication is handled by `$reelsy-video-production` through the Reelsy OAuth MCP Connector.
- If the Foundation Skill reports missing MCP tools or an unauthenticated Connector, stop and follow its onboarding flow. Preserve the product request and supplied image; do not continue with browser-only work or ask the user to restate the brief.

## Evidence and Selling Angles

- Separate observable facts, source-backed facts, proposed marketing angles, and unsupported claims.
- For detail-page work, keep a Product Fact Sheet with `confirmed`, `proposed`, and `missing` sections. Include the evidence source for confirmed facts and never silently promote a proposal to a fact.
- Use observable and source-backed facts directly. Label inferred benefits or positioning as proposals until the user approves or edits them.
- Never infer exact prices, dimensions, ingredients, origin, certifications, storage temperatures, guarantees, or measurable performance from appearance alone.
- Keep product packaging, labels, colors, materials, scale, and recognizable identity stable unless the user explicitly requests a redesign.

## One Review Gate Before Paid Generation

- Present the confirmed/proposed Product Fact Sheet, recommended selling direction, panel-by-panel copy and visual purpose, deliverable list, editable assumptions, expected image and video Job counts, and total estimated credit cost together.
- Use one combined approval by default. Do not interrupt the user with separate approvals for selling points, asset counts, image generation, and video generation when the combined plan already identifies them clearly.
- Treat a direct approval such as "start," "go ahead," or an equivalent response to that complete plan as approval for only the listed paid Jobs. Connector setup or authorization is never production approval.
- If the user changes one part of the plan, revise only that part and preserve the accepted decisions.

## Capability Routing and Execution

- Use `$reelsy-video-production` for every new gallery image, product detail panel, supporting visual, or product video.
- For every paid image or video submission, pass the optional `deliverable` metadata when the MCP tool supports it. Use a stable `id`, a semantic `kind` such as `gallery_image`, `detail_panel`, or `product_video`, a user-readable `title`, and a 1-based `sequence`.
- Give all gallery images the same `collectionId` and `collectionTitle` (for example, `product-gallery` / `Product gallery`), and all detail panels another shared collection (for example, `product-details` / `Product details`). Keep the product video separate unless the user explicitly requests a video collection. Never encode this metadata only in the prompt.
- Use `aspectRatio="9:16"` for detail panels by default. Allow `3:5`, `4:5`, or `1:1` only when the user or target marketplace explicitly requests another ratio.
- Give every detail panel one information job, such as product overview, pain point and benefit, mechanism/specification, usage/care, or trust/brand story. Do not compress unrelated product information into one prompt.
- Use integrated image-and-text generation for ecommerce stills when the design calls for headlines, selling points, specifications, labels, or explanatory copy. Pass the approved copy verbatim in the panel prompt and do not require a deterministic Editing layer merely because a still image contains exact text.
- For every image deliverable, default to `resolution="1k"` and `quality="low"`. Treat this as the shared Reelsy image default for gallery images, detail panels, and supporting visuals; ask about a higher tier only when it materially matters or the user requests `2k`/`4k` or `medium`/`high`.
- Verify generated text against the approved copy and Product Fact Sheet. Check spelling, numbers, units, language, product identity, packaging, logo, colors, quantities, and required visual details. Regenerate only the failed deliverable with the same business idempotency intent; preserve every accepted Artifact.
- Keep distinct semantic deliverables in distinct image Jobs. Use multiple variants from one Job only for alternatives to the same creative goal, not for unrelated gallery or detail-panel purposes.
- Use `$reelsy-video-editing` only for requested or confirmed video assembly, captions, titles, prices, badges, music, sound effects, stickers, overlays, transitions, filters, trims, or ordering. Integrated text in generated still images does not itself require OpenCut.
- A ready image set or one ready video with no requested video editing is complete when every requested Artifact is visible on the Canvas.
- When Production returns multiple video clips and the user did not already request one combined video, keep every clip visible on the Canvas and ask whether to keep them separate or combine them in Hosted OpenCut.
- Use both Foundation Skills without another confirmation when the approved plan already includes generated media plus video editing or combination.

## Completion and Failure Rules

- Re-read the Project snapshot and verify every accepted ready image and video Artifact on the Canvas. Do not claim that a conversational plan is a Canvas Artifact unless the MCP exposes and returns one.
- A failed image or clip must not invalidate accepted outputs. Retry only the failed target after explaining any changed cost.
- Do not fabricate product facts, provider results, Canvas visibility, credits, or completion.
- Complete the exact approved scope. Additional variants, formats, or edits require a revised plan and any additional credit approval.
