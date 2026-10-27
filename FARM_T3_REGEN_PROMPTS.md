# Mayhoa — T3 regeneration: 9 crop images (2026-10-05)

**Status (2026-10-05): done.** All 9 generated with `codex1 exec` (codex-cli built-in `image_gen`,
references via `-i`), normalised into `masters/` as `_v02`. Retries: dragon fruit s2 and s3 took 2 tries
(s2 too close to s1; s3 canopy floated over a bare gap), the rest passed first time.
**Queue source:** `mayhoa/docs/slice/TASKS.md` T3. **Style:** `MAYHOA_ART_STYLE_SPEC.md`,
`mayhoa/docs/slice/ART-DIRECTION.md` §5–§6.

## What and why

| # | File to produce (raw, into `.ai-bridge/t3/incoming/`) | Fixes | Order |
|---|---|---|---|
| 1 | `corn_stage-04_mature_v02.png` | no tassel / no young ears readable | before #2 |
| 2 | `corn_stage-05_harvestable_v02.png` | ears too small, kernels not shown | after #1 |
| 3 | `carrot_stage-05_harvestable_v02.png` | one orange stub, reads as a potted plant | any |
| 4 | `rice_stage-01_seeded_v02.png` | single hair-thin sprout vanishes on a 38 px tile | any |
| 5 | `dragon-fruit_stage-01_sprout_v02.png` | wooden post → concrete post + tyre | first of 5–9 |
| 6 | `dragon-fruit_stage-02_sapling_v02.png` | stage 2 and 3 look the same | after #5 |
| 7 | `dragon-fruit_stage-03_young_v02.png` | same | after #5 |
| 8 | `dragon-fruit_stage-04_flowering_v02.png` | concrete post + tyre | after #5 |
| 9 | `dragon-fruit_stage-05_fruiting_v02.png` | concrete post + tyre | after #8 |

v01 files stay where they are: `mayhoa/tools/prep_sprites.py` and `tools/build_atlas.py` both
take the highest `_vNN` per stage.

## Contract for every image

- **Size:** ask for a square **1024x1024**. Any square ≥1024 is fine; step 3 below resamples.
- **Background:** fully transparent, real alpha (RGBA). No checkerboard, soil, water or scene.
- **Anchor:** the plant's root / the post's foot sits at the **bottom centre** of the canvas.
  After normalising, the master root is `(256, 458)` on a 512 canvas for corn/carrot/rice
  (`(0.5, 0.89453125)`) and `(512, 970)` on a 1024 canvas for dragon fruit (`(0.5, 0.947266)`).
- **Mode:** ChatGPT project "mayhoa", **Chat** mode (not Work), `@Create image`, one image per
  message, 2 reference attachments. Prompts below are one ASCII paragraph each on purpose
  (`GEN_IMAGE_WORKFLOW.md` A3: newlines send early, Vietnamese diacritics get eaten).
- **QC before downloading:** the check line under each prompt, plus no text / frame /
  watermark / second object. Fail → correct in the same chat, at most 3 rounds.
- Reference paths are relative to `/Users/kelvin/Projects/yudgnahk/mayhoa-asset/`.
  `STYLE` = `masters/farm/trees/coffee/coffee_stage-05_berry_v01.png` (calibration standard).

---

## 1. Corn stage 4 — tassel and young ears

Attach: `masters/farm/crops/corn/corn_stage-04_mature_v01.png` + `STYLE`.

```text
Art style - Nostalgic Hand-Painted Farm Sprite: a cozy farming-game sprite inspired by classic 2008-2012 browser/social farm games. Soft painterly hand-painted rendering with light brush texture; selective soft outlines in dark green/brown chromatic tones (never pure black, never thick uniform vector lines); readable silhouette at small gameplay size; cheerful pastel palette, slightly washed, higher saturation only on focal parts; gentle shading, light source upper-left; organic asymmetric shapes. NOT photorealistic, NOT glossy, NOT clean vector, NOT neon. Format: one isolated game sprite on a FULLY TRANSPARENT background (real alpha, not a painted checkerboard), square 1024x1024 canvas, whole plant inside the frame with margin on all sides, plant base at the bottom centre, only a tiny soft contact shadow under the base, no soil, no scene, no text, no watermark, no sprite sheet. Subject: a corn (maize) plant at growth stage 4 of 5, mature but not ripe, same stalk and leaf style as the first attached image: one upright segmented green stalk with long broad arching strap leaves growing alternately up the stalk. Key change: on top, a clearly visible pale golden-cream tassel branching like a small open fan of thin spikes; at mid height, 2 young corn ears attached to the stalk, each slim and wrapped in tight green husk with a tuft of pale yellow-brown silk at the tip. No yellow kernels visible yet. Tassel and ears must stay readable when the whole plant is only 80 pixels tall, so make them slightly larger than life. The plant fills about 85 percent of the canvas height.
```

Check: tassel and 2 ears with silk read at thumbnail size; no kernels; same species look as v01.

## 2. Corn stage 5 — big ears, husk open on yellow kernels

Attach: `.ai-bridge/t3/incoming/corn_stage-04_mature_v02.png` (from #1) +
`masters/farm/crops/corn/corn_stage-05_harvestable_v01.png`.

```text
Art style - Nostalgic Hand-Painted Farm Sprite: a cozy farming-game sprite inspired by classic 2008-2012 browser/social farm games. Soft painterly hand-painted rendering with light brush texture; selective soft outlines in dark green/brown chromatic tones (never pure black, never thick uniform vector lines); readable silhouette at small gameplay size; cheerful pastel palette, slightly washed, higher saturation only on focal parts; gentle shading, light source upper-left; organic asymmetric shapes. NOT photorealistic, NOT glossy, NOT clean vector, NOT neon. Format: one isolated game sprite on a FULLY TRANSPARENT background (real alpha, not a painted checkerboard), square 1024x1024 canvas, whole plant inside the frame with margin on all sides, plant base at the bottom centre, only a tiny soft contact shadow under the base, no soil, no scene, no text, no watermark, no sprite sheet. Subject: the SAME corn plant as the first attached image, one stage later and ready to harvest: same stalk, leaves and tassel, leaf tips turning slightly golden. Harvest cue: 2 big plump corn ears, about twice the size of the young ears in the first image, each with its green husk peeled partly open and folded back so a clear column of warm golden-yellow kernels shows, with dry brown silk at the tip. The yellow kernels are the focal point and must read clearly when the plant is only 80 pixels tall; cartoon exaggeration of the ear size is welcome. Soft painted kernels, no glossy highlights. The plant fills about 88 percent of the canvas height.
```

Check: open husk + yellow kernels obvious at thumbnail size; plant clearly the same as #1.

## 3. Carrot stage 5 — three big orange shoulders

Attach: `masters/farm/crops/carrot/carrot_stage-04_mature_v01.png` +
`masters/farm/crops/carrot/carrot_stage-05_harvestable_v01.png`.

```text
Art style - Nostalgic Hand-Painted Farm Sprite: a cozy farming-game sprite inspired by classic 2008-2012 browser/social farm games. Soft painterly hand-painted rendering with light brush texture; selective soft outlines in dark green/brown chromatic tones (never pure black, never thick uniform vector lines); readable silhouette at small gameplay size; cheerful pastel palette, slightly washed, higher saturation only on focal parts; gentle shading, light source upper-left; organic asymmetric shapes. NOT photorealistic, NOT glossy, NOT clean vector, NOT neon. Format: one isolated game sprite on a FULLY TRANSPARENT background (real alpha, not a painted checkerboard), square 1024x1024 canvas, whole plant inside the frame with margin on all sides, plant base at the bottom centre, only a tiny soft contact shadow under the base, no soil, no scene, no text, no watermark, no sprite sheet. Subject: harvest-ready carrots, same species and feathery finely divided foliage as the attached references. Key change: at the base, THREE separate big plump bright warm-orange carrot roots stand side by side across the full width of the base, each showing its rounded shoulder and upper body with soft horizontal root rings and a slight taper, each with its own tuft of feathery leaves rising from its top, so it reads as three carrots in a row and never as one potted plant. The orange roots take roughly the bottom third of the sprite height. The foliage is a little shorter and less dense than in the first reference so the orange reads first. Carrot orange, not neon. No flowers.
```

Check: three distinct orange roots at thumbnail size; foliage matches s04.

## 4. Rice stage 1 — a visible seedling clump (mạ)

Attach: `masters/farm/crops/rice/rice_stage-02_sprout_v01.png` +
`masters/farm/crops/rice/rice_stage-01_seeded_v01.png`.

```text
Art style - Nostalgic Hand-Painted Farm Sprite: a cozy farming-game sprite inspired by classic 2008-2012 browser/social farm games. Soft painterly hand-painted rendering with light brush texture; selective soft outlines in dark green/brown chromatic tones (never pure black, never thick uniform vector lines); readable silhouette at small gameplay size; cheerful pastel palette, slightly washed, higher saturation only on focal parts; gentle shading, light source upper-left; organic asymmetric shapes. NOT photorealistic, NOT glossy, NOT clean vector, NOT neon. Format: one isolated game sprite on a FULLY TRANSPARENT background (real alpha, not a painted checkerboard), square 1024x1024 canvas, whole plant inside the frame with margin on all sides, plant base at the bottom centre, only a tiny soft contact shadow under the base, no soil, no water, no mud, no scene, no text, no watermark, no sprite sheet. Subject: a freshly transplanted clump of young rice seedlings, growth stage 1 of 5: a small but clearly visible tuft of 7 to 9 seedlings bundled at one base point, thin fresh bright-green grass-like blades fanning out in a loose V, a few blades gently bending, lighter yellow-green tips. Same blade style and green as the first attached image but shorter and fewer blades: about 60 percent of its height and roughly as wide as tall. The second attached image is the old stage 1, a single thin sprout that disappears at game size; this one must read as a small plant clump when only 30 pixels tall. The clump fills about 50 percent of the canvas height.
```

Check: reads as a tuft (not a single sprout) at thumbnail size; shorter than rice s02.

---

## 5–9. Dragon fruit (thanh long) — concrete post with a tyre, 5 stages

The post and tyre are fixed across all five images, so generate #5 first and attach its
result to #6–#8. Every dragon-fruit prompt carries this paragraph (already inlined below):
a slender grey precast concrete post with a square section and softly chipped edges, about
5 times taller than wide, standing at the bottom centre; an old black rubber motorbike tyre
lying flat on top as a ring, held by two short crossbars, as grown in Binh Thuan; tyre top
at about 25 percent from the top of the canvas, post foot at about 95 percent.

### 5. Stage 1 — bare post, cuttings at the foot

Attach: `masters/farm/trees/dragon-fruit/dragon-fruit_stage-01_sprout_v01.png` + `STYLE`.

```text
Art style - Nostalgic Hand-Painted Farm Sprite: a cozy farming-game sprite inspired by classic 2008-2012 browser/social farm games. Soft painterly hand-painted rendering with light brush texture; selective soft outlines in dark green/brown chromatic tones (never pure black, never thick uniform vector lines); readable silhouette at small gameplay size; cheerful pastel palette, slightly washed, higher saturation only on focal parts; gentle shading, light source upper-left; organic asymmetric shapes. NOT photorealistic, NOT glossy, NOT clean vector, NOT neon. Format: one isolated game sprite on a FULLY TRANSPARENT background (real alpha, not a painted checkerboard), square 1024x1024 canvas, whole object inside the frame with margin on all sides, only a tiny soft contact shadow under the base, no soil, no scene, no text, no watermark, no sprite sheet. Subject: a Vietnamese dragon fruit (thanh long) planting on its farm support. Support: a slender grey precast concrete post with a square cross-section and softly chipped edges, about 5 times taller than it is wide, standing upright at the bottom centre; on top of the post an old black rubber motorbike tyre lies flat as a ring, held by two short crossbars, exactly how dragon fruit is grown in Binh Thuan, Vietnam. The tyre top sits about 25 percent from the top of the canvas and the post foot about 95 percent. This post and tyre are a fixed structure that will be reused unchanged for later growth stages. Stage 1 of 5, just planted: 2 or 3 short young cuttings, each 2 or 3 segments of flat three-ribbed (triangular section) light-green cactus stem with softly scalloped edges, planted at the foot of the post and loosely tied to it with straw string, reaching only about a quarter of the post height. Nothing on or above the tyre yet. The attached reference uses a wooden post: REPLACE it with the grey concrete post and black tyre, keep only its painterly style.
```

Check: grey concrete post + black tyre ring on top; short cuttings at the foot only.

### 6. Stage 2 — stems climbing, tyre still bare

Attach: `.ai-bridge/t3/incoming/dragon-fruit_stage-01_sprout_v02.png` (from #5) +
`masters/farm/trees/dragon-fruit/dragon-fruit_stage-02_sapling_v01.png`.

```text
Art style - Nostalgic Hand-Painted Farm Sprite: a cozy farming-game sprite inspired by classic 2008-2012 browser/social farm games. Soft painterly hand-painted rendering with light brush texture; selective soft outlines in dark green/brown chromatic tones (never pure black, never thick uniform vector lines); readable silhouette at small gameplay size; cheerful pastel palette, slightly washed, higher saturation only on focal parts; gentle shading, light source upper-left; organic asymmetric shapes. NOT photorealistic, NOT glossy, NOT clean vector, NOT neon. Format: one isolated game sprite on a FULLY TRANSPARENT background (real alpha, not a painted checkerboard), square 1024x1024 canvas, whole object inside the frame with margin on all sides, only a tiny soft contact shadow under the base, no soil, no scene, no text, no watermark, no sprite sheet. Subject: the SAME dragon fruit planting as the first attached image, stage 2 of 5. The grey concrete post and the black tyre on top must be identical to the first attached image: same size, proportions, position and framing on the canvas. Change only the plant: two or three segmented, flat three-ribbed green cactus stems now climb straight up the post, tied to it with straw string at two points, reaching about three quarters of the post height. The stems have NOT reached the tyre: the tyre and the top quarter of the post are still bare. No drooping canopy, no branches hanging, no flowers, no fruit. The second attached image shows the stem texture only; ignore its wooden post and its full canopy, both are wrong for this stage.
```

Check: tyre and top of post bare; clearly less plant than #7.

### 7. Stage 3 — first spill over the tyre

Attach: `.ai-bridge/t3/incoming/dragon-fruit_stage-01_sprout_v02.png` +
`masters/farm/trees/dragon-fruit/dragon-fruit_stage-03_young_v01.png`.

```text
Art style - Nostalgic Hand-Painted Farm Sprite: a cozy farming-game sprite inspired by classic 2008-2012 browser/social farm games. Soft painterly hand-painted rendering with light brush texture; selective soft outlines in dark green/brown chromatic tones (never pure black, never thick uniform vector lines); readable silhouette at small gameplay size; cheerful pastel palette, slightly washed, higher saturation only on focal parts; gentle shading, light source upper-left; organic asymmetric shapes. NOT photorealistic, NOT glossy, NOT clean vector, NOT neon. Format: one isolated game sprite on a FULLY TRANSPARENT background (real alpha, not a painted checkerboard), square 1024x1024 canvas, whole object inside the frame with margin on all sides, only a tiny soft contact shadow under the base, no soil, no scene, no text, no watermark, no sprite sheet. Subject: the SAME dragon fruit planting as the first attached image, stage 3 of 5. The grey concrete post and the black tyre on top must be identical to the first attached image: same size, proportions, position and framing. Change only the plant: the climbing stems, tied to the post with straw string, have reached the top, grown up through the tyre and now spill over it: a first sparse ring of 6 to 8 arching flat three-ribbed segmented green branches drapes over the tyre rim on all sides and hangs down only about one fifth of the post height below the tyre, with a few fresh lighter-green shoots on top. The black tyre is still partly visible between the branches. No flowers, no fruit. It must look clearly younger and sparser than a full canopy; use the second attached image for stem texture only and ignore its wooden post.
```

Check: a sparse ring hanging just below the tyre, tyre still visible; distinct from #6 and #8.

### 8. Stage 4 — full canopy, white flowers

Attach: `.ai-bridge/t3/incoming/dragon-fruit_stage-01_sprout_v02.png` +
`masters/farm/trees/dragon-fruit/dragon-fruit_stage-04_flowering_v01.png`.

```text
Art style - Nostalgic Hand-Painted Farm Sprite: a cozy farming-game sprite inspired by classic 2008-2012 browser/social farm games. Soft painterly hand-painted rendering with light brush texture; selective soft outlines in dark green/brown chromatic tones (never pure black, never thick uniform vector lines); readable silhouette at small gameplay size; cheerful pastel palette, slightly washed, higher saturation only on focal parts; gentle shading, light source upper-left; organic asymmetric shapes. NOT photorealistic, NOT glossy, NOT clean vector, NOT neon. Format: one isolated game sprite on a FULLY TRANSPARENT background (real alpha, not a painted checkerboard), square 1024x1024 canvas, whole object inside the frame with margin on all sides, only a tiny soft contact shadow under the base, no soil, no scene, no text, no watermark, no sprite sheet. Subject: the SAME dragon fruit planting as the first attached image, stage 4 of 5, flowering. The grey concrete post and the black tyre on top must be identical to the first attached image: same size, proportions, position and framing. Change only the plant: a full dense mop-shaped canopy of many long flat three-ribbed segmented green branches arching up and out over the tyre and hanging down around the post to about half the post height, almost hiding the tyre; the lower half of the post stays visible. 4 or 5 large dragon fruit flowers on the hanging branches: long creamy-white trumpet petals with a pale yellow centre and a greenish-yellow outer ring. No fruit. Canopy about 3 times as wide as the tyre. Use the second attached image for canopy density and flowers only and ignore its wooden post.
```

Check: full canopy, white flowers, no fruit; post foot and tyre position match #5.

### 9. Stage 5 — fruit

Attach: `.ai-bridge/t3/incoming/dragon-fruit_stage-04_flowering_v02.png` (from #8) +
`masters/farm/trees/dragon-fruit/dragon-fruit_stage-05_fruiting_v01.png`.

```text
Art style - Nostalgic Hand-Painted Farm Sprite: a cozy farming-game sprite inspired by classic 2008-2012 browser/social farm games. Soft painterly hand-painted rendering with light brush texture; selective soft outlines in dark green/brown chromatic tones (never pure black, never thick uniform vector lines); readable silhouette at small gameplay size; cheerful pastel palette, slightly washed, higher saturation only on focal parts; gentle shading, light source upper-left; organic asymmetric shapes. NOT photorealistic, NOT glossy, NOT clean vector, NOT neon. Format: one isolated game sprite on a FULLY TRANSPARENT background (real alpha, not a painted checkerboard), square 1024x1024 canvas, whole object inside the frame with margin on all sides, only a tiny soft contact shadow under the base, no soil, no scene, no text, no watermark, no sprite sheet. Subject: the SAME dragon fruit planting as the first attached image, stage 5 of 5, ready to harvest. Keep the grey concrete post, the black tyre and the full hanging canopy identical to the first attached image: same size, proportions, position and framing. Change only this: the white flowers are gone and 5 to 7 plump oval dragon fruits hang on the branches all around the canopy, warm deep magenta-pink skin with soft leaf-like scales whose tips are green. The fruits must read clearly when the whole plant is only 60 pixels tall; slightly larger than life is welcome. Warm pink, not neon, no glossy highlights. Use the second attached image for fruit look only and ignore its wooden post.
```

Check: pink fruits obvious at thumbnail size, no flowers; canopy and post match #8.

---

## After generating: drop in and rebuild (exact steps)

Either open `claude` interactively in this repo and say *"run FARM_T3_REGEN_PROMPTS.md through
Lane A of GEN_IMAGE_WORKFLOW.md"* (it does all of the below), or by hand:

**1. Save the raws** under the exact names in the table above:

```bash
cd /Users/kelvin/Projects/yudgnahk/mayhoa-asset
mkdir -p .ai-bridge/t3/incoming    # put the 9 downloads here, renamed
```

**2. Alpha check** — every file must print `RGBA`; any `RGB` file has a painted checkerboard
and goes through the dechecker first:

```bash
for f in .ai-bridge/t3/incoming/*.png; do python3 -c "from PIL import Image;import sys;print(Image.open(sys.argv[1]).mode, sys.argv[1])" "$f"; done
# only for an RGB file:  python3 tools/dechecker.py "$f" "$f"
```

**3. Normalise into `masters/`** (scale to the stage height, root to the anchor). `normalize_pack.py`
edits in place, so copy first; to redo, copy the raw again.

```bash
vis_h() { python3 -c "import sys;sys.path.insert(0,'tools');from normalize_pack import measure;from PIL import Image;print(measure(Image.open(sys.argv[1]).convert('RGBA'))['vis_h'])" "$1"; }
crop() {  # crop <folder> <file> <target visible height on the 512 canvas>
  cp ".ai-bridge/t3/incoming/$2" "masters/farm/crops/$1/$2"
  s=$(python3 -c "print($3/$(vis_h ".ai-bridge/t3/incoming/$2"))")
  python3 tools/normalize_pack.py --mode root --canvas 512 512 --target 256 458 --scale "$s" "masters/farm/crops/$1/$2"
}
crop corn   corn_stage-04_mature_v02.png        415
crop corn   corn_stage-05_harvestable_v02.png   430
crop carrot carrot_stage-05_harvestable_v02.png 400
crop rice   rice_stage-01_seeded_v02.png        150

# dragon fruit: ONE scale for all five, taken from the bare post, so the post stays one size
D=masters/farm/trees/dragon-fruit
cp .ai-bridge/t3/incoming/dragon-fruit_stage-0*_v02.png "$D/"
s=$(python3 -c "print(800/$(vis_h .ai-bridge/t3/incoming/dragon-fruit_stage-01_sprout_v02.png))")
python3 tools/normalize_pack.py --mode root --canvas 1024 1024 --target 512 970 --scale "$s" "$D"/dragon-fruit_stage-0*_v02.png
```

Heights come from the v01 masters (corn s04/s05 412/431 px, carrot s05 398 px) and ART-DIRECTION
§5 (rice s01 ≈ 60 % of s02's 262 px). Every printed margin must be ≥ 24; if a dragon-fruit file
errors "vượt canvas" or prints a margin < 24, redo it with 760 instead of 800.

**4. Post alignment check (dragon fruit)** — the tyre must sit on the same line in all five:

```bash
python3 -c "
from PIL import Image, ImageDraw
import glob
fs=sorted(glob.glob('masters/farm/trees/dragon-fruit/*_v02.png')); top=Image.open(fs[0]).getchannel('A').getbbox()[1]
sheet=Image.new('RGBA',(1024*5,1024),(235,225,200,255))
for i,f in enumerate(fs): sheet.alpha_composite(Image.open(f).convert('RGBA'),(i*1024,0))
ImageDraw.Draw(sheet).line([(0,top),(5120,top)],fill=(255,0,0,255),width=3); sheet.resize((1280,256)).save('/tmp/df_v02_check.png')"
open /tmp/df_v02_check.png
```

The red line is the top of the bare post (stage 1). A tyre more than ~3 % off it → regenerate that
stage with #5 attached again, or rescale only that file with `--file-scale <name>=<scale>`.

**5. Commit the masters here** (the game atlas records this repo's sha):

```bash
git add masters/farm/crops masters/farm/trees/dragon-fruit
git commit -m "assets: T3 regen corn s04-s05, carrot s05, rice s01, dragon fruit on a concrete post"
```

**6. Rebuild the game atlas and check:**

```bash
cd /Users/kelvin/Projects/yudgnahk/mayhoa
uv run tools/prep_sprites.py          # its log must list the 9 *_v02 files
npm run typecheck && npm test && npm run build
npm run dev                           # http://localhost:5173/  (add ?crops=3d to compare)
```

Then hand back to Claude for the Playwright screenshots (desktop 1280x720, mobile 390x844) and
to tick T3 in `docs/slice/TASKS.md`.
