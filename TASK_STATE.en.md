# TASK_STATE — handoff for the 2026-09-05/07 sessions

**Language:** [Tiếng Việt](TASK_STATE.vi.md) · English

> Read this file before doing anything. Update it when the state changes, or delete it once the regeneration queue is empty.
>
> **Update 2026-09-10:** PR #2 and PR #3 are both merged, `master` is at `795e0b0`. The "Where we are" section below is a snapshot of the 09-05/07 session, kept as history.

## Current goal

Bring the 19 asset packs (95 files) in line with the geometry contract, then work off the rest of the regeneration queue.
Source of truth for every number: `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.en.md`.
Work status: `ASSET_GEOMETRY_FIX_CHECKLIST.en.md` — **section 9 is the most recent QC round**.

## Where we are

- Branch `fix/geometry-qc-2026-09-05`, **12 commits**, pushed.
- **PR #2**: https://github.com/yudgnahk/mayhoa-asset/pull/2 — ~~not merged~~ **merged 2026-09-05**.
- ~~`master` is still at `dd224e1`~~ → `master` is now at `795e0b0` (after PR #3 `assets/durian-pack`, merged 2026-09-09).
- Working tree clean.

QC result: geometry core (canvas / contactY Δ0 / rootX / RGBA8) **PASS on 95/95 plant files**, no regression against the 26-08 normalize pass.

## Done in this session

| | |
|---|---|
| `carrot` s04 | margin 22px → 26px (re-normalized from the original `5276109`, scale 0.9004) |
| `geometry_audit.py` | fixed a bug that swallowed files after hitting a corrupt PNG; +7 tests |
| 5 soil tiles | palette → RGBA8, lossless, verified 100% pixel-for-pixel |
| `soil_tilled` | regenerated as `v02` (v01 has permanently corrupted IDAT data) |
| 3 doc gaps | `rubber` / `water-mimosa` / `water-spinach` had been normalized but were never recorded |
| Vietnamese species names | `thien-ly` → `tonkin-jasmine`, `ngo-gai` → `culantro` |
| `tools/build_atlas.py` | new, 33 tests, idempotent — atlases are reproducible now *(2026-09-10: canvas/anchor guards added, 42 tests)* |
| 4 runtime atlases | grouped by class, replacing the 5 old atlases |
| Asset transport | dropped the Google Drive + `gws` leg entirely |

## Still open — 7 items

**Need the image generation pipeline** (queue in checklist section 6, specs+prompts ready in `FARM_REGENERATION_PROMPTS.en.md`):
- `carrot` s05 — harvest cue too weak (~10px at display size)
- `tonkin-jasmine` whole pack — switch to a trellis-climbing vine form (Profile C, like dragon-fruit)
- `lotus` s05 — shrink the lotus flower to 60–70%
- **`6 fruit trees`** — species-specific silhouettes. *Most worth doing*: verified by eye, the mango and rambutan canopies are nearly identical, differing only in fruit color.

**Need the game environment** (the game code does not exist yet):
- Playground: stage transitions, root must not jump during sway
- Confirm the engine pins the crop anchor to the plate center, matching `(0.5, 0.89453125)`

## How to run the image generation pipeline

**This has changed. Do not use Google Drive, do not use `gws`** (the `gws` token has been revoked, and it is no longer needed).

1. The Claude Code session must be started with `claude --chrome` — the browser tool **cannot be enabled mid-session**.
2. Already available: tmux session **`chromebridge`** in Paseo terminal `f023b260-b6de-497a-b07c-40dc566ef23e`, bridge still alive (checked 2026-09-07).
3. Drive it with `tmux send-keys -t chromebridge ...` + `tmux capture-pane -p -t chromebridge`.
   **`mcp__paseo__send_terminal_keys` CANNOT send arrow keys** — only `Enter`/`Escape`/`BSpace`.
4. One ChatGPT message: `@Create image` + prompt + reference image.
5. Open the image in the **fullscreen viewer**, click **"Save"** (not "Download", and this button does not exist in the chat pane) → it lands in `~/Downloads`.
6. Identifying the new file — set the marker BEFORE clicking Save:
   ```bash
   MARK=$(mktemp); touch "$MARK"
   find ~/Downloads -name 'ChatGPT Image*.png' -newer "$MARK" -print0 | xargs -0 ls -tr
   ```
7. Raw files go to `.ai-bridge/<species>/`, then QC, normalize, and only then into `masters/`.

Full details: the "Asset sync transport" section in `FARM_ASSET_GENERATION_PLAN.en.md`.

## Pitfalls already paid for — do not trip again

**The reference decides the output geometry.** Attaching `soil_empty` (a 2.15:1 plate) as the reference made Create Image produce a 2.13:1 plate while the target group was 1.71:1 — two wasted generation rounds. **Only attach references that belong to the exact geometry group you want to match.**

**Do not infer content from geometry measurements.** A QC agent saw the `water-mimosa` and `water-spinach` bboxes matching within 1px and concluded the artwork might be duplicated. Opening the images shows two clearly different species. The bboxes match only because both were normalized to the same canvas/anchor.

**Bottom-band `rootX` is meaningless for rosette/aquatic morphology** (spec §7.1). Using it as `anchorX` makes `culantro` slide 37px sideways on every stage change. `anchorX` is **always = 0.5**; only `contactY` is measured. `build_atlas.py` already does this correctly and prints a `NOTE QC` for the species that deviate.

**Running `normalize_pack.py` on `water-mimosa`/`water-spinach` without a `--rootx` override will break alignment that is already correct** (it shifts s02 by about −90px). Both packs ALREADY meet the standard, anchor `(384, 728)`.

**Normalization must start from the original artwork**, never stack another transform on top of the current master. The stage-05 margins for `rubber`/`mango`/`pomelo` are at 25px, only 1px of cushion — one more resample drops them below the 24px threshold.

**The Claude-in-Chrome bridge**: the wrapper `~/.claude/chrome/chrome-native-host` is pinned to a version and regenerates itself every time `claude --chrome` runs. **Do not hand-edit it** (edits get overwritten anyway). After a CLI auto-update: run `claude --chrome` once, then `/chrome` → **"Reconnect extension"** (a mandatory step, not a fallback). The `/chrome` panel reporting `Status: Enabled` does **not** mean it is connected — only trust `pgrep -fl chrome-native-host`.

## Frequently used commands

```bash
python3 tools/geometry_audit.py masters/farm/<class>/<species>/*.png
python3 tools/build_atlas.py --dry-run          # show the plan
python3 tools/build_atlas.py                    # rebuild the 4 atlases
python3 -m unittest discover -s tools -p 'test_*.py'   # 42 tests
```

Atlases are a **build product** — edit the masters and re-run the script, do not hand-edit an atlas.

## Decisions settled in this session (do not reopen without a new reason)

- Atlases are grouped **by class**, named `<domain>_<class>_v01`. The old core/herb split reflected production phases, not what is needed at load time.
- Frame key = **slot id** `<species>_stage-0N`. Stage labels differ between species (`coffee`→berry, `rubber`→tapping), so a label-carrying key would force the game into a lookup table. The semantics moved to `stageNames`.
- Soil frame keys use the full stem (`soil_dry`), breaking the rule above — deliberately.
- `mango`/`rambutan` s05 being smaller than s04: **accepted**, because the s04 flower cluster disappears, not because the tree shrank.
- `water-mimosa` vs `water-spinach`: **PASS**, two clearly different species.
