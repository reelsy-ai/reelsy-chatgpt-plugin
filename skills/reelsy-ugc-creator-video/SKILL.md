---
name: reelsy-ugc-creator-video
description: "Plan authentic creator-style UGC videos for Reelsy. Use for selfie testimonials, creator demos, talking-head ads, product reactions, unboxings, social hooks, and native-feeling short-form content. Preserve creator and product identity, then route generation to Reelsy Video Production and deterministic assembly to Reelsy Video Editing."
---

# Reelsy UGC Creator Video

## Domain Method

1. Identify the creator role, product, audience awareness, platform, duration, tone, spoken language, and CTA.
2. Inspect provided creator and product references. Record stable identity, wardrobe, packaging, setting, and camera anchors without inferring private traits.
3. Write a conversational structure: pattern-breaking Hook, personal context, product interaction or proof, honest result or qualification, and native CTA.
4. Prefer first-person language, concrete actions, natural pauses, imperfect handheld framing, and one clear idea per beat. Avoid corporate exposition and unsupported testimonial claims.
5. Define whether dialogue must remain native, be replaced by voiceover, or be supported by captions. Put exact subtitles, emphasis words, emojis, stickers, and CTA text in Editing layers.
6. Produce a compact production intent with ordered beats, spoken intent, shot language, identity anchors, continuity constraints, audio policy, and completion criteria.

## Capability Routing

- Use `$reelsy-video-production` for new creator footage, product interaction shots, or supporting B-roll.
- Use `$reelsy-video-editing` for trims, pacing, captions, active-word styles, titles, stickers, sound effects, music, overlays, and Final revisions.
- Use Editing alone when the user supplies enough existing footage.

## Quality Rules

- Keep the creator's face, body, wardrobe, voice policy, environment, and product identity stable across generated clips.
- Do not create a polished studio ad when the request calls for native UGC.
- Preserve understandable speech and do not let music or sound effects mask dialogue.
- Split clips only on real scene, identity, time, wardrobe, or camera-logic changes.
- Never promise that a generated testimonial is a real customer's experience.
