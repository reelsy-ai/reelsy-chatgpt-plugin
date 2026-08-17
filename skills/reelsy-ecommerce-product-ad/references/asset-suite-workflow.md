# Ecommerce Asset Suite Workflow

## Contents

- [Image Defaults](#image-defaults)
- [Progressive Conversation](#progressive-conversation)
- [Product Fact Sheet](#product-fact-sheet)
- [Detail Panel Architecture](#detail-panel-architecture)
- [Evidence Rules](#evidence-rules)
- [Combined Review](#combined-review)
- [Integrated Image and Text Generation](#integrated-image-and-text-generation)
- [Deliverable Metadata](#deliverable-metadata)
- [Video Routing](#video-routing)

Use this reference for a coordinated ecommerce package, missing selling points, product-detail layouts, or a request that combines product images and video.

## Image Defaults

- Use `aspectRatio="9:16"` for Product Detail Panels by default. Treat `3:5`, `4:5`, and `1:1` as explicit user or marketplace overrides.
- Use `resolution="1k"` and `quality="low"` for every image Job unless the user explicitly requests a higher tier.
- Treat `1k + low` as the shared default for Gallery Images, Detail Panels, and supporting visuals. Do not create a separate quality decision during the first review.
- A user-requested `2k`/`4k` resolution or `medium`/`high` quality is an explicit upgrade and must be reflected in the cost review before submission.

## Default Suite

Use these only when the user requests a complete package without specifying quantities:

| Set | Default |
| --- | ---: |
| Gallery Images | 6 |
| Product Detail Panels | 4 |
| Product Video | 1 |

Use the Full listing page mode below when the user wants a complete long-form detail page with 6 panels. Treat all quantities as editable planning defaults, not MCP limits.

## Progressive Conversation

| Stage | Required behavior | Do not do |
| --- | --- | --- |
| Evidence intake | Inspect supplied product images, a product page, packaging text, or user-provided specifications. Identify the product name, category, and intended use. | Do not ask for a complete marketing brief before inspecting evidence. |
| Blocking input | If product identity is still unclear, ask for one recognizable source image or product page and a useful product name. | Do not ask for platform, audience, colors, CTA, price, and selling points in the same opening question. |
| Product Fact Sheet | Extract confirmed facts, visible attributes, source-backed facts, proposed enrichments, and missing fields before planning detail panels. | Do not turn a visual guess into a specification, ingredient, origin, certification, price, or performance claim. |
| Selling-point proposal | Propose one primary angle and a small set of supporting angles from the available evidence. Include the user pain point and a visual expression for each. | Do not present inferred claims as verified facts. |
| User review | Let the user confirm or edit the facts, selling points, language, panel count, and panel copy in one compact review. | Do not submit paid Jobs before the user approves the combined plan. |
| Draft suite | Map every approved angle to one concrete deliverable and infer sensible defaults such as `9:16`, four detail panels, and a short product video. | Do not hide defaults or create a full suite when the user requested one creative. |
| Execution | Submit only approved Jobs, keep stable intent per deliverable, and verify every result against the approved brief. | Do not rerun accepted outputs when one target fails. |

## Product Fact Sheet

Build this in the conversation before any paid detail-panel Job:

```text
Confirmed facts
- Product identity and category
- Visible color, form, packaging, material appearance, and included components
- User-provided or source-backed specifications, ingredients, origin, certifications, or usage instructions

Proposed content
- Primary selling angle
- Supporting benefits and user pain points
- Headline and supporting copy candidates
- Visual direction for each panel

Missing or restricted information
- Exact specifications, ingredients, origin, certification, price, guarantee, or measurable performance
- Any field required by the user's requested marketplace or compliance policy
```

Use the source for every confirmed fact. Let the user accept, edit, or reject proposed content. Ask only for missing fields that block a specific panel or create factual, compliance, identity, or cost risk.

## Detail Panel Architecture

Use one information job per 9:16 panel. Keep the following as editable planning defaults:

| Mode | Default panels | Suggested information structure |
| --- | ---: | --- |
| Lightweight package | 4 | Product overview; pain point and core benefit; mechanism/specification; usage, care, or trust |
| Full listing page | 6 | Product overview; problem context; core benefits; structure/mechanism; usage and audience; specifications, trust, or CTA |

Detail panels are additional to Gallery Images. A single product video request remains on the existing video path and does not trigger this architecture.

For each panel, prepare:

- `title`: the approved panel title;
- `copy`: exact approved text and numbers;
- `facts`: the Product Fact Sheet entries used by the panel;
- `visualDirection`: the composition, product view, scene, and hierarchy;
- `aspectRatio`: `9:16` unless explicitly overridden.

## Evidence Rules

| Class | Examples | Allowed use |
| --- | --- | --- |
| Observable | Visible color, package shape, material appearance, included components, visible texture. | Use directly while preserving visual identity. |
| Source-backed | Product page copy, packaging text, user-provided specifications, approved brand guide. | Use directly and preserve exact meaning. |
| Proposed content | Convenience, gifting, daily use, premium positioning, freshness cues, or a likely audience benefit inferred from context. | Show to the user as a proposal and use after approval. |
| Restricted or unsupported | Medical outcomes, guaranteed performance, certification, origin, ingredients, exact dimensions, or safety claims without evidence. | Request reliable evidence or omit. Simple approval is not sufficient. |

Keep product packaging, labels, colors, materials, scale, and recognizable identity stable unless the user explicitly requests a redesign.

## Combined Review

Present one compact review before any paid Job:

```text
Product brief
- Confirmed facts: ...
- Proposed selling points: ...
- Missing or restricted information: ...

Recommended direction
- Primary angle: ...
- Supporting angles: ...
- Copy language and marketplace: ...

Asset plan
- Gallery Images: ...
- Product Detail Panels: ... at 9:16
- Product Video: ...

Panel plan
- Panel 1: title, approved copy, visual purpose
- Panel 2: title, approved copy, visual purpose
- ...

Estimated execution
- Image Jobs: ...
- Video Jobs: ...
- Total estimated credits: ...
```

When there is no material ambiguity, ask for one approval of this complete plan. Ask a follow-up only when a missing fact blocks a specific deliverable or creates a meaningful factual, compliance, identity, or cost risk.

## Integrated Image and Text Generation

- Generate the composition, product imagery, typography, and approved marketing copy together when that produces the intended ecommerce design.
- Provide the approved text verbatim in each panel prompt. Keep each panel focused; do not overload one image with unrelated copy.
- Preserve product identity across every panel and reuse the same confirmed facts and approved selling direction.
- After generation, compare every required string and factual statement with the approved plan. Check spelling, numbers, units, punctuation, language, logo treatment, and product identity.
- If one deliverable fails, refine and regenerate only that deliverable. Do not regenerate the entire suite.
- Use deterministic text layout only as a fallback when repeated integrated generation cannot satisfy the approved exact copy. Do not make it the default path.

## Deliverable Metadata

When submitting a generation Job, keep presentation semantics in the MCP request instead of relying on prompt wording:

```json
{
  "deliverable": {
    "id": "detail-01",
    "kind": "detail_panel",
    "title": "Core benefit panel",
    "collectionId": "product-details",
    "collectionTitle": "Product details",
    "sequence": 1,
    "aspectRatio": "9:16"
  }
}
```

Use one stable `collectionId` per visual set and a unique `id` per approved deliverable. The Canvas uses this metadata to show a compact set while preserving every underlying Artifact for selection and recovery. Older tool versions may omit `deliverable`; continue the workflow and use the returned Artifact title.

## Video Routing

- Preserve the existing single-video workflow when the user asks only for a product video.
- For a suite, use the approved Product Fact Sheet and selling direction as continuity anchors for the video.
- Enter `$reelsy-video-editing` without another approval only when the reviewed suite already includes captions, titles, CTA layers, music, effects, ordering, or clip combination.
- Otherwise, finish when the ready product video is visible on the Canvas.
