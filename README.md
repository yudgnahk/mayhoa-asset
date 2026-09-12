# Mayhoa Asset

**Language:** [Tiếng Việt](README.vi.md) · English

**Project:** Mayhoa — art production repo for the Farm system
**Art style:** Mayhoa Nostalgic Hand-Painted Farm Sprite
**Documentation language:** Fully bilingual — every document has both a `.vi.md` and an `.en.md` version. Vietnamese is the original, English is a translation kept in sync; when the two versions disagree, the `.vi` version wins.

This repo is where the artwork (master art + runtime atlases) for the Mayhoa game is produced: art style, generation plans, geometry/anchors and every master PNG file live here. This repo does **not** decide gameplay — scope, crop roster, demo gates and play mechanics all belong to the twin repo `mayhoa` (product/docs). Per decision **D-012** in `mayhoa`, that repo only records (a) which states the game needs assets to represent and (b) the integration contract the demo must follow; every decision about art direction, prompt generation, master artwork, geometry normalization and atlas packing belongs to this repo. The game is currently in its **Farm-only phase** — only the D-008 crop roster (rice, corn, carrot) and the minimal soil/pest/tool system of Gate A are gameplay-relevant right now; other species (fruit trees, aquatic crops) are out of Farm V1 scope even though the artwork already exists.

---

## 1. Documents at the root

| Document | Purpose | Status |
|---|---|---|
| `FARM_ASSET_GENERATION_PLAN.en.md` | Production roadmap: asset taxonomy, growth-stage system, size system, 12 production phases and their execution order | Active for taxonomy/roadmap/phase order; the specific canvas/anchor tables (§5) have been superseded by the geometry spec — see the header inside the file |
| `MAYHOA_ART_STYLE_SPEC.en.md` | Canonical art style spec (silhouette, outline, color, shading, prompting rules) for every asset | Canonical, active |
| `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.en.md` | Single source of truth for canvas size, anchors, scale progression, alpha/geometry QC | **Canonical, highest precedence** whenever there is a geometry conflict with any other document (including the plan/style spec) |
| `ASSET_GEOMETRY_FIX_CHECKLIST.en.md` | Execution record of the `masters/` geometry normalization (2026-08-26) + the re-QC round over all 19 packs (2026-09-05, section 9) | Runtime metadata is done; 7 items remain pending, mostly the regeneration queue plus 2 items that need game code — see section 9.7 |
| `FARM_REGENERATION_PROMPTS.en.md` | Concrete prompts for the regeneration round: carrot stage-05, the whole tonkin-jasmine pack, lotus stage-05, 6 fruit trees | Active. `soil_tilled` has been generated (`v02`, 2026-09-05); the other 4 items are pending |
| `FARM_MISSING_ASSET_PLAN.en.md` | Inventory of the assets still missing before Gate A / Gate B can run, with generation-ready specs for pest, tool, farm scene, plot overlay, FX and icons | **Active — read before starting the next batch.** Supersedes the §17 phase order until Gate A passes |
| `TASK_STATE.en.md` | State handoff between sessions: where we are, what is left, which pitfalls have already been paid for | Active — read it before starting any work |
| `FARM_REMAINING_PLANT_ASSET_PLAN.en.md` | Task breakdown for generating the 7 missing tree/aquatic species (coconut, dragon-fruit, coffee, rubber, lotus, water-mimosa, water-spinach) across several parallel sub-agents | Production is in fact complete (`masters/` has all 5/5 files per species) — the detailed checklist inside the file is not fully ticked, see the header inside the file |

The repo keeps a **fully bilingual** doc set: every document has both a `.vi.md` and an `.en.md` version. The README is the exception in naming only: `README.md` is the English version (that is what GitHub shows outsiders on the repo page) and `README.vi.md` is the Vietnamese one. **Vietnamese is the original** — content is written in Vietnamese first, and the English version is a translation kept in sync. **When the two versions disagree, the `.vi` version wins.** When you edit a document you **must edit both versions in the same commit**, otherwise the two will drift apart.

---

## 2. Current production status

**Complete** — 107 master PNGs, all 5 growth stages per species (except soil, which has no stages):

- **Soil** — 6 states (`empty`, `tilled`, `wet`, `planted`, `dry`, `harvested`), all RGBA8. `soil_tilled_v01.png` has permanently corrupted IDAT data and **has been replaced by `soil_tilled_v02.png`** (2026-09-05); the `v01` file is still in the repo for historical comparison, do not use it.
- **Field crops** (6 species × 5 stages) — rice, corn, carrot, tonkin-jasmine (Vietnamese: thiên lý), culantro (Vietnamese: ngò gai), mint.
- **Fruit/perennial trees** (11 species × 5 stages) — mango, pomelo, lemon, star-apple, rambutan, lychee, coconut, dragon-fruit, coffee, rubber, durian.
  `durian` (2026-09-09) landed un-normalized and failed geometry 5/5; it was **fixed on 2026-09-10** by a per-stage rescale and is now in the atlas — see `ASSET_GEOMETRY_FIX_CHECKLIST.en.md` section 10.
- **Aquatic crops** (3 species × 5 stages) — lotus, water-mimosa, water-spinach.

**Not done yet:**

- **Weeds** — not generated (Phase 9 of the generation plan).
- **Pests** — not generated (Phase 10).
- **Tools** — not generated (Phase 11).

**Waiting on regeneration** (see `FARM_REGENERATION_PROMPTS.en.md`). Polish items: `carrot` stage-05, the entire `tonkin-jasmine` pack (switching to a trellis-climbing form), `lotus` stage-05, and all 6 fruit tree packs (their silhouettes do not yet tell the species apart clearly).
Genuinely **broken, not polish**: `durian` stage-05 has its fruit buried in the canopy (an artwork content defect a rescale cannot reach). The Profile A band problem on durian stages 01/02/03 was **fixed on 2026-09-10** and needs no regenerate.

> ### ⚠️ Important note — `C-ART-02`
>
> Gate A of the playable demo (`mayhoa` repo) **needs at least one pest and one tool UI** to complete the gameplay loop. But under the current execution order in `FARM_ASSET_GENERATION_PLAN.en.md` §17, pests (Phase 10) and tools (Phase 11) are scheduled **last**, after even the tree/aquatic packs (Phases 4–8) that Farm V1 does not use yet. This conflict is tracked by the `mayhoa` repo under the code **`C-ART-02`** (`docs/research/CONTRADICTIONS.md`), currently **OPEN**. Anyone changing the production order should know about it before prioritizing more new tree/aquatic species.

---

## 3. Locked geometry contract (summary)

The table below is extracted from `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.en.md` — see that file for the full audit/QC. This is also the contract the `mayhoa` repo reads (see `FARM-CONTENT.md` §1 over there); **neither side may change these numbers alone.**

| Property | Value |
|---|---|
| Runtime atlas cell | `192×192` px @1x (crops / aquatic / soil); `256×256` for trees |
| Crop master canvas | `512×512`, transparent |
| Crop placement anchor | `(0.5, 0.89453125)` — the ground-contact point of the plant base, not the canopy center |
| Tree master canvas | `1024×1024` |
| Tree placement anchor | `(0.5, 0.947265625)` |
| Pin point on the tile (plant attachment point) | soil plate center, `(0.5, 0.508)` in soil-cell coordinates |
| Growth stages | 5 stages / species |

**The crop anchor changed on 2026-08-26**, from `(0.5, 0.684)` to `(0.5, 0.89453125)`. Any code or runtime metadata still using the old value will make crops "float" above the soil tile instead of standing at the center of the plate.

---

## 4. Runtime atlases

Atlases are a **build product**, generated from `masters/` by `tools/build_atlas.py`. Edit the masters and re-run the script — **do not hand-edit an atlas**.

```bash
python3 tools/build_atlas.py --dry-run   # show the plan, write no files
python3 tools/build_atlas.py             # rebuild all 4 atlases
```

| Atlas | Contents | Size | Cell |
|---|---|---|---|
| `farm_crops_v01` | 6 species × 5 stages | 960×1152 | 192 |
| `farm_trees_v01` | 11 species × 5 stages (includes `durian` since 2026-09-10) | 1280×2816 | 256 |
| `farm_aquatic_v01` | 3 species × 5 stages | 960×576 | 192 |
| `farm_soil_v01` | 6 tiles | 576×384 | 192 |

The JSON lives at `runtime/<atlas>.json`, the PNG at `runtime/1x/farm/<class>/<atlas>.png`.

Schema contract for game code:

- **The frame key is a slot id**: `<species>_stage-0N` (for example `coffee_stage-05`), carrying no semantic label. The reason: stage labels differ between species (`coffee` ends with `berry`, `rubber` with `tapping`, the rest with `fruiting`), so if the key carried the label the game would need a lookup table just to build the key. Soil is the exception, where the key is the full stem (`soil_dry`).
- `stageOrder` is always `["stage-01".."stage-05"]`; the semantic part lives in `stageNames` and is for display only.
- **`anchor.x` is always `0.5`**. Do not measure it with a bottom-band centroid — that heuristic is wrong for rosette morphology (spec §7.1) and once threw `culantro` off by up to 37px between stages.
- `anchor.y` is measured per file. It is not uniform in `farm_aquatic_v01` (lotus canvas 1024, water-* canvas 768) or in `farm_soil_v01` — read it per frame, do not use the shared `placementAnchor`.
- `masterCanvasBySpecies` is present when an atlas mixes several canvas sizes, so the game can compensate the display scale per spec §9.5.

Details: spec §11.1 (naming) and §13.2 (schema).
