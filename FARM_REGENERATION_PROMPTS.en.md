# Mayhoa — Regeneration Specs & Prompts (Round 1)

**Language:** [Tiếng Việt](FARM_REGENERATION_PROMPTS.vi.md) · English

**Status:** Ready to generate
**Queue source:** `ASSET_GEOMETRY_FIX_CHECKLIST.en.md` section 6 (visual review 2026-08-26)
**Related specs:** `MAYHOA_ART_STYLE_SPEC.en.md`, `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.en.md`

---

## 1. Workflow

For a **new species, always split this into two phases — write the prompt first, generate the assets
second.** Never merge them: the species block is the source of truth, and editing a paragraph of prompt
is far cheaper than regenerating five images.

**Phase A — write the prompt (generate nothing yet):**

1. Add the species block for the species to section E–K below: characteristic silhouette, leaf type, stage-04 flowers, stage-05 fruit.
2. Check it against the group's acceptance criteria — with the fruit covered up, the silhouette must still be distinguishable from every existing species.
3. Commit the prompt **before** moving on to phase B.

**Phase B — generate the assets:**

4. For each image: paste the **Shared Style Block + species block + exactly ONE stage line** into ChatGPT (together with the noted reference images). One prompt = one image.
5. Download the PNG, name it exactly per the convention in the table, and put it into the correct `masters/` folder.
6. Tell Claude → the pipeline runs by itself: `geometry_audit.py` → `normalize_pack.py` (resample + root alignment) → composite QC onto the soil tile → playground → PASS/FAIL report per file.

### Generation does NOT have to get these right (the pipeline fixes them)

- Canvas size / frame ratio — any square ≥1024 (tree) or ≥512 (crop/tile) is fine, the pipeline resamples.
- Plant position inside the frame, off-center root, too close to the edge, missing padding — the pipeline scales + translates.
- Relative size **between different species** — the runtime display scale takes care of that. (This does NOT cover the ratio **between stages within one pack** — that one is mandatory, see below.)

### Generation MUST get these right (no transform can save them)

- Correct species morphology + a characteristic silhouette (the main goal of this round).
- A painterly style consistent with the existing packs.
- The harvest/flower cue on the right stage — no early flowers or fruit.
- **A genuinely transparent background** (no white/black matte, no scene, no baked-in soil/tile).
- A single plant/object only, no contact sheet, no text/watermark.
- For multi-stage packs: the same individual plant growing, with the structure genuinely changing (not one image scaled up).
- **The height ratio between stages inside one pack** must land inside that species' profile band (Profile A/B/C, `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.en.md` §523–560). The pipeline applies one shared scale factor per pack, so it **cannot** repair a wrong growth curve.

---

## 2. Shared Style Block (paste at the top of EVERY prompt)

```text
Art style — "Nostalgic Hand-Painted Farm Sprite": a cozy farming-game sprite
inspired by classic 2008–2012 browser/social farm games. Soft painterly
hand-painted rendering with light brush texture; selective soft outlines in
dark green/brown chromatic tones (never pure black, never thick uniform
vector lines); readable silhouette at small gameplay size; cheerful pastel
palette, slightly washed, higher saturation only on focal parts (fruit,
flowers); gentle shading, light source upper-left; organic asymmetric shapes.
NOT photorealistic, NOT glossy modern mobile art, NOT clean vector/cel-shade,
NOT neon.

Format: single isolated game sprite on a FULLY TRANSPARENT background.
One object only, whole object fully inside frame with margin on all sides.
A very small soft contact shadow directly under the base is allowed; no long
cast shadows, no ground/soil/scene baked in, no text or watermark.
```

**Negatives to repeat when the model gets stubborn:** `no background, no soil tile, no scene, no frame, no border, no watermark, no photorealism, no 3D render, no neon colors, no multiple views, no sprite sheet`.

**Reference:** always attach 1–2 existing PASS assets as a style anchor — ideally `coffee_stage-05_berry_v01.png` (the calibration standard) + 1 older-version file of the same species (to keep it recognizable, with a note on what needs to change).

---

## 3. Output table

| # | Item | Files | Minimum canvas | Destination |
|---|---|---:|---|---|
| A | soil_tilled | 1 | 512 | `masters/farm/soil/soil_tilled_v02.png` |
| B | carrot stage-05 | 1 | 512 | `masters/farm/crops/carrot/carrot_stage-05_harvestable_v02.png` |
| C | tonkin-jasmine pack | 5 | 512 | `masters/farm/crops/tonkin-jasmine/tonkin-jasmine_stage-0N_<semantic>_v02.png` |
| D | lotus stage-05 | 1 | 1024 | `masters/farm/aquatic-crops/lotus/lotus_stage-05_flowering_v02.png` |
| E–J | 6 fruit tree packs | 30 | 1024 | `masters/farm/trees/<species>/<species>_stage-0N_<semantic>_v02.png` |
| K | durian pack (new species) | 5 | 1024 | `masters/farm/trees/durian/durian_stage-0N_<semantic>_v01.png` — **generated 2026-09-08** |

Stage semantics stay as in v01 (tree: sprout/sapling/young/flowering/fruiting; crop: seeded/sprout/young/mature/harvestable; for tonkin-jasmine see section C).

---

## A. soil_tilled (the v01 file is data-corrupt)

Attach references: `soil_empty_v01.png` + `soil_planted_v01.png`.

```text
A farmland soil tile sprite for a farming game, matching the attached soil
tiles exactly in style, palette, perspective and plate shape: a rounded
oval/elliptical dirt plate seen from a high 3/4 top-down angle, soft dark
earthy rim, warm brown dirt surface.

State: TILLED — the surface is freshly ploughed into 4–6 neat parallel
furrow rows that follow the oval perspective of the plate, with soft ridges
and shallow trenches, slightly darker moist soil in the trenches. No plants,
no seeds, no grass.
```

Acceptance: the same plate shape/size as the other 5 tiles (the pipeline will overlay and compare alpha); the furrows follow the oval perspective; no plants.

---

## B. carrot stage-05 (expose the root shoulders)

Attach references: `carrot_stage-04_mature_v01.png` + `carrot_stage-05_harvestable_v01.png` (note: keep the foliage, change the root part).

```text
Harvest-ready carrot plant sprite, same species and foliage style as the
attached reference: a lush rosette of feathery green carrot tops growing
from one point.

Key change: at the base, 2–3 plump bright-orange carrot shoulders push
clearly up out of the ground — big, rounded, unmistakably readable as
carrots even at small size, taking roughly the bottom 1/5 of the plant
height, with a hint of root taper. This is the harvest cue: make the orange
pop against the green foliage.
```

Acceptance: the orange root shoulders read clearly at ~150 px; the foliage is still the same species as s01–s04; orange appears only at s05 (s04 stays at v01).

---

## C. tonkin-jasmine (Vietnamese: thiên lý) — the whole 5-stage pack, trellis-climbing form

New contract: **support-structure plant** like dragon fruit (spec §9.4 Profile C) — a fixed wooden trellis, **identical in all 5 images** (size, position, style), with only the vine growing. Measure the progression by plant coverage, excluding the trellis.

Attach references: `dragon-fruit_stage-03_young_v01.png` (post style + rustic feel) + 1 tonkin-jasmine v01 image (to keep the signature heart-shaped leaves + yellow-green flowers).

Base prompt for the whole pack (append the matching stage line):

```text
A Tonkin jasmine vine (Telosma cordata, Vietnamese: thien ly) growing on a small rustic
wooden trellis — two upright weathered wooden posts with 2–3 horizontal
crossbars, simple and hand-made looking. The trellis is a FIXED structure:
keep its exact size, shape and position identical across all growth stages;
only the vine changes. Heart-shaped soft green leaves, slender twining stems.
```

| Stage | Line to append to the prompt | File |
|---|---|---|
| 01 seeded | `Stage: just planted — the bare empty trellis, freshly disturbed soil spot at its base with a tiny 2-leaf sprout emerging. No vine on the trellis yet.` | `tonkin-jasmine_stage-01_seeded_v02.png` |
| 02 sprout | `Stage: young sprout — a single thin vine has started twining up one post, reaching the first crossbar, a handful of small heart-shaped leaves.` | `tonkin-jasmine_stage-02_sprout_v02.png` |
| 03 young | `Stage: young vine — the vine now covers about half the trellis with fresh green heart-shaped leaves, a few stems dangling. No flowers.` | `tonkin-jasmine_stage-03_young_v02.png` |
| 04 mature | `Stage: mature — dense foliage covering most of the trellis, layered heart-shaped leaves, a few curling stem tips. No flowers yet.` | `tonkin-jasmine_stage-04_mature_v02.png` |
| 05 harvestable | `Stage: harvestable — full lush coverage plus several restrained clusters of small pale yellow-green Tonkin jasmine flower buds tucked among the leaves; flowers are the focal cue but must not overload the sprite.` | `tonkin-jasmine_stage-05_harvestable_v02.png` |

Acceptance: the trellis is identical across 5/5 images (the pipeline will diff the trellis silhouette); coverage increases per Profile C (0.20–0.35 / 0.40–0.55 / 0.65–0.80 / 0.88–0.96 / 1.0); flowers only at s05.

---

## D. lotus stage-05 (smaller flower)

Attach references: `lotus_stage-04_budding_v01.png` + `lotus_stage-05_flowering_v01.png` (note: keep all the leaves, only fix the flower proportion).

```text
Flowering lotus plant sprite, same species, leaf style and radial
composition as the attached stage-05 reference.

Key change: the main pink lotus bloom must be CLEARLY SMALLER than the
largest leaf — about 60–70% of its current size — botanically believable
while still the focal point through its saturated pink color. Keep one
green seed pod and one closed pink bud among the leaves. Leaves unchanged:
large round pastel green lotus pads on upright stems, radial spread.
```

Acceptance: the diameter of the main bloom < the diameter of the largest leaf; it still reads as the harvest stage thanks to the color; the spread ratio does not drop versus s04 (Profile D).

---

## E–J. 6 fruit trees — regenerate the whole pack, with a silhouette characteristic of each species

The problem with the v01 round: all 6 trees used the same "round canopy + brown trunk" formula and differed only in their fruit. This round **the silhouette must identify the species even with the fruit covered up**.

### Stage template (shared, substitute `<SPECIES BLOCK>`)

```text
<SHARED STYLE BLOCK>

<SPECIES BLOCK — dán khối riêng từng loài bên dưới>

Same individual tree across all 5 stages, structure genuinely changing:
Stage 01 — sprout: small seedling, 2–4 leaves showing the species' leaf character.
  HEIGHT: 0.35–0.45 of the mature stage-05 tree.
Stage 02 — sapling: young tree, thin trunk, first branches, species leaf shape clear.
  HEIGHT: 0.55–0.65 of the mature stage-05 tree.
Stage 03 — young: distinctly smaller and simpler than mature, but the species
silhouette is already recognizable. No flowers, no fruit.
  HEIGHT: 0.75–0.88 of the mature stage-05 tree.
Stage 04 — flowering: near-full silhouette with the species' flowers. No fruit.
  HEIGHT: 0.90–0.98 of the mature stage-05 tree.
Stage 05 — fruiting: full mature silhouette, harvest-ready fruit as focal cue.
  HEIGHT: this is the reference — 1.0.
```

> **The `HEIGHT:` line is mandatory and must sit in each stage's own prompt.**
> Because one prompt carries only **one** stage line, a size constraint that is
> not on that line is never seen by the model. Omitting it is why `coconut`
> broke Profile B (`0.65/0.84/0.95/0.99`) and `durian` broke Profile A
> (`0.66/0.95/0.99/1.00`) — the tree stops growing after stage 02.
>
> `normalize_pack.py` applies **one** scale factor to the whole pack, so it
> **cannot** repair a flat growth curve: getting this wrong means regenerating.
>
> The numbers above are **Profile A** (upright woody trees — E–J, `durian`,
> `coffee`, `rubber`). Species on another profile need different numbers:
> **Profile B** palms (`0.25–0.35 / 0.40–0.55`), **Profile C** trellis climbers
> (`0.20–0.35 / 0.40–0.55`). Full table: `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.en.md` §523–560.

Generate **one image at a time** (one prompt = shared block + species block + exactly one stage line).

### E. Mango `mango`

```text
MANGO TREE. Silhouette: a BROAD SPREADING DOME — the canopy is clearly wider
than tall, with 2–3 heavy near-horizontal limbs. Long slender dark-green
leaves drooping in clusters, young leaf flush in coppery red-bronze at
branch tips. Flowers (stage 4): upright pale yellow panicle plumes at the
canopy edge. Fruit (stage 5): yellow-orange mangoes DANGLING on long string-
like stalks well below the foliage — the hanging stalks are the signature.
```

### F. Pomelo `pomelo`

```text
POMELO TREE. Silhouette: an OPEN, slightly sparse and irregular crown where
individual sturdy branches stay visible through the foliage; thick trunk.
Large rounded glossy leaves with winged leaf stalks. Flowers (stage 4):
large white citrus blossoms. Fruit (stage 5): only a FEW but VERY LARGE
round green-yellow pomelos, visibly heavy, bending their branches downward —
few-but-huge is the signature.
```

### G. Lemon `lemon`

```text
LEMON TREE. Silhouette: a SMALL LOW BUSHY citrus — clearly the shortest
fruit tree, crown starting near the ground, almost shrub-like, dense with
small glossy pointed leaves, thin twiggy branches. Flowers (stage 4): small
white-purple-tinged citrus blossoms. Fruit (stage 5): many small bright
yellow lemons scattered evenly through the low canopy. Keep the whole tree
compact and low — it must NOT look like a tall tree.
```

### H. Star apple `star-apple`

```text
STAR APPLE TREE (vu sua, Chrysophyllum cainito). Silhouette: dense layered
canopy with slightly DROOPING branch tips. Signature: TWO-TONE FOLIAGE —
leaves glossy dark green on top with a distinctly COPPERY GOLDEN-BROWN
underside, so the canopy shimmers green-and-bronze wherever leaves turn.
This two-tone shimmer must read at a glance. Flowers (stage 4): tiny
inconspicuous purplish-white clusters along twigs. Fruit (stage 5): round
smooth fruits in purple and green-purple, sitting close to the branches.
```

### I. Lychee `lychee`

```text
LYCHEE TREE. Silhouette: a DENSE LOW ROUNDED MUSHROOM-shaped canopy, wider
than tall, compact and full with almost no gaps; short stout trunk. Pinnate
leaves in drooping clusters. Flowers (stage 4): airy pale yellow-green
panicle sprays on the canopy surface. Fruit (stage 5): bright red round
fruits with a BUMPY knobbly rind, hanging in tight grape-like BUNCHES at
the canopy edge.
```

### J. Rambutan `rambutan`

```text
RAMBUTAN TREE. Silhouette: an irregular OPEN spreading crown with a few
distinct foliage clumps and visible gaps between them (less tidy than
lychee); slightly leaning character in the trunk. Flowers (stage 4): subtle
greenish-yellow clusters. Fruit (stage 5): red fruits covered in SOFT HAIRY
GREEN-TIPPED SPINES, in loose clusters — the hairy texture is the signature
and must be visible.
```

### K. Durian `durian`

```text
DURIAN TREE (Durio zibethinus). Silhouette: a SLENDER, TALL PYRAMIDAL / CONICAL
CANOPY — distinctly taller than wide. Central upright straight woody trunk with
elegant vertical taper, branching outward into 3–4 clearly SEPARATED horizontal
scaffold tiers (pagoda-like tiered architecture). Between the tiers there must be
EMPTY TRANSPARENT GAPS you can see straight through — the canopy is a few
distinct foliage shelves stacked with air between them, NOT one continuous
conical mass and NOT a round dense dome. Think stacked pagoda roofs, not a
Christmas tree.
Foliage: slender elongated lanceolate leaves with sharp pointed tips. Two-tone
coloring: upper leaf surface is a light, soft warm olive-green and sunny pastel
sage-green with crisp pale-yellow midrib veins and glossy sunlight highlights;
underside has a soft shimmering light golden-bronze / dusty gold sheen.
Flowers (stage 4): clusters of creamy-white and pale golden-butter blossoms
hanging directly beneath the horizontal woody branches (cauliflory), dangling
down into the open gaps between tiers so each cluster is silhouetted against
empty space instead of being buried in the leaves.
Fruit (stage 5): 5–7 large, spiky DURIAN fruits with sharp pyramidal thorns,
bright golden-olive green, hanging on thick rope-like woody stalks directly
underneath the horizontal tiered limbs (cauliflory). Each fruit is BIG — at
least as wide as the trunk — and hangs DOWN INTO THE EMPTY GAP below its own
branch tier, fully silhouetted against the transparent background with clear
space around it. No fruit may be tucked inside or overlapped by the foliage
mass. The fruits must be the single loudest read in the image at 150 px.
```

Acceptance for group E–K:

- With the fruit covered up, the 7 species are still distinguishable by silhouette (especially: mango broad-domed, lemon low-bushy, lychee dense-mushroom, rambutan open-ragged, star-apple two-tone leaves, durian tall-pyramidal-tiered).
- Lemon: the shortest of the group (the display target has already been lowered to ~256 px — spec §9.5).
- No flowers at s01–s03, no fruit at s01–s04.
- **The harvest cue must sit in open space.** Fruit (and flowers) hang out into the gaps, clear of the foliage mass, cleanly silhouetted against the transparent background. Fruit buried inside the canopy is a FAIL even when the painting is beautiful — at 150 px the player cannot tell the plant is ready.
- Profile A progression (s03 ≤ 0.88 after the loosening).
- The pipeline will align the root (512, 970) and the margins itself — no need to frame it at generation time.

---

## 4. After generating

- Put the v02 file next to v01 (do not delete v01 until it PASSes).
- Claude runs: audit → normalize → composite → playground → per-file report in the format from spec §17.
- Files that PASS: v02 becomes canonical, v01 is archived; the runtime atlas is rebuilt as the final step.
