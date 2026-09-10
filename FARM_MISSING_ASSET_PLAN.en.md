# Mayhoa — Farm Missing Asset Plan

**Status:** Ready to generate
**Language:** English · [Tiếng Việt](FARM_MISSING_ASSET_PLAN.vi.md)
**Inventory date:** 2026-09-08

## Status and relationship to other documents

This document lists **the assets still missing before the game can run**, derived by comparing the current `masters/` tree against the Gate A / Gate B requirements in the `mayhoa` repo (`FARM-V1-SPEC.md` §3, `FARM-CONTENT.md` §1, `FARM-DEMO-BRIEF.md` §4).

How it differs from the documents already here:

- `FARM_ASSET_GENERATION_PLAN.en.md` lists assets by **art category** (soil, crops, trees, weeds, pests, tools). This document lists them by **what is blocking gameplay**.
- `FARM_REGENERATION_PROMPTS.en.md` covers assets that **exist but do not pass**. This document covers assets that **do not exist at all**.
- `FARM_REMAINING_PLANT_ASSET_PLAN.en.md` finished the plant work; this document continues for everything that is not a plant.

This is a temporary document: delete it once every P0 and P1 item is done.

---

## 1. Inventory conclusion

107 master PNGs have been produced, and **all of them are plants or soil tiles**. There is not one asset for environment, UI, effects, pests, or tools.

Gate A needs roughly 21 of those 107 files. **80% of production so far sits outside what is blocking the path.** This ratio has got **worse** since the 2026-09-08 inventory (79% of 102 files) because the `durian` pack merged on 2026-09-09 is another tree. This is the numeric expression of the `C-ART-02` conflict.

| Group | State | Gate that needs it | Spec exists? |
|---|---|---|---|
| Soil, 6 states | ✅ Done | A | — |
| D-008 crops (rice, corn, carrot) | ✅ Done | A | — |
| `carrot` stage-05 | ⚠️ Geometry passes, **gameplay fails** | A | ✅ `FARM_REGENERATION_PROMPTS.en.md` §B |
| **Pest** | ❌ Missing | **A** | List only (Phase 10), no detailed spec |
| **Tool** | ❌ Missing | **A** | List only (Phase 11), no detailed spec |
| **Farm scene / environment** | ❌ Missing | **A** | ❌ **not in the taxonomy** |
| **Plot overlay** | ❌ Missing | **A** | ❌ none |
| **Interaction FX** | ❌ Missing | **A** | ❌ none |
| **Inventory icons** | ❌ Missing | **A** | ❌ none |
| **Water surface / aquatic tile** | ❌ Missing | depends on scope | ❌ §6.2 calls it a "separate system" that does not exist |
| **Buildings + economy UI** | ❌ Missing | B | ❌ none |
| Weeds | ❌ Missing | not required | List only (Phase 9) |

**Five groups are absent from the generation plan's §2 taxonomy:** environment/scene, water system, UI icons, interaction FX, and buildings. The taxonomy currently holds only `soil / crops / aquatic-crops / trees / weeds / pests / tools`. Extend the taxonomy before generating any of these.

---

## 2. P0 — Blocks Gate A acceptance

### P0-1 · `carrot` stage-05

Already in the regeneration queue, but **filed at the wrong priority as "polish"**. It actually blocks an acceptance test in `FARM-DEMO-BRIEF.md` §5: *"players can distinguish ready crops at normal zoom"*. Carrot is `crop_tutorial`, the first crop a player ever sees, and its ready cue is currently about 10px at display size. The spec is ready in `FARM_REGENERATION_PROMPTS.en.md` section B.

### P0-2 · Pest pack

Gate A requires **exactly one** pest type (`FARM-CONTENT.md` §1; `FARM-V1-SPEC.md` §3 lists "pest handling" as a verb). Phase 10 lists six variants, which is **more than Gate A needs**. One is enough to unblock the gate.

| Requirement | Value |
|---|---|
| First choice | `caterpillar_single` — reads best at small size, works on any foliage |
| Master canvas | `512×512` transparent, same camera angle and upper-left lighting |
| Anchor | overlay anchored to foliage, **not** to the root — do not reuse the crop anchor |
| States | at least 2: `idle` and cleared/removed |
| Acceptance | legible in a `192px` cell over rice (tall foliage), carrot (low rosette) and corn (upright stalk); must not hide the crop's own stage cue |
| Constraint | never bake the plant into the pest sprite, nor the pest into a plant master |

The remaining five Phase 10 variants stay scheduled after Gate A.

### P0-3 · Tool pack

Gate A needs a minimal tool UI (`FARM-DEMO-BRIEF.md` §4). Phase 11 lists five tools; Gate A only exercises five actions: till, plant, water, pest, harvest.

| Tool | Required for Gate A? |
|---|---|
| `watering_can` | ✅ the water action |
| `harvest_hand` | ✅ the harvest action |
| `pest_catcher` | ✅ the pest action |
| `hoe` / tilling implement | ✅ the till action — **missing from Phase 11**, which lists `shovel` but no implement that breaks a furrow |
| `pruning_shears` | ❌ defer |

Tools are judged at **UI interaction size**, never at crop/tree world scale. Each tool needs an `idle` and a `selected`/active version so `FARM-INTERACTION.md` §4 can keep the current tool visible.

---

## 3. P1 — Needed for Gate A, no spec yet

### P1-1 · Farm scene / environment

**This is the largest gap and nobody had recorded it.** `FARM-V1-SPEC.md` §3 requires *"one Farm scene"*, and D-010 fixes the field at **35 cells in a 7 × 5 diagonal layout**. Today there is only one repeating soil tile and nothing that makes those 35 cells read as a field.

Minimum needed:

- ground/grass base outside the cultivated area, tileable without a visible repeat;
- a field boundary or bund that delimits the 7 × 5 block;
- at least one surrounding layer so the frame has an edge, rather than cells floating in empty space;
- the same camera angle and upper-left lighting as the rest of the pack.

Not needed yet: buildings, decorative fencing, weather, day/night.

### P1-2 · Plot overlay

`FARM-CONTENT.md` §1 requires *"crop-compatible plot overlays"*. This means cell-state layers independent of the plant sprite: selected cell, valid cell during a batch drag, invalid cell. `FARM-INTERACTION.md` §4 requires invalid targets to explain themselves through shape and colour and **never** open a modal.

### P1-3 · Interaction FX

`FARM-INTERACTION.md` §3 mandates feedback per action:

| Action | Required feedback |
|---|---|
| Till | soil breaks, darkens, changes edge shape — may be satisfied by a soil state change |
| Water | water arc / splash, then the wet-soil state |
| Harvest | the crop reacts, the item count rises |
| Pest | the pest leaves, foliage settles |

A binding constraint from `FARM-INTERACTION.md` §5: a ready crop must **not** be signalled by a floating icon over every plot. The ready cue has to live in the crop artwork itself, which is also why P0-1 is an acceptance blocker rather than polish.

### P1-4 · Inventory icons

UI-size item icons, separate from world sprites: the three harvested goods (rice, corn, carrot) and their three seed packets. Gate A has a minimal inventory; the full item set belongs to Gate B.

---

## 4. P2 — Gate B, nothing exists

`FARM-V1-SPEC.md` §3 Gate B needs a shared warehouse, **one** processing building, a production queue, up to three processed goods, one order surface, coins and progression, and basic plot expansion.

No asset exists for any of it. A detailed spec can wait until Gate A passes, but the gap should be visible now so the earlier mistake is not repeated: **do not generate more plant species before this group exists.**

---

## 5. Water surface — open decision

`FARM_ASSET_GENERATION_PLAN.en.md` §6.2 states that the water surface, pond edge and ripple FX belong to *"a separate environment/water system"*. **That system does not exist**: it is not in the §2 taxonomy, has no phase, and has no files.

Consequence: the 15 finished aquatic masters **cannot be placed in the game**, because there is no water for them to sit on. Priority depends on whether the `mayhoa` repo brings aquatic crops into Farm V1 scope.

---

## 6. Recommended order

```text
P0-1 carrot s05      → unblocks an acceptance test
P0-2 pest ×1         → unblocks the pest-handling verb
P0-3 tool ×4         → unblocks the tool UI
P1-1 farm scene      → unblocks "one Farm scene"
P1-2 plot overlay    → unblocks selection and batch feedback
P1-3 interaction FX  → unblocks the immediate-feedback criterion
P1-4 inventory icons → unblocks the minimal inventory
────────────── Gate A asset-complete ──────────────
P2   buildings + economy UI
     water system (if aquatic enters scope)
     weeds, the other 5 pests, the last tool
```

This order **supersedes** §17 of the generation plan until Gate A passes. Adopting it is what closes the `C-ART-02` conflict currently OPEN in the `mayhoa` repo.

---

## 7. What is NOT missing

Recorded so nobody redoes it:

- 6 field crops × 5 stages, packed, anchor `(0.5, 0.89453125)`;
- 10 trees × 5 stages, atlas cell `256×256`, **packed into the atlas**;
- `durian` (the 11th tree) has 5 masters but is **NOT packed into the atlas and FAILS geometry** — see `ASSET_GEOMETRY_FIX_CHECKLIST.en.md` section 10;
- 3 aquatic crops × 5 stages;
- 6 soil states, RGBA8, with `soil_tilled` served by `v02`;
- a reproducible atlas pipeline in `tools/build_atlas.py`, 33 tests, idempotent;
- the geometry contract, locked and mirrored in both repos.
