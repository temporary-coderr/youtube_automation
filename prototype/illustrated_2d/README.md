# WISE-LAB Illustrated 2D Character Rig

This is a separate experiment. It does not replace or modify the comic, Blender hybrid, or production engines.

## Why this is a different approach

The previous rig benchmarks generated the character from primitive geometry. This track starts from a finished, hand-designed illustrated character supplied as a layered OpenRaster (`.ora`) file. Blender is used for the skeleton, IK, prop constraints, camera, lighting, compositing and MP4 render—not to invent the character from capsules and spheres.

## Art asset contract

The source `.ora` must be a single 1280x720 or 1920x1080 character canvas with transparent background and separately named layers:

- `head`, `hair_back`, `hair_front`, `torso`
- `upper_arm_L`, `forearm_L`, `hand_L`
- `upper_arm_R`, `forearm_R`, `hand_R`
- `thigh_L`, `shin_L`, `foot_L`
- `thigh_R`, `shin_R`, `foot_R`

Each limb segment must be drawn with overlap at its joint so rotation does not expose gaps. Hands, sleeves, hair and clothing details should be painted into the relevant layer; do not replace the artwork with generated primitive shapes. Keep the recurring male character's dark charcoal hoodie, dark jeans, warm medium-brown skin and messy black hair consistent.

## Pivot and skeleton data

A JSON rig map defines each bone's head/tail in source-canvas pixel coordinates and each layer's attachment bone and pivot pixel. The importer converts those coordinates to Blender units and parents textured planes to the matching bones. Missing required layers or pivots must fail loudly; no silent fallback to circles/capsules.

## First animation gate

A 10-second landscape shot: seated at a desk, notices a phone notification, reaches, grips, lifts and looks at the phone. Required:
- hand stays visibly attached to the phone during pickup;
- shoulder, elbow and wrist move as a connected chain;
- torso leans and shifts weight rather than the arm stretching alone;
- phone rotates with the hand after contact;
- camera has a restrained push-in; environment has parallax;
- no limb gaps, detached joints, clipping, duplicate captions or primitive placeholder body parts.

## Acceptance

Do not merge until the actual MP4 and contact sheet are reviewed. A successful render/encode is not a visual-quality pass. Keep the existing engines untouched.
