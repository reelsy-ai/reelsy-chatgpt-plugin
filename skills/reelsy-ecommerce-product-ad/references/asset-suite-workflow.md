# Ecommerce Asset Suite Workflow

Use this reference for a coordinated ecommerce package, missing selling points, product-detail layouts, or any request that combines product images and video.

## Progressive Conversation

| Stage | Required behavior | Do not do |
| --- | --- | --- |
| Evidence intake | Inspect supplied product images or a product page and identify the product name or category. | Do not ask for a complete marketing brief before inspecting evidence. |
| Blocking input | If product identity is still unclear, ask for one recognizable source image or product page and a useful product name. | Do not ask for platform, audience, colors, CTA, price, and selling points in the same opening question. |
| Selling-point proposal | Propose a primary angle and a small set of supporting angles from available evidence. Mark assumptions and facts that need confirmation. | Do not present inferred claims as verified facts. |
| Draft suite | Map each approved or proposed angle to a concrete deliverable and infer sensible defaults. | Do not turn defaults into hidden requirements. |
| Review | Present selling angles, deliverables, assumptions, Job counts, and estimated credits in one review. | Do not split one coherent plan into repeated mechanical approvals. |
| Execution | Submit only the approved Jobs, keep stable intent per deliverable, and verify each result. | Do not rerun accepted outputs when one target fails. |

Follow the user's language in conversation. Keep internal Skill instructions and plan labels in English.

## Default Suite

Use this only when the user requests a complete package and does not specify quantities:

| Set | Default | Typical purposes |
| --- | ---: | --- |
| Gallery Images | 6 | Hero, product detail, lifestyle context, use case, scale or packaging, and one supporting benefit. |
| Product Detail Panels | 3 | Core benefits, specifications or mechanism, and usage, care, storage, or brand story. |
| Product Video | 1 | A short product-focused video with immediate recognition, a coherent demonstration, and an approved CTA when supplied. |

Detail panels are additional to gallery images by default. Treat these numbers as editable planning defaults, not MCP limits. Respect an explicitly requested smaller or larger scope.

## Evidence Classes

| Class | Examples | Allowed use |
| --- | --- | --- |
| Observable | Visible color, package shape, material appearance, included components, visible texture. | Use directly while preserving visual identity. |
| Source-backed | Product page copy, packaging text, user-provided specifications, approved brand guide. | Use directly and preserve exact meaning. |
| Proposed angle | Convenience, gifting, daily use, premium positioning, freshness cues, or a likely audience benefit inferred from context. | Present as a proposal and use after approval. |
| Restricted or unsupported | Medical outcomes, guaranteed performance, certification, origin, ingredients, exact dimensions, or safety claims without evidence. | Request reliable evidence or omit. Simple approval is not sufficient for regulated claims. |

## Combined Review Format

Present one compact review before any paid Job:

```text
Recommended direction
- Primary angle: ...
- Supporting angles: ...

Asset plan
- 6 gallery images: ...
- 3 product detail panels: ...
- 1 product video: ...

Assumptions to approve or edit
- ...

Estimated execution
- Image Jobs: ...
- Video Jobs: ...
- Total estimated credits: ...
```

When there is no material ambiguity, ask for one approval of this complete plan. Ask a follow-up only when a missing fact blocks a specific deliverable or would create a meaningful factual, compliance, cost, or identity risk.

## Integrated Image and Text Generation

- Generate the composition, product imagery, typography, and marketing copy together when that produces the intended ecommerce design.
- Provide the approved text verbatim in the image prompt. Keep each panel focused; avoid overloading one image with unrelated copy.
- After generation, compare every required string and factual statement with the approved plan. Check spelling, numbers, units, punctuation, language, logo treatment, and product identity.
- If one deliverable fails, refine and regenerate only that deliverable. Do not regenerate the entire suite.
- Use deterministic text layout only as a fallback when repeated integrated generation cannot satisfy the approved exact copy. Do not make it the default path.

## Deliverable Metadata

When submitting a generation Job, keep presentation semantics in the MCP request instead of relying on prompt wording:

```json
{
  "deliverable": {
    "id": "gallery-01",
    "kind": "gallery_image",
    "title": "Hero product image",
    "collectionId": "product-gallery",
    "collectionTitle": "Product gallery",
    "sequence": 1
  }
}
```

Use one stable `collectionId` per visual set and a unique `id` per approved deliverable. The Canvas uses this metadata to show a compact set while preserving every underlying Artifact for selection and recovery. If the request is a single creative, omit the collection fields. Older tool versions may omit `deliverable`; continue the workflow and use the returned Artifact title.

## Video Routing

- Preserve the existing single-video workflow when the user asks only for a product video.
- For a suite, use the approved product identity and selling direction as continuity anchors for the video.
- Enter `$reelsy-video-editing` without another approval only when the reviewed suite already includes captions, titles, CTA layers, music, effects, ordering, or clip combination.
- Otherwise, finish when the ready product video is visible on the Canvas.
