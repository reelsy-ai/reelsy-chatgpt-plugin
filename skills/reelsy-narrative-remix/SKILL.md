---
name: reelsy-narrative-remix
description: "Analyze a source video's observed roles, world rules, causal events, recurring motifs, pacing, shot handoffs, and ending payoff, then adapt that narrative into a new Reelsy video. Use for plot recreation, viral story remix, branded narrative transfer, or multi-event video cloning. Use Motion Clone for one continuous action."
---

# Reelsy Narrative Remix

## Domain Method

1. Require one source video or supported public source. If the request is only a continuous action or camera trajectory, route to `$reelsy-motion-clone` instead.
2. Import and inspect the full source as open-world evidence. Do not assume a conventional ad, creator, dialogue, conflict, office, product demo, or CTA unless the evidence shows it.
3. Build an evidence-grounded source map containing ordered shots, observable actions, participating roles, world and prop rules, causal handoffs, recurring motifs, pacing, audio facts, and ending payoff.
4. Derive a narrative skeleton that preserves functions rather than protected surface details: Hook, required causal beats, escalation or progression, reversals, motifs, and payoff.
5. Bind source roles to target subjects and define continuity entities for every repeated person, product, creature, prop, environment, logo, or visual style.
6. Pack one to three adjacent causal beats into the fewest production clips that preserve scene, cast, wardrobe, hero prop, time, and camera logic. Do not create one paid clip per analytical source shot.
7. Put exact subtitles, prices, logos, UI text, CTA copy, transitions, overlays, and music decisions in Editing layers.
8. Produce a compact production intent with evidence references, source-to-target role bindings, ordered production clips, continuity anchors, preserve/replace boundaries, audio policy, and payoff criteria.

## Capability Routing

- Use `$reelsy-video-production` for the adapted production clips.
- Use `$reelsy-video-editing` for the narrative assembly, captions, titles, overlays, visualizers, music, transitions, trims, and Final branch.
- Use Editing alone when remixing supplied footage without new paid generation.

## Quality Rules

- Every required target event must trace to observed source evidence; do not invent missing source facts.
- Preserve causal order and payoff function, not merely color palette or camera style.
- Split on a real world, cast, identity, wardrobe, hero-prop, time, or camera-logic boundary.
- Keep successful clips and prior Finals when revising only one narrative segment or assembly layer.
- Do not expose provider payloads, credentials, storage keys, or internal workflow identifiers.
