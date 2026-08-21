# Phase 2 Core Crops and Phase 3 Herb / Low Crop Pack

**Status:** Canonical Phase 2 and Phase 3 crop growth reference<br>
**Project:** Mayhoa<br>
**Art style:** Mayhoa Nostalgic Hand-Painted Farm Sprite

This folder contains the Phase 2 growth-stage masters for rice, corn, and carrot, plus the Phase 3 herb / low crop masters for thien-ly, ngo-gai, and mint. Each crop uses five structurally distinct growth silhouettes rather than scaling one drawing.

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

- `thien-ly/` — Telosma cordata; seeded emergence -> tiny vine sprout -> young leafy vine -> fuller heart/ovate-leaf vine -> restrained pale yellow-green flower clusters at harvest.
- `ngo-gai/` — Eryngium foetidum (culantro); emergence -> tiny basal rosette -> widening young rosette -> dense mature rosette -> lush harvestable rosette with long, narrow, serrated-looking leaves. It is not coriander/cilantro foliage.
- `mint/` — paired oval-to-lanceolate textured leaves -> branching stems -> increasingly dense, lush mint clump, with characteristic leaf-edge and texture cues kept readable at gameplay scale.

## Locked production rules

- transparent 512x512 master canvas;
- common placement anchor around `(0.5, 0.684)`;
- visual base aligns to the Phase 1 soil footprint;
- upper-left lighting, soft contact shadow, selective dark-chromatic outlines;
- no baked soil, weeds, pests, UI, text, or scene background;
- stage progression changes silhouette, density, and focal cues;
- species identity must remain readable at 192px runtime-cell size.

## Runtime atlases

`runtime/1x/farm/crops/core_crops_v01.png` is a 960x576 shared-texture atlas with 192x192 cells. `runtime/core_crops_v01.json` stores frame coordinates and the shared placement anchor. Rows are rice, corn, carrot. Columns follow the five-stage order above.

`runtime/1x/farm/crops/herb_crops_v01.png` is the equivalent Phase 3 960x576 atlas. `runtime/herb_crops_v01.json` stores its frame coordinates and shared placement anchor. Rows are thien-ly, ngo-gai, mint; columns follow the same five-stage order.

## Artwork and production pipeline

Phase 2 historically used a deterministic Pillow workflow. That historical implementation is documented only as Phase 2 provenance and does not define the authoring method for Phase 3 or later painted asset packs.

Phase 3 source art is actual generated painted bitmap artwork created with the built-in imagegen system. Pillow, sips, ImageMagick, and similar raster tools are permitted only for non-art-authoring production work such as proportional downsampling, atlas packing, metadata/alpha inspection, contact sheets, and QC. They must not paint, synthesize, add, or reshape plant artwork.

## Acceptance criteria

Each pack is locked when all fifteen frames: (1) remain distinguishable at gameplay size, (2) sit plausibly on the shared farm footprint, (3) preserve coherent progression and relative crop scale, and (4) keep harvestable states readable without glossy or neon treatment.
