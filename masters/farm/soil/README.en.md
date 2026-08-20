# Phase 1 Soil Foundation

**Status:** Canonical Phase 1 soil reference  
**Project:** Mayhoa  
**Art style:** Mayhoa Nostalgic Hand-Painted Farm Sprite

This folder contains the locked soil-state foundation for the first Mayhoa farm production set.

## Canonical master states

- `soil_empty_v01.png`
- `soil_tilled_v01.png`
- `soil_wet_v01.png`
- `soil_planted_v01.png`
- `soil_dry_v01.png`
- `soil_harvested_v01.png`

All six masters use a transparent 512x512 canvas and the same camera angle, footprint, center, and grounding logic. Approximate visual footprint: x 88-424, y 163-355; placement center around (256, 268).

## State semantics

- `empty`: smooth untreated soil with minimal surface disturbance.
- `tilled`: canonical furrow pattern and primary crop-placement reference.
- `wet`: darker hydrated soil with restrained soft reflections; never glossy.
- `planted`: tilled soil with subtle planting-hole/seed marks; crops remain separate overlays.
- `dry`: lighter, drier soil with sparse organic cracks.
- `harvested`: disturbed tilled soil with restrained cut-stubble cues.

## Locked rendering rules

- selective dark-brown/chromatic edge treatment, never pure black;
- gentle upper-left lighting and soft grounding shadow;
- warm nostalgic brown palette with limited tone count;
- soft painterly texture, no glossy/vector-clean rendering;
- no baked crop, weed, pest, UI, or background scene;
- transparent background and identical placement geometry across states.

## Runtime atlas

For PixiJS, Phase 1 includes a shared-texture 1x atlas:

- `runtime/1x/farm/soil/soil_states_v01.png` - 576x384, six 192x192 cells.
- `runtime/soil_states_v01.json` - frame coordinates.

Frame order: top row `empty`, `tilled`, `wet`; bottom row `planted`, `dry`, `harvested`. The 512x512 masters remain the source for future 2x/high-DPI exports instead of shipping oversized masters directly in gameplay.

## Exit criteria

Phase 1 is locked when all six states remain clearly distinguishable at runtime size while preserving identical footprint and perspective. Phase 2 crop growth stages must be composited and reviewed against `soil_tilled_v01.png` first, then spot-checked against wet, dry, and planted states.
