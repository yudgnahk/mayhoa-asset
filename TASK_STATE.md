# TASK_STATE — session handoff

> Read this before doing anything. Update it when state changes, or delete it once the
> regenerate queue is empty.
>
> **2026-09-10:** PR #2 and PR #3 are both merged; `master` sits at `795e0b0`. The
> "Where things stand" section below is a snapshot of the 09-05/07 session, kept as history.

## Session 2026-09-12 — branch merge, tool pack cleanup, docs go English-only

**Branch layout was split in two and is now merged.** Gate A work had been landing on
`fix/durian-rescale-and-atlas-guard` while doc work landed on
`assets/downloads-sync-2026-09-12`; neither branch had the other's commits. Merged at
`97a2230` (`--no-ff`, zero conflicts — the two branches touched disjoint file sets).
All 11 Gate A commits are now ancestors of HEAD. Work on the merged branch from here.

**Tool pack is now contract-clean.** Every file in `masters/farm/tools/` is 512×512 per
geometry contract §4, verified with `geometry_audit.py`:

| Asset | State |
|---|---|
| `tool_hoe_*_v02` | Normalized to 512 (`--mode center --margin 34`), `selected` re-derived from the normalized idle. `v01` deleted. |
| `tool_pest-catcher_*_v01` | Normalized + `selected` derived. Renamed from `tool_pest-net` to match the spec. |
| `tool_watering-can_*_v01` | Already correct. |

Three files had been imported into `masters/` as raw 1254×1254 downloads that had never
been through `normalize_pack`. None of this cost a generate round — the source PNGs were
already on disk.

Note: tools are **not** part of any atlas. `build_atlas.py` builds `farm_crops`,
`farm_trees`, `farm_aquatic` and `farm_soil` only, so the mixed-canvas guard never saw
these files. The contract violation was real; the predicted atlas build failure was not.

**Queue: empty — the Gate A brief is fully generated** *(2026-09-12)*. `harvest_hand` was the
last asset; it passed §5.6 acceptance (a glove, no arm past the cuff, holding nothing) and its
`selected` was derived offline. Artwork for P0-2 and P0-3 is complete:

| Pack | Files |
|---|---|
| `pest_caterpillar-single` | `present`, `cleared` |
| `tool_hoe` | `idle_v02`, `selected_v02` |
| `tool_watering-can` | `idle_v01`, `selected_v01` |
| `tool_pest-catcher` | `idle_v01`, `selected_v01` |
| `tool_harvest-hand` | `idle_v01`, `selected_v01` |

All ten are 512x512 RGBA with margins >= 30px. **This is "artwork done", not "verbs unblocked
in game"** — see the OPEN GAP below: nothing loads these yet.

**RESOLVED — Chrome now downloads straight into `.ai-bridge/incoming`,** inside the repo, so
the TCC problem below no longer blocks the pipeline. Verified end to end on `harvest_hand`:
the file landed at the expected byte count and was read without any permission error. Kept
for the record:

**(was) BLOCKER — the agent holding the Chrome bridge cannot read `~/Downloads`.** macOS TCC
(Privacy → Files and Folders), not POSIX permissions: `ls ~/Downloads` returns
`Operation not permitted` even with the sandbox off, while `stat` shows `drwx------ kelvin`.
It changed mid-session. Fix chosen: point Chrome's download directory at
`.ai-bridge/incoming` (already created and gitignored) so files land outside the TCC-gated
tree and drop the `~/Downloads` hop entirely. **This needs a human** —
`chrome://settings/downloads` → Location → Change, on **Profile 1**. Extensions cannot
drive `chrome://` pages, and editing `Preferences` while Chrome runs gets overwritten.

**Correction to the previous session's blocker.** The 2026-09-11 entry blamed Chrome for
silently blocking downloads after the first file. That was wrong. The files had landed;
the verification step was checking too early and the wrong conclusion stuck. `chatgpt.com`
now has `automatic_downloads` set to allow on Profile 1, which does no harm but was not
the cause.

**OPEN GAP — pest and tool assets have no runtime path.** Found 2026-09-12 while
verifying the atlas claim above. `build_atlas.py` declares exactly four `AtlasSpec`
entries (`farm_crops_v01`, `farm_trees_v01`, `farm_aquatic_v01`, `farm_soil_v01`) and
`runtime/` holds only those four. Nothing references `masters/farm/pests/` or
`masters/farm/tools/`, so the 2 pest files and 6 tool files that have passed QC cannot
reach the game.

The consumer side is equally unbuilt — checked in `mayhoa-farm-demo`:
`src/assets/loader.ts` only knows `parseCropAtlas` and `parseSoilAtlas`, and
`src/render/cues.ts` still draws the pest procedurally (a tinted circle with an X) and
the tool cursor as a diamond outline. Both are placeholders, not sprites.

So this is not "add one AtlasSpec line". It spans both repos:
1. Extend `build_atlas.py` to handle a non-`<species>_stage-0N` structure, with tests.
   Tools are UI icons — anchor `(0.5, 0.5)`, no lifecycle, key `<tool>_<state>`. Pests are
   foliage overlays — also center-anchored, also no lifecycle. Neither fits the current
   `AtlasSpec` assumption of `<class>/<species>/<species>_stage-0N_*.png`.
2. Add the matching format + loader on the demo side.
3. Replace the placeholder drawing with real sprites.

**Do not guess the design.** `README.md` §1 puts the integration contract in the twin
`mayhoa` repo, so how the runtime wants to load pest/tool (own atlas? loose sprites?
manifest?) has to come from there before anyone writes code. Deliberately left uncoded
2026-09-12.

Note that `FARM_MISSING_ASSET_PLAN.md` frames the milestone as "Gate A **asset**-complete",
which may mean this repo's duty legitimately ends at `masters/`. That boundary is itself
unresolved — this repo does ship four runtime atlases.

**Docs are English-only as of this session.** The parallel `.vi.md` set has been removed
and `.en.md` files renamed to plain `.md`. See `README.md` §1.

---

## Session 2026-09-11 — Gate A pest + tool

Queue: `.ai-bridge/GATE_A_GEN_BRIEF.md`. Prompt spec: `FARM_GATE_A_PEST_TOOL_PROMPTS.md`.

**Done:**
- `pest_caterpillar-single` — `present` + `cleared`, 512×512, QC'd composited over
  rice/corn/carrot at a 192px cell. P0-2 closed.
- `tool_hoe` — `idle` + `selected`.

**Two pipeline changes from that session — read before generating again:**

- **Fake alpha is a Work-mode symptom, not a platform change.** *(corrected 2026-09-12)*
  A **Work**-mode thread returns colortype 2 with a checkerboard painted into the pixels; a
  thread in the mayhoa project on **Chat** mode returns real RGBA. Check the colour type first
  and run `python3 tools/dechecker.py raw.png out.png` only when it reads 2
  before anything else. It flood-fills from the edge (a plain color key punches holes
  through white eyes in the sprite) and then difference-mattes the fringe. The viewer's
  `Remove BG` button produces nothing usable.
- **Tool `selected` state is never generated.** The model cannot hold pose and scale
  steady, so the icon jumps in the toolbar. Derive it with `tools/make_selected.py` from
  the idle master. Because the glow bleeds past the silhouette, normalize tool idles with
  `--margin 34`.

Not yet started from the brief: `carrot` s05 (optional), 4 backgrounds, tree/aquatic,
weed, the remaining 5 pests.

---

## The goal being pursued

Bring 19 asset packs (95 files) in line with the geometry contract, then finish the
regenerate queue. Source of truth for every number:
`MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.md`. Work status:
`ASSET_GEOMETRY_FIX_CHECKLIST.md` — **section 9 is the most recent QC pass**.

## Where things stand

- Branch `fix/geometry-qc-2026-09-05`, **12 commits**, pushed.
- **PR #2**: https://github.com/yudgnahk/mayhoa-asset/pull/2 — merged 2026-09-05.
- `master` now at `795e0b0` (after PR #3 `assets/durian-pack`, merged 2026-09-09).

QC result: geometry core (canvas / contactY Δ0 / rootX / RGBA8) **PASS on 95/95 plant
files**, no regression against the 26-08 normalize pass.

## Done in the 09-05/07 session

| | |
|---|---|
| `carrot` s04 | margin 22px → 26px (re-normalized from original `5276109`, scale 0.9004) |
| `geometry_audit.py` | fixed a bug that swallowed files after hitting a corrupt PNG; +7 tests |
| 5 soil tiles | palette → RGBA8, lossless, verified pixel-for-pixel |
| `soil_tilled` | regenerated as `v02` (v01 has permanent IDAT corruption) |
| 3 doc gaps | `rubber` / `water-mimosa` / `water-spinach` were normalized but never recorded |
| Vietnamese species names | `thien-ly` → `tonkin-jasmine`, `ngo-gai` → `culantro` |
| `tools/build_atlas.py` | new, 33 tests, idempotent — atlases are reproducible now *(2026-09-10: canvas/anchor guard added, 42 tests)* |
| 4 runtime atlases | grouped by class, replacing the 5 old ones |
| Asset transport | Google Drive + `gws` hop removed entirely |

## Still open — 7 items

**Need the image pipeline** (checklist section 6; specs and prompts ready in
`FARM_REGENERATION_PROMPTS.md`):
- `carrot` s05 — harvest cue too weak (~10px at display size)
- `tonkin-jasmine` whole pack — convert to trellis vine form (Profile C, like dragon-fruit)
- `lotus` s05 — shrink the bloom 60–70%
- **`6 fruit trees`** — species-distinct silhouettes. *Highest value*: checked by eye, the
  mango and rambutan canopies are nearly identical and differ only in fruit color.

**Need the game environment** (game code does not exist yet):
- Playground: stage transition, root must not jump during sway
- Confirm the engine pins the crop anchor to the plate center, matching `(0.5, 0.89453125)`

## Running the image pipeline

**This changed. No Google Drive, no `gws`** (the `gws` token is revoked and is no longer needed).

1. The Claude Code session must be started with `claude --chrome`. Browser tools **cannot
   be enabled mid-session**, and `claude -p --chrome` does **not** work either — verified
   2026-09-12, a print-mode session gets zero `mcp__claude-in-chrome__*` tools even while a
   bridged interactive session is live on the same machine. The bridge is per-session and
   non-inheritable.
2. An agent without the bridge hands the work to the interactive session over
   `SendMessage` instead of trying to drive Chrome itself.
3. One ChatGPT message: `@Create image` + prompt + reference image.
4. Open the image in the **fullscreen viewer** and click the **download icon in the
   top-right header**, next to Share. The middle toolbar (Markup / Comment / Remove BG /
   Erase / Resize) has no download control, and neither does the chat pane. *(Before
   2026-09-12 this was a "Save" button on the Remove BG / Erase bar — the UI changed.)*
5. Identify the new file — set a marker **before** clicking download:
   ```bash
   MARK=$(mktemp); touch "$MARK"
   find <download-dir> -name 'ChatGPT Image*.png' -newer "$MARK" -print0 | xargs -0 ls -tr
   ```
6. Raw goes to `.ai-bridge/<species>/`, then QC, then normalize, and only then `masters/`.

Full detail: `GEN_IMAGE_WORKFLOW.md`, and the "Asset sync transport" section in
`FARM_ASSET_GENERATION_PLAN.md`.

## Pitfalls already paid for — do not repeat

**The reference image dictates output geometry.** Attaching `soil_empty` (a 2.15:1 plate)
as reference made Create Image return a 2.13:1 plate when the target group was 1.71:1 —
two wasted generate rounds. **Only attach references from the geometry group you want to
match.**

**Do not infer content from geometry numbers.** A QC agent saw the `water-mimosa` and
`water-spinach` bounding boxes agree to within 1px and concluded the artwork might be
duplicated. Opening the images showed two clearly different species. The boxes matched
only because both were normalized to the same canvas and anchor.

**The same trap, seen again 2026-09-12:** four files in `~/Downloads` sharing one md5 were
read as "the Save step is grabbing a stale image". In fact only one generate had ever
happened for that asset, and it had been downloaded four times. Identical bytes were the
expected result. Check whether a new generate actually occurred before blaming the
transport.

**The real grab hazard runs the other way:** fetching the image before the new one has
finished loading picks up the *previous* `img` in the DOM. That is how a watering-can file
once came back from a bug-net generate. Guard by comparing bytes or asset id against the
previous image and only trusting the result once it differs — file names carry a fresh
timestamp even when the contents are stale, so names prove nothing.

**Bottom-band `rootX` is meaningless for rosette/aquatic morphology** (spec §7.1). Using it
as `anchorX` slides `culantro` 37px sideways on every stage change. `anchorX` is **always
0.5**; only `contactY` is measured. `build_atlas.py` already does this and prints `NOTE QC`
for species that skew.

**Running `normalize_pack.py` on `water-mimosa`/`water-spinach` without a `--rootx`
override destroys alignment that is already correct** (it shifts s02 by about −90px). Both
packs already meet the contract at anchor `(384, 728)`.

**Normalize must start from the original artwork**, never stack a transform on the current
master. Stage-05 margins for `rubber`/`mango`/`pomelo` sit at 25px with only 1px of
cushion — one more resample drops them under the 24px threshold.

**Claude-in-Chrome bridge**: the wrapper `~/.claude/chrome/chrome-native-host` is
version-pinned and regenerates every time `claude --chrome` starts. **Do not hand-edit it**
(the edit is overwritten). After a CLI auto-update: run `claude --chrome` once, then
`/chrome` → **"Reconnect extension"** — mandatory, not a fallback. The `/chrome` panel
reporting `Status: Enabled` does **not** mean connected; trust only
`pgrep -fl chrome-native-host`.

**A mid-session CLI auto-update does not kill a live bridge, but it arms the trap.** The
wrapper regenerates to the new version while the running native host is still the old
binary; the live session keeps working because it matches the *running* host, and the skew
only bites on the next `--chrome` launch. If a long generate session is mid-queue when the
CLI updates, finish the queue first, then do the relaunch + Reconnect.

## Commands in regular use

```bash
python3 tools/geometry_audit.py masters/farm/<class>/<species>/*.png
python3 tools/build_atlas.py --dry-run          # show the plan
python3 tools/build_atlas.py                    # rebuild all 4 atlases
python3 -m unittest discover -s tools -p 'test_*.py'   # 67 tests
python3 tools/dechecker.py raw.png out.png            # rebuild alpha from the checkerboard
python3 tools/make_selected.py idle.png selected.png  # derive a tool icon's selected state
```

Atlases are a **build product** — edit the master and re-run the script; never hand-edit
an atlas.

## Decisions settled in session (do not reopen without new information)

- Atlases group **by class**, named `<domain>_<class>_v01`. The old core/herb split
  reflected production phases, not load-time needs.
- Frame key = **slot id** `<species>_stage-0N`. Stage labels diverge between species
  (`coffee`→berry, `rubber`→tapping), so a label-bearing key would force the game to
  consult a lookup table. Semantics live in `stageNames` instead.
- Soil frame keys use the full stem (`soil_dry`), deliberately breaking the rule above.
- `mango`/`rambutan` s05 being smaller than s04 is **accepted** — the s04 flower cluster
  disappears; the tree is not shrinking.
- `water-mimosa` vs `water-spinach`: **PASS**, they are clearly different species.
