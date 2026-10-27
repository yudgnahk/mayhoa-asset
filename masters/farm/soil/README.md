# Phase 1 - Soil Foundation

**Status:** Canonical Phase 1 soil reference  
**Project:** Mayhoa  
**Art style:** Mayhoa Nostalgic Hand-Painted Farm Sprite

This folder contains the canonical soil-state set used as the visual foundation for Mayhoa's first farm batch.

## Canonical master states

- `soil_empty_v01.png`
- `soil_tilled_v01.png` (permanently corrupted IDAT — kept only for historical comparison) and `soil_tilled_v02.png` (canonical, 2026-09-05)
- `soil_wet_v01.png`
- `soil_planted_v01.png`
- `soil_dry_v01.png`
- `soil_harvested_v01.png`

All six masters use a transparent 512x512 canvas and the same camera angle, footprint, asset placement center and contact-shadow logic. Approximate footprint: x 88-424, y 163-355; placement center around (256, 268).

## State semantics

- `empty`: untreated soil, a relatively flat surface with little disturbance.
- `tilled`: the canonical furrow pattern, and the primary reference for placing crops.
- `wet`: darker hydrated soil with very restrained soft reflections, never glossy.
- `planted`: tilled soil with subtle planting-hole/seed marks; crops remain a separate overlay.
- `dry`: lighter, drier soil with a few organic cracks.
- `harvested`: post-harvest soil with disturbance marks and very subtle cut stubble.

## Locked rendering rules

- selective dark brown/chromatic edges, never pure black;
- gentle upper-left lighting and a soft contact shadow;
- warm, nostalgic brown palette with a limited tone count;
- soft painterly texture, avoiding glossy/vector-clean rendering;
- no baked crop, weed, pest, UI or background scene;
- transparent background and identical placement geometry across every state.

## Runtime atlas

For PixiJS, soil uses a 1x shared-texture atlas:

- `runtime/1x/farm/soil/farm_soil_v01.png` - 576x384, six 192x192 cells.
- `runtime/farm_soil_v01.json` - frame coordinates + per-frame anchors.

Frame order is alphabetical: top row `soil_dry`, `soil_empty`, `soil_harvested`; bottom row `soil_planted`, `soil_tilled`, `soil_wet`. The frame key here is the tile's **full stem** (`soil_dry`, `soil_tilled`...) — soil is the only exception; every atlas that has stages uses the slot id `<species>_stage-0N`.

Anchor `x` is always = 0.5; anchor `y` is measured per file and therefore not perfectly uniform: 0.701172 (`soil_empty`) up to 0.703125 (the other 5 tiles), with a representative `placementAnchor` of `(0.5, 0.703125)` and `anchorUniform: false`. `masterCanvas` = 512x512, and it remains the source for future 2x/high-DPI exports instead of shipping oversized masters directly into gameplay.

The `soil_tilled` cell comes from `soil_tilled_v02.png`: the script always picks the highest version that is **readable**, and `v01` has permanently corrupted IDAT data.

This atlas replaces `soil_states_v01` (deleted from the repo). An atlas is a **product generated from the masters, never hand-edited** — rebuild it with:

```bash
python3 tools/build_atlas.py --atlas farm_soil_v01   # add --dry-run to preview
```

Run `python3 tools/build_atlas.py` with no arguments to rebuild all 4 atlases (`farm_crops_v01`, `farm_trees_v01`, `farm_aquatic_v01`, `farm_soil_v01`). The script is idempotent: two runs produce byte-identical output.

## Phase 1 exit criteria

Phase 1 is locked when all six states remain clearly distinguishable at runtime size while preserving identical footprint and perspective. Phase 2 must composite/review the crop growth stages on `soil_tilled_v02.png` first, then spot-check against wet, dry and planted.
