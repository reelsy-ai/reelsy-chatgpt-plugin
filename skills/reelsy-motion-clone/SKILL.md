---
name: reelsy-motion-clone
description: "Analyze movement and camera trajectories from a reference video and transfer the motion rhythm and key states to a new subject in Reelsy. Use for dances, actions, pose sequences, gestures, movement timing, or camera-motion transfer. Use Narrative Remix instead for multi-event plots."
---

# Reelsy Motion Clone

## Domain Method

1. Require one motion reference video and one target identity or subject reference. Ask only for a missing required source.
2. Import and inspect the motion video. Treat it as motion evidence, not as a source of target identity, branding, or hidden intent.
3. Extract the action phases, body or object trajectory, pose landmarks, timing, direction changes, camera path, framing, speed changes, and contact constraints.
4. Classify cloneability:
   - `direct`: clear subject, readable motion, stable framing, and executable trajectory.
   - `review`: occlusion, cuts, crowding, fast motion, or camera ambiguity create fidelity risk; explain the risk before paid generation.
   - `unsupported`: the motion cannot be isolated or safely reproduced; do not submit generation.
5. Define one stable target identity, wardrobe, environment, lighting, start pose, action phases, end pose, camera behavior, and negative constraints.
6. Say that Reelsy will reproduce the analyzed motion rhythm and key states as closely as possible. Never promise an exact clone.

## Capability Routing

- Let the selected Foundation Skill own Connector authorization, Project resolution, and the exact Canvas or Hosted OpenCut handoff. Never open or construct a generic Reelsy Agent URL from this Domain Skill.
- Use `$reelsy-video-production` to generate the motion-guided footage with the fewest continuous clips.
- A single ready motion video with no requested deterministic edits is complete when it is visible on the Canvas.
- Use `$reelsy-video-editing` for requested trims, speed-neutral pacing adjustments, captions, titles, music, sound effects, overlays, ordering, or combination.
- When Production returns multiple clips and the user did not already request one combined video, show every clip on the Canvas and ask whether to keep them separate or combine them in Hosted OpenCut.
- For a new identity using the same motion, reuse the existing trusted motion analysis and generate only the new branch.

## Quality Rules

- Preserve the target subject identity from the opening frame through the complete action.
- Do not pass the reference motion video's identity or copyrighted branding into target prompts unless authorized and explicitly requested.
- Keep action phase order and timing relationships; do not replace hard motion with unrelated cinematic movement.
- Preserve previous result branches when generating a new identity version.
