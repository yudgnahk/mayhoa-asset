# Phase 1 Soil Foundation

**Status:** Canonical Phase 1 soil reference  
**Project:** Mayhoa  
**Art style:** Mayhoa Nostalgic Hand-Painted Farm Sprite

This folder contains the locked soil-state foundation for the first Mayhoa farm production set.

## Canonical master states

- `soil_empty_v01.png`
- `soil_tilled_v01.png` (permanently corrupt IDAT — kept for historical comparison only) and `soil_tilled_v02.png` (canonical, 2026-09-05)
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

For PixiJS, soil ships as a shared-texture 1x atlas:

- `runtime/1x/farm/soil/farm_soil_v01.png` - 576x384, six 192x192 cells.
- `runtime/farm_soil_v01.json` - frame coordinates plus per-frame anchors.

Frame order is alphabetical: top row `soil_dry`, `soil_empty`, `soil_harvested`; bottom row `soil_planted`, `soil_tilled`, `soil_wet`. The frame key here is the tile's **full stem** (`soil_dry`, `soil_tilled`, ...) — soil is the one exception; every staged atlas uses the `<species>_stage-0N` slot id instead.

Anchor `x` is always 0.5; anchor `y` is measured per file, so it is not perfectly uniform: 0.701172 (`soil_empty`) through 0.703125 (the other five tiles), with a representative `placementAnchor` of `(0.5, 0.703125)` and `anchorUniform: false`. `masterCanvas` is 512x512 and remains the source for future 2x/high-DPI exports instead of shipping oversized masters directly in gameplay.

The `soil_tilled` cell comes from `soil_tilled_v02.png`: the builder always picks the highest **readable** version, and `v01` has a permanently corrupt IDAT stream.

This atlas replaces `soil_states_v01`, which was deleted from the repo. An atlas is a **build product of the masters, never hand-edited** — rebuild it with:

```bash
python3 tools/build_atlas.py --atlas farm_soil_v01   # add --dry-run to preview
```

Run `python3 tools/build_atlas.py` with no arguments to rebuild all four atlases (`farm_crops_v01`, `farm_trees_v01`, `farm_aquatic_v01`, `farm_soil_v01`). The script is idempotent: two runs produce byte-identical output.

## Exit criteria

Phase 1 is locked when all six states remain clearly distinguishable at runtime size while preserving identical footprint and perspective. Phase 2 crop growth stages must be composited and reviewed against `soil_tilled_v02.png` first, then spot-checked against wet, dry, and planted states.
