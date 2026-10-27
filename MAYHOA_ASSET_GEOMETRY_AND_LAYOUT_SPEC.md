# Mayhoa — Asset Geometry, Anchor & Layout Spec

**Language:** [Tiếng Việt](MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.md) · English

**Status:** Canonical geometry/layout contract for asset audit and production  
**Project:** Mayhoa  
**Scope:** Master assets, multi-stage assets, runtime anchor metadata, normalization/QC  
**Related specs:** `MAYHOA_ART_STYLE_SPEC.md`, `FARM_ASSET_GENERATION_PLAN.md`, `FARM_REMAINING_PLANT_ASSET_PLAN.md`, `ASSET_GEOMETRY_FIX_CHECKLIST.md`

---

## Status and relationship to other documents

This is the **active geometry document with the highest precedence** in the repo (see the precedence order this file itself defines in §18: this geometry spec > species-specific lifecycle spec > `FARM_ASSET_GENERATION_PLAN.md` > `MAYHOA_ART_STYLE_SPEC.md` > existing runtime JSON/README).

This document complements (does not replace) `MAYHOA_ART_STYLE_SPEC.md` (which only governs visual style, not geometry) and `FARM_ASSET_GENERATION_PLAN.md` (roadmap/taxonomy/phase order, not the source of exact canvas/anchor numbers). The actual application of the numbers here to the existing `masters/` is recorded in `ASSET_GEOMETRY_FIX_CHECKLIST.md` (executed 2026-08-26); §20 of this very file contains the measured baseline and the post-normalize results.

---

## 1. Purpose

This document locks the shared geometry rules used for Mayhoa assets so that:

- every asset of the same type has a consistent canvas and gameplay anchor;
- lifecycle stages are not centered individually by bounding box;
- stage-transition animation does not jump origin / jump position;
- master assets and runtime sprites use the same semantic anchor;
- normalizing assets via raster transforms does not change the artwork;
- there is a single checklist for re-auditing the whole asset set in a later session.

This document **does not replace the art-style spec**. It is only the source of truth for:

- canvas;
- anchor coordinates;
- scale/progression;
- transparent padding;
- placement geometry;
- normalization;
- geometry QC.

---

## 2. The most important principles

### 2.1 The gameplay anchor matters more than the visual center

For assets with a clear gameplay contact point, **do not center the asset by bounding box**.

The fixed point must be the semantic anchor:

- tree / perennial: the point where the trunk base contacts the ground;
- crop / herb: the footprint point placed on the soil;
- aquatic crop: root/base or waterline anchor per the pack's spec;
- animal standing on ground: foot/contact anchor;
- object placed on a surface: contact/base anchor;
- only assets with no clear contact point may use an appropriate visual-center/pivot.

The `object centered` rule in the art-style spec is only a preference for isolated composition. For assets with a gameplay anchor, **this geometry spec takes precedence**.

### 2.2 One lifecycle pack must use one single anchor

If a species has multiple stages:

- all stages use the same canvas;
- the same absolute anchor coordinate within the master canvas;
- do not compute a per-stage anchor at runtime to hide master errors;
- the tree/crop must grow out of that fixed anchor.

Runtime may store a normalized anchor, but the master artwork must still be aligned correctly first.

### 2.3 Do not normalize by aligning tops

For tree/crop growth:

- the top of the foliage must be allowed to change with growth;
- the bottom/root/contact point is the locked point;
- if the tops of all stages are equal but the roots differ, the asset **FAILS**.

---

## 3. Standard coordinate system

Master rasters use the conventional image coordinate system:

```text
(0,0) --------------------> +X
  |
  |
  |
  v
 +Y
```

- `(0,0)` at the top-left corner;
- X increases to the right;
- Y increases downward;
- pixel coordinates are understood in terms of the master canvas;
- when we say `root=(x,y)`, this is a coordinate on the raw PNG master, not a coordinate after PixiJS applies its own anchor compensation.

### 3.1 Absolute anchor and normalized anchor

Master QC uses absolute pixel coordinates:

```text
anchor_px = (x, y)
```

Runtime metadata should use normalized coordinates:

```text
anchor_norm = (x / canvas_width, y / canvas_height)
```

Example, a 1024×1024 tree master with root `(512,970)`:

```text
anchor_px   = (512, 970)
anchor_norm = (0.5, 0.947265625)
```

Do not round the master anchor during QC. Runtime may serialize floats with sufficiently high precision.

---

## 4. Master canvas by asset class

Current targets from the production plan:

| Asset class | Master canvas target | Notes |
|---|---:|---|
| Small crop / weed / pest | `512×512` | the current crop pack mostly uses 512 |
| Medium crop / herb | `768×768` new target | old 512 packs must be audited before migrating |
| Aquatic crop | `768×768` | lotus LOCKED `1024×1024` — see §5.4 |
| Normal tree / perennial / animal-sized farm asset | `1024×1024` | canonical for fruit tree / coffee; default master target |
| Tall / special tree | `1024×1280` only if truly needed | all stages of a species must share one canvas; coconut is settled as NOT using it — see §5.2 |
| Tool / small isolated icon | `512×512` | anchor depends on semantics |
| Large hero asset | `1536+` only when explicit | not used directly as runtime |

### 4.1 Do not mix canvases within one lifecycle

Example of what is not allowed:

```text
stage-01 = 1024×1024
stage-02 = 1024×1024
stage-03 = 1254×1254
stage-04 = 1024×1024
stage-05 = 1024×1024
```

If you normalize, normalize the whole pack to one canonical canvas.

### 4.2 Generator output is not the canonical canvas

Actual measurements (2026-08-26) show the generation pipeline frequently outputs:

- `1122×1402` — mango, pomelo, lemon, star-apple;
- `1254×1254` — lychee, rambutan, coconut, lotus.

None of the sizes above are canonical. Every newly generated pack must be resampled + aligned to the canonical canvas/anchor before it counts as a finished master. Do not lock the spec to whatever size the generator happened to emit.

---

## 5. Canonical anchor by asset class

### 5.1 Normal tree / perennial — LOCKED

Canvas:

```text
1024×1024
```

Canonical root/contact anchor:

```text
root_px   = (512, 970)
root_norm = (0.5, 0.947265625)
```

Meaning:

- X sits at the middle of the gameplay footprint;
- Y is the lowest/root contact point;
- there is still `53 px` of transparent padding below the root (`1023 - 970 = 53`);
- foliage/canopy grows upward and outward to both sides;
- do not move the root to center the canopy.

Coffee was used as the calibration for this anchor and must be re-audited together with the whole tree pack in the next session.

The species in `FARM_REMAINING_PLANT_ASSET_PLAN.md` use this contract by default if they keep the `1024×1024` canvas:

- `coffee`;
- `dragon-fruit` if it supports a post/trellis and the whole plant envelope still fits safely in the square master;
- `rubber` if it does not need a tall canvas after the cross-species audit.

`dragon-fruit` is a **special-structure plant**: the root/base anchor of the plant + support system must be fixed, but the fixed height of the support post **must not be used as a growth metric** for the plant.

Measured status 2026-08-26 — `dragon-fruit`: the pack is internally consistent (root ≈ `(500.5, 987.5)`, delta ≤ 1 px) but off the canonical anchor by `(-11.5, +17.5)`. The visible height of stage-03 is 962 px, so it **cannot be translated directly** to `(512, 970)` without breaking the 24 px top margin; the whole pack must be scaled `×0.98` around the root and then translated (see the fix checklist).

### 5.2 Tall / special tree — PROVISIONAL

If the `1024×1280` canvas is truly used, keep the same 53 px bottom padding logic:

```text
root_px = (512, 1226)
```

That is:

```text
root_y = canvas_height - 54
```

This is a provisional rule until the rubber/tall-tree audit is complete.

Remaining candidates for a tall/special canvas:

- `rubber` — may need a tall canvas if the mature/tapping stage exceeds the safe envelope of `1024×1024`.

`coconut` has been measured (2026-08-26) and is **settled on the square `1024×1024`, root `(512, 970)`**. The current pack is `1254×1254`, contactY = 1236 (Δ0), rootX ≈ 646 (Δ1.1 px) — internally consistent but on the wrong canvas, with only 17 px of bottom padding and only 6 px of top margin left on stage-05. Resampling the whole pack `×0.768` to 1024 gives stage-05 a visible height of ≈ 946 px — still the tallest member of the remaining tree pack, and no tall canvas is needed.

Do not move a species to `1024×1280` automatically just because the current artwork is tall. Only use a tall canvas if, after the cross-species audit, the relative world scale is sensible but the square master no longer leaves enough safe margin.

### 5.3 Crop / herb — LOCKED (bottom-anchor, 2026-08-26)

Legacy Phase 2/3 (SUPERSEDED, kept as history):

```text
master_canvas ≈ 512×512
placement_anchor_norm ≈ (0.5, 0.684)
placement_anchor_px   ≈ (256, 350)
```

This legacy reference used to exist in:

- `masters/farm/crops/README.md` — updated;
- `runtime/core_crops_v01.json` — the atlas has been deleted (2026-09-07);
- `runtime/herb_crops_v01.json` — the atlas has been deleted (2026-09-07).

Both atlases above have been merged into `runtime/farm_crops_v01.json` (see §13.2).

**Final contract (rev 2, same day): a crop is an independent bottom-anchor sprite, like a tree.**

How it was settled: (1) the reading that "crops do not need the same contactY" was wrong — the base of the larger crop stages stuck out below the soil plate; (2) the base-align option at `(256, 350)` was wrong too — that point is the **front edge** of the plate (the plate occupies y 157–360), whereas the calibration sheet shows the plant must stand at the **center of the plate**; and if we kept the 1:1 per-tile bake style, a base at the plate center would leave only ~236 px of height — not enough for class M. Therefore:

- a crop is an independent sprite, bottom-anchored under the same philosophy as a tree;
- canvas `512×512`, root `(256, 458)` = `(0.5, 0.89453125)` — 54 px of bottom padding, the same convention as trees;
- contactY = 458, Δ0 across all 5 stages; max visible height = `458 − 24 = 434 px`;
- the engine pins the crop root to the **tile plant point = the soil plate center `(256, 260)` ≈ `(0.5, 0.508)`** in the 512 soil-tile coordinate system;
- X align: single-stem/clump forms (rice, corn, carrot) use the bottom-band centroid; rosette/bush forms (culantro, tonkin-jasmine, mint) use the **bbox center** (§7.1);
- QC requires a composite check onto the soil tile: the plant base sits at the plate center and does not stick out below the plate.

`placementAnchor` changed from `(0.5, 0.684)` → `(0.5, 0.89453125)`. Since 2026-09-07 this value lives in `runtime/farm_crops_v01.json` (written rounded to 6 digits: `(0.5, 0.894531)`), replacing the deleted `core_crops_v01.json` / `herb_crops_v01.json`. **The game code that reads this anchor needs to be re-checked for the pin point on the tile (the plate center).**

A later audit session must verify:

- whether the raw PNGs really share the same footprint/contact anchor;
- whether the runtime metadata actually reflects the real master;
- whether the Phase 2/3 512 canvas remains canonical or migrates to the 768 target for medium crops.

### 5.4 Aquatic crop — LOTUS LOCKED; the remaining species MUST AUDIT

Default master:

```text
768×768
```

Lotus may use:

```text
1024×1024
```

The semantic anchor must be one of:

- a common root/base point;
- a common waterline point;
- or a clearly documented pack-specific gameplay anchor.

All 5 stages of the same aquatic species must use the **exact same anchor**.

Do not lock a shared pixel coordinate for all aquatic assets before the audit, because lotus, water mimosa and water spinach have different water-surface structures.

Required semantic anchors for the three remaining species:

| Species | Canvas target | Canonical anchor semantic | Main growth direction |
|---|---:|---|---|
| `lotus` | `768×768`, may be `1024×1024` | the common root/base or common waterline point chosen for the whole pack | upward + radial leaf spread |
| `water-mimosa` | `768×768` | common waterline/root placement point | horizontal spread |
| `water-spinach` | `768×768` | common waterline/root placement point | horizontal spread |

Important aquatic rules:

- the three species are not required to use the same **pixel coordinate** before the audit;
- but each species must have one single exact anchor across all 5 stages;
- once Wave B audit is done, a shared aquatic placement convention should be locked if the neutral water tile allows it;
- do not bake the water surface/ripple/pond edge into the master to "fake" waterline alignment.

Measured status 2026-08-26 — `lotus` (now LOCKED):

- the current pack is `1254×1254` (wrong canvas policy);
- contactY = 1185–1187 (Δ2 px, acceptable);
- bottom-band rootX swings between 585–647 — mostly because the heuristic does not suit radial morphology (see §7.1), so it must be aligned manually;
- spread progression 0.25 / 0.64 / 0.81 / 0.95 — close to Profile D.

Decision: lotus is **LOCKED at `1024×1024`, anchor `(512, 970)`**, following the same bottom-padding convention as trees. Resample `×0.835` + align the root manually per stage. `water-mimosa` / `water-spinach` are **LOCKED at `768×768`, anchor `(384, 728)`** — where `728 = round(768 × 970/1024)`, matching the bottom-padding convention ratio of tree/lotus. X align uses the **bbox center** (Profile E), **not** the bottom-band centroid.

Measured status 2026-09-05 — both aquatic horizontal packs are **fully normalized and conformant**: canvas `768×768` uniform across 5/5 stages, RGBA8, contactY = 728 (Δ0), bbox center X = 383.0–384.5 (canvas center 383.5, Δ ≤ 1.5 px), L/R margins symmetric within 1–2 px. Per-stage measurements are in Appendix B of `ASSET_GEOMETRY_FIX_CHECKLIST.md`.

> **WARNING — DO NOT re-normalize `water-mimosa` / `water-spinach`.**
> These two packs are already conformant. Running `tools/normalize_pack.py` on them **without a `--rootx` override** will make the bottom-band heuristic **destroy the currently correct alignment**: the bottom-band rootX of `water-mimosa` spans `376.9–474.0` (Δ 97 px) because of aquatic-horizontal morphology, so the script would shift stage s02 by roughly **−90 px**. This is exactly the heuristic-failure case described in §7.1, which names `water-mimosa`. The bottom-band `rootX` of these 2 packs is **reference only**, not a PASS/FAIL number — the PASS/FAIL number is the bbox center X.

### 5.5 Animal / fish / dragon / object

Do not force every asset to use the tree root.

The anchor must follow semantic placement:

- land animal: foot/base contact;
- fish: a gameplay pivot suited to swimming/rotation;
- dragon/flying asset: pivot based on body mass / animation rig contract;
- tool/icon: visual pivot if there is no world-contact semantic.

When a class is productionized into a pack, the exact canonical anchor for that class must be added to this doc.

---

## 6. Transparent background and alpha contract

Every isolated master sprite must have:

- a genuinely transparent background;
- no black/white matte;
- no scene background;
- no UI/text/watermark;
- no baked-in soil/ground tile/pond edge/pond surface unless the asset spec explicitly requires it;
- no baked-in decorative clutter that is not part of the object.

### 6.1 Alpha threshold used for geometry QC

To keep anti-alias fringing from affecting the bbox, geometry QC should use:

```text
alpha >= 24 / 255
```

This is the threshold compatible with the current playground logic.

QC must state the threshold explicitly if a different value is used.

### 6.2 Opaque bounding box

With the `alpha >= 24` threshold, measure:

```text
minX, minY, maxX, maxY
visibleWidth  = maxX - minX + 1
visibleHeight = maxY - minY + 1
```

For a grounded asset:

```text
contactY = maxY
```

The `contactY` of every stage in the same pack must be identical after normalization (crops: contactY = 458 — see §5.3).

### 6.3 Master PNG format

- The master must be RGBA8 (PNG colortype 6).
- Do not use palette/quantized PNG (colortype 3) as a master; quantization is only allowed for runtime assets.
- Known issue, now closed (2026-08-26): `rice`, `corn`, `carrot` used to be palette PNGs; all three became RGBA8 after the crop base-align pass. Every new pack is required to be RGBA8.

---

## 7. Root X must be measured from the base/contact band, not from the canopy

Do not use the center of the whole opaque bounding box to infer root X.

For tree/perennial:

1. measure the visible height;
2. take a bottom band of about `2–3%` of the visible height, at minimum roughly `6–20 px` depending on master size;
3. only consider alpha pixels above threshold within the bottom band;
4. derive the center/centroid of the trunk/root contact area;
5. align root X to the canonical X.

The goal is to align the **base of the trunk**, not to align the canopy.

Failure examples to avoid:

- canopy leans left -> bbox center leans left -> the script shifts the whole tree -> the root ends up off;
- canopy widens with each stage -> bbox center changes -> the animation jumps horizontally.

### 7.1 Limits of the bottom-band heuristic

The bottom-band centroid is only reliable for single-stem morphology (tree / palm / column). For radial / rosette / multi-stem morphology (lotus, culantro, water-mimosa, ...), the centroid of the bottom band swings widely with the foliage — measured Δ 62–125 px even though the artwork is not necessarily mispositioned. For these species:

- do not use the bottom-band centroid as an automatic PASS/FAIL number;
- set the anchor manually (visually) or use a higher band around the base cluster;
- state the measurement method explicitly in the audit report;
- **do not re-run normalization with this heuristic on a pack already aligned by bbox center** — `water-mimosa` / `water-spinach` are the concrete case, see the warning in §5.4.

---

## 8. Safe padding / breathing room

### 8.1 General rule

The artwork must not touch the canvas edge at the alpha QC threshold.

Recommended opaque safe margin:

```text
>= 24 px minimum
>= 32 px preferred
```

for the left/right/top edges on a 1024 master where morphology allows.

### 8.2 Grounded tree bottom padding

A normal 1024 tree uses root `y=970`, so there is 53 px of transparent area below the contact point.

Do not push the tree all the way down to row 1023 just to use up the canvas.

### 8.3 Do not crop to force a fit if artwork is lost

If a mature stage exceeds the canvas:

prioritize in this order:

1. shrink the whole species pack by a sensible relative scale;
2. choose a tall/special canvas if the spec allows it;
3. regenerate if the morphology is wrong;
4. do not crop leaf/fruit/branch just to pass the size check.

---

## 9. Scale and lifecycle progression

### 9.0 Core rule — same stage does not mean same absolute height

Species at the same `stage-03`, `stage-04`, `stage-05` are **not required to have the same pixel height**.

The same stage only means an equivalent maturity/lifecycle level within that species.

Examples:

- coffee stage 05 must still be shorter/more compact than coconut stage 05;
- water-mimosa stage 05 may not be much taller than stage 04, but it must spread/be denser;
- dragon-fruit has a fixed support post, so its full bbox height may be nearly unchanged across some stages while the plant mass still develops clearly.

Geometry audits must therefore separate two concepts:

```text
within-species progression = the stage growth logic of the species itself
cross-species world scale  = sensible relative size between species
```

Do not normalize all species to the same stage height just to make the number table look even.

### 9.1 Dominant growth metric

Every species must have a clear `dominantGrowthMetric`. The 5-stage progression must increase along a metric that suits the morphology; it is not necessarily always height.

Usable metrics:

- `visibleHeight` — tree/palm/trunk-driven plant;
- `canopySpread` — crown/canopy development;
- `plantEnvelope` — plant-only envelope when there is a fixed support;
- `horizontalSpread` — aquatic/vine/creeping form;
- `density` — stem/leaf mass;
- `structuralComplexity` — branch/segment/stem count;
- a composite metric if a species needs several signals.

The general lifecycle relation is still:

```text
stage-01 < stage-02 < stage-03 < stage-04 < stage-05
```

but the `<` applies to the **dominant growth metric / perceived maturity**, not to forcing every bbox dimension to increase.

### 9.2 Do not merely scale one piece of artwork

Stages must change real structure.

Raster scaling may only be used to **normalize relative size after generation**; it must not be used to fake a lifecycle by scaling a single image into 5 stages.

### 9.3 Stage 05 must not regress relative to stage 04

Stage 05 must not regress in perceived maturity relative to stage 04.

For vertical trees/palms:

- stage 05 should not be shorter/smaller than stage 04 without a species-specific reason;
- stage 05 may be scaled slightly if the artwork/morphology remains correct and nothing is cropped;
- if scaling is not enough, regenerate.

For horizontal aquatic plants:

- stage 05 is not required to be taller than stage 04;
- but horizontal spread, density, or harvestable plant mass must be equal to or greater than stage 04.

For support-structure plants such as dragon-fruit:

- the support post may stay unchanged;
- plant coverage/branching/segment mass around the support must increase;
- do not use the fixed support height to conclude that the progression PASSes.

### 9.4 Recommended progression ratio profiles

The ratios below are **audit/calibration bands**, not a reason to break morphology. Ratios are measured on the dominant growth metric and normalized against stage 05 of **that same species**:

```text
stageRatio = dominantMetric(stage) / dominantMetric(stage-05)
```

#### Profile A — vertical tree / shrub

Used for: `coffee`, `rubber` and major fruit trees where appropriate.

| Stage | Recommended ratio |
|---|---:|
| 01 | `0.35–0.45` |
| 02 | `0.55–0.65` |
| 03 | `0.75–0.88` |
| 04 | `0.90–0.98` |
| 05 | `1.00` |

The stage-03 band was widened to `0.88` (2026-08-26) because coffee — the calibration species — measured `0.867`.

#### Profile B — palm / strong vertical special tree

Used for: `coconut`.

| Stage | Recommended ratio |
|---|---:|
| 01 | `0.25–0.35` |
| 02 | `0.40–0.55` |
| 03 | `0.65–0.78` |
| 04 | `0.88–0.96` |
| 05 | `1.00` |

This profile allows an early coconut to be clearly small before the mature palm trunk/crown forms.

#### Profile C — support-structure plant

Used for: `dragon-fruit`.

Measure the **plant envelope / coverage**, excluding the fixed post/trellis height from the main metric.

| Stage | Recommended ratio |
|---|---:|
| 01 | `0.20–0.35` |
| 02 | `0.40–0.55` |
| 03 | `0.65–0.80` |
| 04 | `0.88–0.96` |
| 05 | `1.00` |

#### Profile D — aquatic upright/radial

Used for: `lotus`.

The main metric is a composite of:

- leaf/stem structure;
- radial spread;
- vertical flower/bud envelope where the lifecycle allows.

Recommended maturity ratio:

| Stage | Recommended ratio |
|---|---:|
| 01 | `0.25–0.40` |
| 02 | `0.45–0.65` |
| 03 | `0.65–0.82` |
| 04 | `0.85–0.95` |
| 05 | `1.00` |

The stage 02/03 bands were widened slightly (2026-08-26) to match the measured spread of the current lotus (`0.64 / 0.81`).

Do not use stage-05 flower height as the only metric, as that would misjudge leaf-spread progression.

#### Profile E — aquatic horizontal spread

Used for: `water-mimosa`, `water-spinach`.

Main metric:

```text
horizontalSpread + stem/leaf density
```

Recommended spread ratio:

| Stage | Recommended ratio |
|---|---:|
| 01 | `0.25–0.35` |
| 02 | `0.45–0.60` |
| 03 | `0.65–0.80` |
| 04 | `0.85–0.95` |
| 05 | `1.00` |

Height may be nearly flat across stages 03–05 and still PASS if the spread/density progression is clear.

### 9.5 Relative scale between species

Current runtime semantic reference:

| Class | Suggested display size | Examples |
|---|---:|---|
| S | `64–96 px` | tiny stage, weed, pest, small tool |
| M | `128–160 px` | rice, carrot, herb, water-mimosa, water-spinach |
| L | `192–256 px` | corn, coffee, dragon-fruit, lotus |
| XL | `256–384 px` | mango, pomelo, coconut, rubber, major fruit tree |

Relative species scale is **canonical gameplay intent**. Lifecycle normalization must not force different species into the same pixel height.

Do not use master bbox size alone to conclude world scale; the semantic class and the runtime display target must be taken into account.

Clarification (2026-08-26): the master stage-05 target px (§9.7) is a target for **making use of the canvas resolution**, not a mechanism for enforcing world scale. Cross-species world scale is enforced solely by the runtime display size in the table above. Two species of different semantic classes may therefore both nearly fill their own master canvas.

Additional calibration (2026-08-26, after visual review):

- `corn` is the **only crop in class L** (per the table above) — display target ~224 px, and it must be clearly taller than rice; a corn master ≈ rice master is normal because both hit the canvas ceiling, the difference is in display scale;
- `lemon` is lowered to the **shortest fruit tree**, display target ~256 px (the L/XL boundary) — shorter than mango/pomelo/star-apple; a small citrus does not stand level with the large trees.

### 9.6 Remaining-plant geometry matrix — REQUIRED SUPPORT

Every species in `FARM_REMAINING_PLANT_ASSET_PLAN.md` must be audited against this matrix:

| Species | Geometry class | Canvas policy | Anchor policy | Size class | Progression profile | Dominant growth metric | Stage-05 scale policy |
|---|---|---|---|---|---|---|---|
| `coconut` | tall/special palm | `1024×1024` — LOCKED (measured 2026-08-26, no tall canvas needed) | fixed ground root `(512,970)` | XL | B | height + crown spread | tallest member of the remaining tree pack; stage-05 visH ≈ 946 px after `×0.768` resample |
| `dragon-fruit` | support-structure perennial | `1024×1024` preferred | fixed plant base + support anchor → `(512,970)`; the current pack is off, fix with `×0.98` + translate | L | C | plant envelope/coverage excluding fixed post | shorter than major fruit trees; do not normalize by post height |
| `coffee` | compact tree/shrub | `1024×1024` | fixed root `(512,970)` | L | A | visible height + canopy complexity | compact; must be shorter than major fruit trees/coconut/rubber at world scale |
| `durian` | tall fruit tree | `1024×1024` ✓ (per-stage rescale 2026-09-10, s01–s05 = 0.4713/0.4884/0.6394/0.7291/0.7733 from a `1254×1254` canvas) | fixed ground root `(512,970)`, contactY Δ0 ✓ | XL | A | height + tiered branch structure | tall; the pagoda branch tiers must stay open, fruit hangs in the gap below a tier — **s05 is still buried in the canopy, awaiting a regenerate** |
| `rubber` | tall industrial tree | `1024×1024` if it fits; `1024×1280` if needed | fixed ground root; the corresponding square/tall root contract | XL | A | height + trunk thickness | tall; larger than coffee, exact relation to coconut/major trees locked after the audit |
| `lotus` | aquatic upright/radial | `1024×1024` — LOCKED | fixed root `(512,970)`; manual align (radial morphology, §7.1) | L | D | radial spread + stem/leaf structure + final flower envelope | do not compare raw height directly with land trees |
| `water-mimosa` | aquatic horizontal | `768×768` — LOCKED | fixed waterline/root anchor `(384, 728)`; X align by bbox center (§5.4) | M | E | horizontal spread + density | low/wide; width progression matters more than height |
| `water-spinach` | aquatic horizontal | `768×768` — LOCKED | fixed waterline/root anchor `(384, 728)`; X align by bbox center (§5.4) | M | E | horizontal spread + density | low/wide; distinct silhouette from water-mimosa |

The `Stage-05 scale policy` in the table above is cross-species intent. The exact master-pixel target is only `LOCKED` after an audit session measures all references and picks a calibration set.

### 9.7 Stage-05 target height/dimension policy

After the audit, every species must have a record:

```text
semanticSizeClass: L | XL | M | ...
stage05TargetMetric: visibleHeight | horizontalSpread | plantEnvelope | composite
stage05TargetValuePx: <locked after audit>
stageRatios: [s1, s2, s3, s4, 1.0]
```

A single `stage05TargetValuePx` must not be used for all species.

If two species share a semantic class but have very different morphologies, they may use different target metrics. For example:

- coffee: visible height;
- dragon-fruit: plant envelope excluding support;
- lotus: radial/composite envelope;
- water-mimosa: horizontal spread.

---

## 10. Shared lifecycle semantics for plant/tree packs

If a species uses 5 stages:

- exactly 5 separate images;
- no contact sheet;
- no sprite sheet in place of masters;
- stage 01 is the smallest;
- stage 02 is early/sapling/sprout, with no harvest cue;
- stage 03 is young vegetative;
- stage 04 is mature/flowering where applicable;
- stage 05 is harvestable/final;
- the harvest focal point only appears at the correct lifecycle point;
- a species-specific spec may override stage names but must not override the shared-anchor rule.

Fruit tree/perennial default:

```text
stage-01_sprout
stage-02_sapling
stage-03_young
stage-04_flowering-or-mature
stage-05_harvestable
```

---

## 11. Naming and file contract

Master asset filenames must be deterministic:

```text
<species>_stage-<NN>_<semantic>_v<NN>.png
```

Example:

```text
coffee_stage-01_sprout_v01.png
coffee_stage-02_sapling_v01.png
coffee_stage-03_young_v01.png
coffee_stage-04_flowering_v01.png
coffee_stage-05_berry_v01.png
```

Directory:

```text
masters/<domain>/<asset-class>/<species>/
```

Do not change filenames just because the canvas/anchor was normalized, if the artwork version has not changed in semantics/art direction.

### 11.1 Runtime atlas — naming contract (settled 2026-09-07)

One atlas per asset class, not grouped by wave and not per-species:

```text
<domain>_<class>_v<NN>
```

Fixed output paths:

```text
runtime/<atlas>.json
runtime/1x/<domain>/<class>/<atlas>.png
```

Example: `farm_crops_v01` → `runtime/farm_crops_v01.json` + `runtime/1x/farm/crops/farm_crops_v01.png`.

The list of species/tiles in an atlas is **read from the filesystem and sorted alphabetically**, never hardcoded — adding a new master pack only requires a rebuild. For each tile/pack with multiple versions, the atlas takes the **highest readable version**; a higher version whose file is corrupt is skipped down with the reason recorded.

---

## 12. Normalization policy — allowed and not allowed

### 12.1 Allowed without redrawing

Permitted production transforms:

- translation on a transparent canvas;
- resize/downscale/slight upscale to normalize relative scale;
- canvas resize/pad/crop of transparent-only empty regions;
- alpha-aware bbox measurement;
- metadata/anchor correction;
- atlas packing;
- runtime downsampling.

### 12.2 Not considered normalization

The following changes are artwork edits/regeneration:

- drawing additional leaves/fruit/flowers;
- deleting a branch/object;
- repainting the trunk;
- compositing part of another stage in;
- procedural reconstruction;
- changing morphology through raster manipulation.

If these changes are needed, the artwork must be explicitly regenerated/edited.

### 12.3 Translation must be verified on the raw PNG

After every translation:

- re-measure the alpha bbox of the raw file;
- re-measure the contact/root band;
- do not just open the playground to check.

Playground/runtime code **must not apply per-stage anchor compensation to hide master errors** in QC mode.

---

## 13. Runtime anchor contract

The runtime anchor must reflect the semantic master anchor.

If a 1024 tree master has:

```text
root_px = (512,970)
```

the runtime normalized anchor must correspond to:

```text
(0.5, 0.947265625)
```

If the runtime atlas frame has trimmed/cropped the transparent padding, the anchor must be remapped from master-space to frame-space deterministically.

Do not copy an old runtime anchor for a new asset if the master geometry differs.

### 13.1 Legacy runtime metadata to audit — RESOLVED (kept as history)

> **Status 2026-09-07:** all the atlases mentioned in this section (`core_fruit_trees_v01/v02`,
> `core_crops_v01`, `herb_crops_v01`, `soil_states_v01`) **have been deleted from the repo** and replaced by
> 4 atlases generated with `tools/build_atlas.py` — see §13.2. The text below is kept as a
> historical record of the 2026-08-26 audit and does not describe the current state.

`runtime/core_fruit_trees_v01.json` had legacy metadata at the time such as:

```text
masterCanvas = 1122×1402
placementAnchor = (0.5, 0.88)
```

whereas the current generation plan uses a tree master target of `1024×1024`.

This metadata must therefore **not be treated as the new canonical geometry** until an audit session re-verifies the whole pipeline.

State of runtime metadata **as of 2026-08-26** (historical snapshot, superseded by §13.2):

- `core_fruit_trees_v01.json` — legacy `1122×1402` / anchor `(0.5, 0.88)`, covering mango/pomelo/lemon/star-apple; must be rebuilt as `v02` after the masters are normalized to `1024×1024` with anchor `(0.5, 0.947265625)`.
- `lychee`, `rambutan` — master `1254×1254`, **no runtime JSON yet**.
- `coffee`, `dragon-fruit`, `coconut`, `lotus` — **no runtime JSON yet**.
- `core_crops_v01.json`, `herb_crops_v01.json` — match the current 512 masters, keeping anchor `(0.5, 0.684)`.

### 13.2 Current runtime atlases — LOCKED (2026-09-07)

Atlases are no longer built by hand. `tools/build_atlas.py` generates all of them from `masters/`, has tests
(`tools/test_build_atlas.py`), is idempotent (running it twice produces byte-identical output), and writes nothing if the build fails.

```bash
python3 tools/build_atlas.py                        # rebuild all 4 atlases
python3 tools/build_atlas.py --atlas farm_soil_v01  # only 1 atlas
python3 tools/build_atlas.py --dry-run              # preview, write nothing
python3 tools/build_atlas.py --allow-mixed-canvas    # only when mixing canvases is deliberate
```

**Guards (2026-09-10).** The build fails and writes nothing — including under `--dry-run` —
when master canvases inside one atlas are not uniform, or when `anchorSpread.y` converted to
pixels inside the cell exceeds 2.0 px. Legitimate canvas mixing is declared via
`mixed_canvas_ok` in `ATLAS_SPECS` (`farm_aquatic_v01`: lotus 1024 vs water-* 768) or
`--allow-mixed-canvas`; a drifting anchor has no override because it is always a master
defect. See `ASSET_GEOMETRY_FIX_CHECKLIST.md` section 10.4.

**An atlas is a product generated from masters — do not edit it by hand.** If the numbers are wrong, fix the master or fix
the script and rebuild; do not patch the JSON.

| Atlas | Master source | Size | Cell | Contents | Replaces |
|---|---|---|---|---|---|
| `farm_crops_v01` | `masters/farm/crops/*/` | 960×1152 | 192 | 6 species × 5 stages | `core_crops_v01` + `herb_crops_v01` |
| `farm_trees_v01` | `masters/farm/trees/*/` | 1280×2816 | 256 | 11 species × 5 stages (`durian` joined the atlas on 2026-09-10, see checklist section 10) | `core_fruit_trees_v01` + `v02` |
| `farm_aquatic_v01` | `masters/farm/aquatic-crops/*/` | 960×576 | 192 | 3 species × 5 stages | *(never had an atlas)* |
| `farm_soil_v01` | `masters/farm/soil/*.png` | 576×384 | 192 | 6 tiles | `soil_states_v01` |

Paths: `runtime/<atlas>.json` + `runtime/1x/farm/<class>/<atlas>.png` (§11.1).

**Schema (different from the legacy version, the game code must re-read it):**

- **The frame key is the slot id** `<species>_stage-0N` — for example `coffee_stage-05`, `rubber_stage-05`. The key
  does **not** carry the semantic label, because stage labels differ across species (`coffee` → `berry`,
  `rubber` → `tapping`, the rest → `fruiting`); if the key carried the label, the game would need a lookup table just to
  construct the key. Soil is the exception: the key is the full stem (`soil_dry`, `soil_tilled`, ...).
- **`stageOrder`** is always `["stage-01","stage-02","stage-03","stage-04","stage-05"]`.
- **`stageNames`**: maps `<species> -> ["seeded","sprout",...]`, preserving the semantic part, **for display only**.
- **`anchor.x` is always = 0.5**, fixed by the way the packs were normalized: the single-stem group aligns its bottom-band
  to the canvas center, the rosette group aligns its bbox center to the canvas center (§7.1). **Do not measure the bottom-band centroid
  to derive anchorX** — that heuristic is wrong for rosette morphology and once made culantro slide sideways by up to
  37 px between stages. The centroid is still measured and reported on the `NOTE` line as a master QC signal; it does not
  fail the build.
- **`anchor.y` is measured per file** = `contactY / canvasH`, recorded for **every frame**; `placementAnchor` is only
  a representative value, accompanied by `anchorUniform` / `anchorSpread`:
  - crops: `0.894531` uniform (458/512, `anchorUniform: true`);
  - trees: `0.947266` uniform (970/1024, `anchorUniform: true`);
  - aquatic: per-frame `0.947266`–`0.947917` (lotus canvas 1024, water-* canvas 768);
  - soil: per-frame `0.701172`–`0.703125`.
- **`masterCanvasBySpecies`** is present when an atlas mixes several canvases — currently only `farm_aquatic_v01`
  (lotus 1024×1024, water-mimosa / water-spinach 768×768). The cell stays uniform; the game compensates display
  scale per §9.5, the atlas does not scale on its own.
- `farm_soil_v01` takes the tilled cell from `soil_tilled_v02.png` — `v01` has permanently corrupt IDAT, so the script picks the
  highest readable version (§11.1).

---

## 14. Shared art rules directly related to geometry

Every Mayhoa asset must continue to follow the art-style spec:

- nostalgic hand-painted farm sprite;
- soft painterly rendering;
- readable silhouette;
- selective dark-chromatic outlines;
- upper-left lighting;
- organic asymmetry;
- not photorealistic;
- not excessively glossy/vector-clean;
- not over-detailed;
- species/object identity readable at gameplay size.

Geometry normalization must not break these characteristics.

---

## 15. Canonical QC checklist for each multi-stage species

### File / canvas

- [ ] Correct number of files/stages.
- [ ] Filenames follow the convention.
- [ ] All stages share the same canvas size.
- [ ] Canvas matches the target class.
- [ ] PNG has clean alpha/transparent background.

### Anchor

- [ ] The semantic anchor has been clearly determined.
- [ ] Raw master PNGs share the exact same anchor coordinate.
- [ ] Grounded assets share the same contact/root Y (crops: contactY = 458 — §5.3).
- [ ] Crops: composite check onto the soil tile — the plant base sits at the plate center and does not stick out below the plate.
- [ ] Root/contact X is measured from the base band, not from the canopy center.
- [ ] No top alignment.
- [ ] No per-stage independent centering.

### Bounds

- [ ] No opaque pixel touches the edge unintentionally.
- [ ] Reasonable breathing room.
- [ ] No cropped leaf/fruit/branch/body.
- [ ] Bottom padding matches the class contract.

### Growth / scale

- [ ] Perceived size increases correctly along the lifecycle.
- [ ] A later stage is not smaller than an earlier one where the spec requires monotonic growth.
- [ ] Stage 05 is not smaller than stage 04.
- [ ] Not merely the same image scaled up.
- [ ] Relative world scale matches the semantic class.

### Lifecycle / content

- [ ] Stage semantics are correct for the species.
- [ ] No flower/fruit/harvest cue too early.
- [ ] The final stage has a clear enough focal cue without being overloaded.

### Runtime

- [ ] The runtime anchor is derived from the canonical master anchor.
- [ ] Atlas trim/remap does not change the gameplay pivot.
- [ ] The playground does not use per-stage auto-anchoring to hide master errors.
- [ ] The atlas is rebuilt with `python3 tools/build_atlas.py` after masters change — do not hand-edit atlas JSON/PNG (§13.2).
- [ ] `git status` is clean after rebuilding the atlas (the script is idempotent; a diff means a master really changed).

---

## 16. Audit plan for the next session

The next session should scan all of `masters/` in this order:

### Pass A — inventory

For each PNG, record:

```text
path
asset class
canvas W×H
alpha bbox
visible W×H
semantic anchor type
measured contact/root X/Y
stage index
```

### Pass B — group by lifecycle/species

For each species:

- verify the same canvas;
- verify the same root/contact/waterline;
- verify monotonic stage scale;
- find top-aligned or independently-centered packs;
- find files on the wrong master target.

### Pass C — normalize

Only normalize packs whose rule is locked:

- tree/perennial 1024: root `(512,970)`;
- crops: keep the current crop contract until the crop audit is settled;
- aquatic: lotus is settled at `1024×1024` root `(512,970)` — it can be normalized right away; mimosa/spinach need their pack anchors settled before normalizing;
- other classes: define the semantic anchor before touching files.

### Pass D — runtime metadata

After the masters pass:

- audit runtime JSON anchors;
- rebuild the atlas with `python3 tools/build_atlas.py` (use `--dry-run` to preview) — do not remap by hand;
- do not fix runtime before the master.

### Pass E — visual playground

Only check at the very end:

- stage transitions;
- soil/pond placement;
- relative scale between species;
- no jump at the anchor;
- no cropping/clipping during sway/animation.

---

## 17. Proposed audit report format

Each species should have a record like:

```text
Species: coffee
Class: tree/perennial
Semantic size class: L
Canvas: 1024×1024
Canonical anchor: (512,970)
Dominant growth metric: visibleHeight + canopyComplexity
Stage-05 target metric: visibleHeight
Stage-05 target value: <px after calibration>
Stage metric values: [...]
Stage ratios vs stage-05: [..., 1.0]
Measured root coordinates: [...]
Anchor delta max: ... px
Within-species progression: PASS/FAIL
Cross-species scale: PASS/FAIL
Canvas: PASS/FAIL
Lifecycle: PASS/FAIL
Clipping: PASS/FAIL
Action: KEEP / TRANSLATE / RESCALE / REGENERATE
```

For horizontal aquatic plants, replace `visibleHeight` with `horizontalSpread`/a suitable composite metric. For dragon-fruit, the report must include a plant-envelope metric **excluding the fixed support post**.

Recommended tolerance:

```text
Master anchor target: exact preferred
Measurement tolerance from anti-alias/root-band heuristic: <= 1 px ideal, <= 2 px acceptable only if semantic contact is visually identical
```

Do not use tolerance to legitimize a misalignment that is obvious to the eye.

---

## 18. Source-of-truth precedence

When older docs contradict each other about geometry, prioritize:

1. **`MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.md`** — anchor/canvas/layout/QC geometry.
2. Species-specific explicit lifecycle spec — morphology/harvest semantics.
3. `FARM_ASSET_GENERATION_PLAN.md` — roadmap/size/lifecycle general contract.
4. `MAYHOA_ART_STYLE_SPEC.md` — visual style/art direction.
5. Existing runtime JSON/README — implementation reference; may be legacy and must be audited.

Key rule:

> **Master geometry must be correct first. Runtime code/metadata must not be used to hide a master asset with a wrong anchor.**

---

## 19. Current locked decisions

As of the creation of this spec:

```text
Normal tree canvas: 1024×1024
Normal tree root:   (512,970)
Tree root meaning:  lowest/root contact point on raw master PNG
Tree growth:        grows upward/outward from fixed root
Tree stage rule:    same canvas + same root across lifecycle
Same stage rule:    same biological maturity, NOT same absolute pixel height
Growth audit:       use species-specific dominantGrowthMetric
Stage-05 target:    per-species/per-morphology, never one global px value
QC alpha threshold: 24/255
Master format:      RGBA8 PNG; palette/quantized master is invalid
Crop contract:      512×512, root (256,458) = (0.5,0.89453125), contactY=458 Δ0, max visH 434
Tile plant point:   soil plate center (256,260) ≈ (0.5,0.508) — where the engine pins every plant root
Aquatic anchor:     lotus LOCKED 1024×1024 root (512,970); mimosa/spinach pack-specific, pending
Coconut canvas:     1024×1024 LOCKED — do not use 1024×1280
Runtime legacy:     removed 2026-09-07 — replaced by 4 atlases generated from a script (§13.2)
Atlas naming:       <domain>_<class>_v<NN>, one atlas per class (§11.1)
Atlas build:        python3 tools/build_atlas.py — the atlas is a build product, never hand-edited
Atlas frame key:    slot id <species>_stage-0N; soil uses the full stem (soil_dry...)
Atlas anchorX:      constant 0.5, never measured from the bottom-band centroid
Atlas anchorY:      contactY/canvasH, measured and written for every frame
```

Remaining-plan support is explicitly defined for:

- `coconut` → Profile B / tall-special palm;
- `dragon-fruit` → Profile C / support-structure plant;
- `coffee` → Profile A / compact tree-shrub;
- `rubber` → Profile A / tall industrial tree;
- `lotus` → Profile D / aquatic upright-radial;
- `water-mimosa` → Profile E / aquatic horizontal;
- `water-spinach` → Profile E / aquatic horizontal.

This is the baseline for the next full scan/normalize pass over the Mayhoa assets.

---

## 20. Measured baseline — 2026-08-26

Measured with `tools/geometry_audit.py` (alpha ≥ 24/255, bottom band 3% of visible height). Δ = the largest difference between stages within a pack. PASS criteria for trees: contactY Δ=0, rootX Δ≤2 px, margin ≥24 px.

### Trees / perennial

| Species | Canvas | contactY (Δ) | rootX (Δ) | Worst margin | Progression notes | Verdict |
|---|---|---|---|---|---|---|
| coffee | 1024² ✓ | 970 (Δ0) ✓ | 511–513 (Δ1.6) ✓ | 33 px ✓ | matches Profile A (s03 = 0.867) | **PASS — calibration reference** |
| dragon-fruit | 1024² ✓ | 987–988 (Δ1) | 500–501 (Δ1.4) | top 27 px (s03) | s04 ≈ s05 bbox identical — visual density check | Internally consistent, off canonical (−11.5, +17.5) |
| coconut | 1254² ✗ | 1236 (Δ0) ✓ | 645–647 (Δ1.1) ✓ | top 6 px (s05) ✗, bottom 17 px ✗ | 0.65/0.84/0.95/0.99 — breaks Profile B | FAIL canvas + margin + progression |
| mango | 1122×1402 | 1282–1310 (Δ28) ✗ | 568–581 (Δ13) ✗ | 47 px ✓ | s05 visH < s04 (907 < 993) — check fruit cue | FAIL align |
| pomelo | 1122×1402 | 1290–1357 (Δ67) ✗ | 568–579 (Δ11) ✗ | 7 px (s05) ✗ | increasing ✓ | FAIL align + margin |
| lemon | 1122×1402 | 1167–1259 (Δ92) ✗ | 561–581 (Δ21) ✗ | 20 px (s05) ✗ | increasing ✓ | FAIL align |
| star-apple | 1122×1402 | 1218–1364 (Δ146) ✗ | 567–575 (Δ8) ✗ | 14 px (s05) ✗ | increasing ✓ | FAIL align (worst case) |
| lychee | 1254² ✗ | 1155–1230 (Δ75) ✗ | 650–698 (Δ48) ✗ | 22 px (s05) ✗ | increasing ✓ | FAIL align on both axes |
| rambutan | 1254² ✗ | 1173–1211 (Δ38) ✗ | 641–648 (Δ7) ✗ | 10 px (s04) ✗ | s05 < s04 in both dimensions ✗ | FAIL align + s04/s05 contradiction |

### Aquatic

| Species | Canvas | contactY (Δ) | rootX (Δ) | Margin | Spread progression | Verdict |
|---|---|---|---|---|---|---|
| lotus | 1254² ✗ | 1185–1187 (Δ2) | 585–647 (Δ62)* | 12 px (s05) ✗ | 0.25/0.64/0.81/0.95 — matches Profile D (widened) | FAIL canvas; *radial heuristic, align manually |

### Crops (soil-plate anchor — contactY not scored)

| Species | Canvas | rootX (Δ) | Worst margin | Progression | Verdict |
|---|---|---|---|---|---|
| rice | 512² ✓ (palette ✗) | 252–258 (Δ6) | 33 px ✓ | increasing ✓ | Geometry OK; palette format |
| corn | 512² ✓ (palette ✗) | 255–260 (Δ4) | top 4 px, bottom 19 px (s05) ✗ | increasing ✓ | FAIL margin s05 |
| carrot | 512² ✓ (palette ✗) | 256–265 (Δ9) | top 12 px (s04) ✗ | s05 < s04 (443 < 479) | FAIL margin s04; check s05 |
| tonkin-jasmine | 512² ✓ | 250–276 (Δ26) | 20 px (s03) | s05 < s04 in both dimensions ✗ | Visual check s05 |
| culantro | 512² ✓ | 228–352 (Δ125)* | 26 px | increasing ✓ | *Rosette — manual anchor (§7.1) |
| mint | 512² ✓ | 257–270 (Δ13) | 28 px | increasing ✓ | Near PASS |

Detailed handling plan + scale factors: see `ASSET_GEOMETRY_FIX_CHECKLIST.md`.

### 20.1 Post-normalize results — 2026-08-26 (same day)

The normalize pass has been completed with `tools/normalize_pack.py`. Re-measured results:

- **All 10 tree packs + lotus**: canvas `1024×1024`, contactY = 970 (Δ0), rootX 511.6–512.5 (Δ ≤ 1 px), every margin ≥ 25 px — **all PASS**.
- **durian** (the 11th pack, added after this round): audited 2026-09-10 as FAIL 5/5 and fixed the same day by a per-stage rescale — canvas `1024×1024`, contactY = 970 (Δ0), rootX 511.6–512.3, tightest margin 26 px, ratios 0.400 / 0.600 / 0.821 / 0.939 / 1.0 inside the Profile A band — **PASS**. Details in `ASSET_GEOMETRY_FIX_CHECKLIST.md` section 10.
- **coconut**: per-stage rescale following Profile B, new ratios 0.332 / 0.506 / 0.725 / 0.916 / 1.0 — within band.
- **crops (final rev 2, same day)**: two steps — (a) the composite QC found crop bases sticking out below the soil plate; (b) the calibration sheet confirmed the plant must stand at the **plate center**, leading to crops being switched to **bottom-anchor sprites** with root `(256, 458)`. Transform from the originals (single resample): rice / tonkin-jasmine / culantro / mint scale 1.0 (translate only), corn 0.8855, carrot 0.904. Herb rosettes align X by bbox center. The runtime `placementAnchor` in both JSONs changed → `(0.5, 0.89453125)`, textures rebuilt. All 3 palette packs became RGBA8. Composite of 30 frames + playground verify PASS. **Awaiting confirmation from the game-code side: the pin point on the tile = the plate center.**
- **Visual QC**: 6/6 cases in the regenerate queue PASS — no file had to be regenerated.
- **Runtime**: `core_fruit_trees_v02.json` + atlas rebuilt (cell 256×256, anchor `(0.5, 0.947265625)`); atlases for the new packs awaited a naming decision; the crops atlas texture should be re-rendered because corn/carrot were rescaled. *(Update 2026-09-07: the naming is settled as one atlas per class — `core_fruit_trees_v02` is replaced by `farm_trees_v01`, and all atlases are now generated by `tools/build_atlas.py`; see §11.1 + §13.2.)*
- **Still pending**: playground verify (Pass E) + user diff comparison + commit.
