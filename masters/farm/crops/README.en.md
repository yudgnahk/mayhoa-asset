# Phase 2 Core Crops and Phase 3 Herb / Low Crop Pack

**Status:** Canonical Phase 2 and Phase 3 crop growth reference<br>
**Project:** Mayhoa<br>
**Art style:** Mayhoa Nostalgic Hand-Painted Farm Sprite

This folder contains the Phase 2 growth-stage masters for rice, corn, and carrot, plus the Phase 3 herb / low crop masters for tonkin-jasmine, culantro, and mint. Each crop uses five structurally distinct growth silhouettes rather than scaling one drawing.

## Growth stages

1. `stage-01_seeded`
2. `stage-02_sprout`
3. `stage-03_young`
4. `stage-04_mature`
5. `stage-05_harvestable`

## Phase 2 core crops

- `rice/` — tiny emergence -> expanding grass clump -> mature clump -> golden panicles at harvest.
- `corn/` — tiny emergence -> broader leaves -> structured stalk -> tassel -> readable corn ears at harvest.
- `carrot/` — tiny emergence -> leafy rosette -> denser feathery foliage -> subtle root shoulder -> orange harvest cue.

## Phase 3 herb / low crops

- `tonkin-jasmine/` — Telosma cordata (Vietnamese: thiên lý); seeded emergence -> tiny vine sprout -> young leafy vine -> fuller heart/ovate-leaf vine -> restrained pale yellow-green flower clusters at harvest.
- `culantro/` — Eryngium foetidum (Vietnamese: ngò gai); emergence -> tiny basal rosette -> widening young rosette -> dense mature rosette -> lush harvestable rosette with long, narrow, serrated-looking leaves. It is not coriander/cilantro foliage.
- `mint/` — paired oval-to-lanceolate textured leaves -> branching stems -> increasingly dense, lush mint clump, with characteristic leaf-edge and texture cues kept readable at gameplay scale.

## Locked production rules

- transparent 512x512 master canvas;
- crops are bottom-anchored sprites: root `(256, 458)` = `(0.5, 0.89453125)`, pinned by the engine to the soil-plate center (replaces the legacy `(0.5, 0.684)` anchor as of 2026-08-26);
- visual base aligns to the Phase 1 soil footprint;
- upper-left lighting, soft contact shadow, selective dark-chromatic outlines;
- no baked soil, weeds, pests, UI, text, or scene background;
- stage progression changes silhouette, density, and focal cues;
- species identity must remain readable at 192px runtime-cell size.

## Runtime atlases

`runtime/1x/farm/crops/farm_crops_v01.png` is a 960x1152 shared-texture atlas with 192x192 cells that merges all six crop packs (Phase 2 + Phase 3) into one texture: 6 species x 5 stages = 30 frames. `runtime/farm_crops_v01.json` stores frame coordinates, per-frame anchors, and `stageNames`.

- Rows follow alphabetical order: carrot, corn, culantro, mint, rice, tonkin-jasmine. Columns follow `stageOrder` = `stage-01`..`stage-05`.
- The frame key is a **slot id**, `<species>_stage-0N` (for example `culantro_stage-04`); it carries no semantic label, so the game builds keys directly from species + stage index without a lookup table. Semantic labels live in `stageNames` (`<species> -> ["seeded","sprout",...]`) and are display-only.
- A uniform `(0.5, 0.894531)` anchor applies to all 30 frames (`anchorUniform: true`), matching the `(256, 458)` master root. `anchor.x` is always 0.5 because every master is already centered on its canvas — **do not** derive anchorX from a bottom-band centroid (that heuristic breaks on rosette morphology, see spec §7.1).
- `masterCanvas` is 512x512 for the whole atlas.

This atlas replaces `core_crops_v01` + `herb_crops_v01`, which were deleted from the repo. An atlas is a **build product of the masters, never hand-edited** — rebuild it with:

```bash
python3 tools/build_atlas.py --atlas farm_crops_v01   # add --dry-run to preview
```

Run `python3 tools/build_atlas.py` with no arguments to rebuild all four atlases (`farm_crops_v01`, `farm_trees_v01`, `farm_aquatic_v01`, `farm_soil_v01`). The script is idempotent: two runs produce byte-identical output.

## Artwork and production pipeline

Phase 2 historically used a deterministic Pillow workflow. That historical implementation is documented only as Phase 2 provenance and does not define the authoring method for Phase 3 or later painted asset packs.

Phase 3 source art is actual generated painted bitmap artwork created with the built-in imagegen system. Pillow, sips, ImageMagick, and similar raster tools are permitted only for non-art-authoring production work such as proportional downsampling, atlas packing, metadata/alpha inspection, contact sheets, and QC. They must not paint, synthesize, add, or reshape plant artwork.

## Acceptance criteria

Each pack is locked when all fifteen frames: (1) remain distinguishable at gameplay size, (2) sit plausibly on the shared farm footprint, (3) preserve coherent progression and relative crop scale, and (4) keep harvestable states readable without glossy or neon treatment.
