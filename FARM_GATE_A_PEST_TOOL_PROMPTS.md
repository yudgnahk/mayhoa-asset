# Mayhoa — Gate A: pest + tool prompt spec

**Status:** Phase A (prompts) — settled before generating
**Queue source:** `.ai-bridge/GATE_A_GEN_BRIEF.md`, `FARM_MISSING_ASSET_PLAN.md` §P0-2 / §P0-3
**Related specs:** `MAYHOA_ART_STYLE_SPEC.md`, `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.md`

`FARM_MISSING_ASSET_PLAN.md` records pest and tool as "listed, but missing a detailed
spec". This is that spec. It covers the **10 Gate A files** only; the remaining 5 pests and
1 tool from Phase 10/11 come later.

---

## 1. Output table

| # | Asset | File | Canvas | Status (2026-09-12) |
|---|---|---|---:|---|
| 1 | pest present | `masters/farm/pests/pest_caterpillar-single_present_v01.png` | 512 | Done |
| 2 | pest cleared | `masters/farm/pests/pest_caterpillar-single_cleared_v01.png` | 512 | Done |
| 3 | hoe idle | `masters/farm/tools/tool_hoe_idle_v02.png` | 512 | Done (v02; v01 dropped) |
| 4 | hoe selected | `masters/farm/tools/tool_hoe_selected_v02.png` | 512 | Done (derived) |
| 5 | watering can idle | `masters/farm/tools/tool_watering-can_idle_v01.png` | 512 | Done |
| 6 | watering can selected | `masters/farm/tools/tool_watering-can_selected_v01.png` | 512 | Done (derived) |
| 7 | pest catcher idle | `masters/farm/tools/tool_pest-catcher_idle_v01.png` | 512 | Done |
| 8 | pest catcher selected | `masters/farm/tools/tool_pest-catcher_selected_v01.png` | 512 | Done (derived) |
| 9 | harvest hand idle | `masters/farm/tools/tool_harvest-hand_idle_v01.png` | 512 | **Remaining — needs a generate** |
| 10 | harvest hand selected | `masters/farm/tools/tool_harvest-hand_selected_v01.png` | 512 | Remaining (derive after #9) |

Names follow the generation plan's §11 pattern `<asset>_<state>_v<nn>.png`
(`tool_watering-can_idle_v01.png`).

The pest catcher was briefly committed as `tool_pest-net_*`; it was renamed to
`tool_pest-catcher_*` to match this spec and the Gate A queue.

---

## 2. Decisions settled in phase A

**`hoe` is a real tilling tool, not a temporary remap to `shovel`.** Phase 11 has no hoe;
the brief allows a temporary remap but it is not needed — a flat blade at a right angle to
the handle is a distinct silhouette, readable against a shovel at UI size. Phase 11 should
add `hoe` to its list.

**`selected` is NOT generated — derive it with `tools/make_selected.py`.**
*(revised 2026-09-11, after trying to generate it.)* The requirement is the same object,
same pose, same silhouette, with only the rendering changed: `FARM-INTERACTION.md` §4 needs
the toolbar to show *the currently selected tool*, and a silhouette that shifts between
states makes the icon jump when the player clicks. The model cannot hold that steady — the
generated `selected` hoe came back off in both pose and scale versus `idle`. So `selected`
is now a deterministic transform on the idle master itself: a warm golden rim light on the
upper-left edge, a warm glow, and a slight lift in brightness and saturation. Pixel-identical
silhouette, and half as many generate rounds.

Geometry consequence: the glow bleeds a few px past the silhouette, so **tool idles are
normalized with `--margin 34`** (not 24) so that `selected` still clears a ≥24 margin. Do
not re-normalize `selected` — that scales it smaller than `idle` and the icon jumps again.

**`cleared` is not an empty sprite.** Draw a soft dust puff plus the caterpillar curled up
and knocked aside, about 55% smaller. `FARM-INTERACTION.md` §3 specifies the pest response
as *"the caterpillar leaves"* — a single static frame that reads that way has to show the
caterpillar leaving, not an empty space.

**Pest anchor is the canvas-center pivot `(0.5, 0.5)`, not root contact.**
`MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.md` §5.5 permits this: a pest is an overlay riding
the foliage, attached by the game to each species' foliage attach point, so the sprite has
no world-contact semantics. Tools also use `(0.5, 0.5)` — a visual pivot per §5.5.

**No contact shadow on tools.** The Shared Style Block allows a "very small soft contact
shadow" because most assets stand on soil. A tool is a UI icon floating in the toolbar; a
shadow under it makes the icon look like it is resting on an invisible surface.

---

## 3. Shared Style Block (paste at the top of EVERY prompt)

Identical to `FARM_REGENERATION_PROMPTS.md` §2, minus the shadow line for tools.

```text
Art style — "Nostalgic Hand-Painted Farm Sprite": a cozy farming-game sprite
inspired by classic 2008–2012 browser/social farm games. Soft painterly
hand-painted rendering with light brush texture; selective soft outlines in
dark green/brown chromatic tones (never pure black, never thick uniform
vector lines); readable silhouette at small gameplay size; cheerful pastel
palette, slightly washed, higher saturation only on focal parts; gentle
shading, light source upper-left; organic asymmetric shapes. NOT
photorealistic, NOT glossy modern mobile art, NOT clean vector/cel-shade,
NOT neon.

Format: single isolated game sprite on a FULLY TRANSPARENT background.
One object only, whole object fully inside frame with margin on all sides.
No ground/soil/scene baked in, no text or watermark, no button or panel
background behind the object.
```

**Negatives, for when the model gets stubborn:** `no background, no soil tile, no scene, no frame, no border, no watermark, no photorealism, no 3D render, no neon colors, no multiple views, no sprite sheet, no UI button behind the object`.

**Reference:** attach `coffee_stage-05_berry_v01.png` as the single style anchor, with an
explicit note *"style only — the object I want is different and much smaller"*. Do not
attach a soil tile or a plant master as a geometry reference: the trap already paid for in
`TASK_STATE.md` is that the reference dictates output geometry, and pest/tool belong to
neither the plate nor the plant geometry group.

---

## 4. Pest — `caterpillar_single`

### 4.1 Shared constraints

- Do not bake a plant, leaf or soil tile into the sprite. Do not bake the pest into a plant master.
- Must read clearly composited over rice (tall canopy), carrot (low rosette) and corn
  (upright stem) at a `192px` cell.
- Must not hide the plant's stage signal → keep the caterpillar compact, not spread sideways.
- Cute and readable, **not** realistic insect horror (generation plan §8).
- The body must **not** be pure leaf-green: it disappears against foliage. The focal point
  has to be a warm color.

### 4.2 `present`

```text
A single cute cartoon caterpillar sprite for a farming game, seen from a
slight 3/4 side angle.

Body: a chubby caterpillar made of 6 soft rounded segments, arched upward in
the middle like it is mid-crawl. Body color is a bright lime yellow-green
with slightly darker soft green bands between segments and a few small warm
orange dots along the back. Head is a rounded warm coral-red with two big
friendly cartoon eyes, a tiny smile, and two short soft antennae. Tiny stubby
orange feet under the front segments.

The warm coral head and orange dots are the focal contrast so the creature
stays readable when it sits on top of green foliage. Compact chunky shape,
wider than tall but not stretched into a long thin worm.

Nothing else in the image: no leaf, no branch, no plant, no soil.
```

Acceptance: composited over rice/carrot/corn at 192px the caterpillar still separates from
the foliage; bbox no wider than ~55% of canvas; no leaf or branch fragment anywhere in the
alpha.

### 4.3 `cleared`

```text
A "pest cleared" effect sprite for a farming game: the same cute cartoon
caterpillar as before, but now being knocked away.

The caterpillar is curled into a small comma shape, tilted, tumbling up and
to the right, drawn small — roughly half the size it would be at rest. Its
eyes are closed in a harmless dizzy way, still cute, not hurt or gory. Same
lime yellow-green body with a warm coral head.

Below and left of it, a soft pale mint-white cartoon dust puff made of 3–4
rounded overlapping lobes, plus three small four-point sparkles scattered
around. The puff is soft and airy with gentle painterly edges, semi-opaque.

Nothing else: no leaf, no plant, no soil, no impact lines, no text.
```

Acceptance: reads as "the caterpillar was just cleared away"; the puff is not so opaque it
hides the soil tile; same upper-left lighting as `present`.

---

## 5. Tools — 4 tools × 2 states

### 5.1 Shared constraints

- A gameplay interaction icon, not a realistic illustration (generation plan §9).
- Very clear silhouette, slightly higher contrast than a world asset.
- The 4 tools must be distinguishable from each other **by silhouette alone** at UI size.
- No baked button background, no contact shadow.
- Place the object diagonally, filling most of the frame.

### 5.2 `selected` suffix (append to the idle prompt, leaving the rest unchanged)

```text
State: SELECTED — exactly the same object, same pose, same angle, same
silhouette as the idle version, only lit differently: a warm golden rim light
along the upper-left edges, slightly higher saturation and brightness overall,
and a soft warm glow bleeding just a few pixels outside the object's edge.
Do not change the shape, the pose, the framing, or the size.
```

### 5.3 `hoe`

```text
A farming hoe tool icon sprite for a farming game, seen at a slight 3/4
angle, lying diagonally across the frame with the blade at the lower left
and the handle going up to the upper right.

A wide flat trapezoid steel blade, mounted at a right angle to the end of a
straight wooden handle — clearly a soil-tilling hoe, NOT a shovel and NOT a
pickaxe. The blade is soft warm grey steel with a lightly worn edge and a
hint of dry earth on it; the handle is warm honey-brown wood with a soft
grain and a slightly darker binding collar where blade meets handle.
```

Acceptance: blade at a right angle to the handle (not in line with it like a shovel); one
flat blade (not pointed, not two-pronged).

### 5.4 `watering_can`

```text
A watering can tool icon sprite for a farming game, seen at a slight 3/4
angle, standing upright and slightly turned, spout pointing to the left.

A rounded chubby metal watering can with a soft pastel mint-teal body, a
large rounded carry handle on top, a second small grip handle at the back,
and a long spout ending in a round sprinkler rose head. A warm cream painted
band runs around the belly of the can. Friendly, plump, storybook proportions.

The can is empty and not pouring: no water, no droplets, no splash.
```

Acceptance: a rose head at the spout tip (distinguishes it from a jug or teapot); no water.

### 5.5 `pest_catcher`

```text
An insect-catching net tool icon sprite for a farming game, seen at a slight
3/4 angle, lying diagonally with the net hoop at the upper left and the
handle going down to the lower right.

A round hoop of pale gold metal holding a soft pale cream mesh net bag that
hangs down and slightly to the side with a gentle fabric droop; the mesh is
suggested with a light woven texture and is semi-translucent at its edge. A
straight warm honey-brown wooden handle with a small green cloth grip wrap
near the end.

Empty net: no insect, no butterfly, no caterpillar inside or nearby.
```

Acceptance: an empty round hoop with a softly drooping mesh bag; no insect anywhere in frame.

### 5.6 `harvest_hand`

```text
A harvesting glove tool icon sprite for a farming game: a single chunky
cartoon gloved hand seen at a slight 3/4 angle, tilted diagonally, fingers
curled into a soft open picking gesture as if about to pluck a fruit.

A plump rounded farm work glove in warm cream canvas with soft sage-green
accents on the back of the hand and a rolled green cuff at the wrist. Chunky
storybook fingers, no visible fingernails, no skin — it is a glove. The
opening at the wrist is closed off with a soft dark cuff lining, not an arm.

Just the glove: no arm, no crop, no fruit, no basket.
```

Acceptance: it is a glove (not a bare hand); no arm extending past the wrist; not holding
any produce.

---

## 6. Pipeline after download

**Fake alpha is not universal — check, do not assume.** *(2026-09-12)* Some raws come back
as PNG colour type 2 with a white/grey checkerboard *painted into the pixels* in place of
transparency; `Save` then bakes that checkerboard into the file. Others come back as real
RGBA (colour type 6) and need no repair at all.

**Always read the `IHDR` colour type first**, and run `tools/dechecker.py` only when it reads
2. Never skip that check on the strength of the hypothesis below.

*Working hypothesis, not established:* the split tracked the chat mode. Every one of the 7
model-generated images in the Work-mode thread `/c/6aa2df26-…` was type 2 (the single type-6
file there was a reference image uploaded by hand), while all 3 generated in the Chat-mode
project thread `/g/g-p-…/c/6aa3664c-…` were type 6. Both modes were verified programmatically
at the time, not recalled. But the two threads also differ in **project membership** and in
**date**, so mode is confounded and n is 2 threads. Generating one image in a Work-mode thread
*inside* the project would separate the variables. **The user decided 2026-09-12 not to run
that experiment and to generate in Chat mode only** (`GEN_IMAGE_WORKFLOW.md` A1), so the
question stays open but stops mattering in practice — Chat mode returns type 6. Keep the
colour-type check regardless: a type-2 raw under Chat mode would mean something changed.

1. Raw goes to `.ai-bridge/pests/` or `.ai-bridge/tools/`.
2. Only if `IHDR` colour type is 2: `python3 tools/dechecker.py raw.png out.png`.
3. `python3 tools/normalize_pack.py --mode center --canvas 512 512 --target 256 256 <file>`
   (for tools, add `--margin 34`).
4. Tools: `python3 tools/make_selected.py idle.png selected.png`.
5. `python3 tools/geometry_audit.py` — check canvas, RGBA8, margins.
6. Composite QC: pest over rice/carrot/corn at 192px; tools rendered at UI size.
7. Only promote to `masters/farm/pests/` and `masters/farm/tools/` on PASS.
8. Update `TASK_STATE.md` and §5.5 of the geometry spec (canonical anchor for the two new
   classes).
