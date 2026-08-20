# Phase 2 Core Crop Pack

**Status:** Canonical Phase 2 core crop growth reference  
**Project:** Mayhoa  
**Art style:** Mayhoa Nostalgic Hand-Painted Farm Sprite

This folder contains the Phase 2 growth-stage masters for rice, corn, and carrot. Each crop uses five distinct silhouettes rather than scaling one drawing.

## Growth stages

1. `stage-01_seeded`
2. `stage-02_sprout`
3. `stage-03_young`
4. `stage-04_mature`
5. `stage-05_harvestable`

## Canonical crops

- `rice/` — tiny emergence -> expanding grass clump -> mature clump -> golden panicles at harvest.
- `corn/` — tiny emergence -> broader leaves -> structured stalk -> tassel -> readable corn ears at harvest.
- `carrot/` — tiny emergence -> leafy rosette -> denser feathery foliage -> subtle root shoulder -> orange harvest cue.

## Locked production rules

- transparent 512x512 master canvas;
- common placement anchor around `(0.5, 0.684)`;
- visual base aligns to the Phase 1 soil footprint;
- upper-left lighting, soft contact shadow, selective dark-chromatic outlines;
- no baked soil, weeds, pests, UI, text, or scene background;
- stage progression changes silhouette, density, and focal cues;
- species identity must remain readable at 192px runtime-cell size.

## Runtime atlas

`runtime/1x/farm/crops/core_crops_v01.png` is a 960x576 shared-texture atlas with 192x192 cells. `runtime/core_crops_v01.json` stores frame coordinates and the shared placement anchor. Rows are rice, corn, carrot. Columns follow the five-stage order above.

## Reproducible generation

Run `python scripts/generate_phase2_core_crops.py --root .` with Pillow 11.3.0 to regenerate the fifteen masters, runtime atlas, and manifest deterministically.

## Phase 2 exit criteria

Phase 2 is locked when all fifteen frames: (1) remain distinguishable at gameplay size, (2) sit plausibly on the Phase 1 `soil_tilled` reference, (3) preserve a coherent relative crop scale, and (4) keep harvestable states more readable without glossy or neon treatment.
