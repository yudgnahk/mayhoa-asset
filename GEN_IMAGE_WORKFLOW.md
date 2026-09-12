# Image generation workflow — read this BEFORE running, whichever agent you are

This document is the single source of truth for the chain **ChatGPT Create image → local
disk → QC → `masters/`**. It is written for an agent to read and execute, not for a human
to skim.

`.ai-bridge/` is gitignored, so anything that must travel with the repo lives here, not in
there.

Last verified **2026-09-12** by running the flow for real, not by reading docs.

---

## Step 0 — DETERMINE WHICH LANE YOU CAN RUN (mandatory, before anything else)

Do not guess. Do not infer from the session name. Probe with a tool:

```
ToolSearch  query: "select:mcp__claude-in-chrome__list_connected_browsers"
```

- **Loads** → call `list_connected_browsers`. A browser with `isLocal: true` means
  **LANE A**: you can run the whole flow.
- **No such tool** → **LANE B**. You cannot generate images. Jump to the Lane B section.

### No workarounds

If you are a Paseo agent you will see a `mcp__paseo__browser_*` set (navigate, click, fill,
screenshot…). **Do not use it for this flow.** Verified 2026-09-12: Paseo's browser tools
drive a **clean, logged-out browser** — opening `chatgpt.com` redirects straight to
`chatgpt.com/auth/login`. And **do not log in on the user's behalf**: entering a password or
creating an account is not something an agent does, even with credentials at hand.

A login screen means stop, not try another route.

---

## Who can run which lane (verified 2026-09-12)

| Runner | Has `mcp__claude-in-chrome__*`? | Can generate? |
|---|---|---|
| `claude` interactive in a terminal | Yes | **Yes — Lane A** |
| Paseo agent, provider `claude/*` | **No** | No — Lane B |
| Paseo agent, other provider (`codex/*`…) | No | No — Lane B |
| Subagent / Task tool inside a Lane A session | No | No — Lane B |

A Paseo agent has no bridge because Paseo spawns `claude` through the Agent SDK
(ProcessTransport), not as an interactive session.

The `--chrome` flag does not rescue this: verified 2026-09-12, `claude -p --chrome` exposes
**zero** `mcp__claude-in-chrome__*` tools. Read straight from the `tools` array of the
`init` event under `--output-format stream-json --verbose`: 123 tools, none matching
`chrome` or `browser`, from `/tmp` and from the repo alike.

This is not a machine configuration gap: `~/.claude.json` already has
`claudeInChromeDefaultEnabled: true` and a `chromeExtension.pairedDeviceId`, so an
interactive session does not need the `--chrome` flag. Pairing lives in `~/.claude.json`
(machine-wide), not per session.

### The nested-session workaround is CLOSED — do not retry

Verified 2026-09-12 across three different permission mechanisms, all the same result:

| Attempt | Result |
|---|---|
| `claude -p --chrome` then `list_connected_browsers` | **No tool exists to call** (0 chrome tools) |
| `--allowedTools` listing every chrome tool | **Blocked** |
| `--permission-mode bypassPermissions` | **Blocked** |

**This is not a permissions problem — it is a lifecycle problem.** The bridge binds
per-session to the interactive session the extension attaches to. A `-p` session lives for
seconds and has no UI to attach to, so it never receives a connection. Adding rules to
`settings.json` is pointless: that is exactly the mechanism `--allowedTools` already used
and failed with.

Do not reach for `--dangerously-skip-permissions` either; the equivalent
(`bypassPermissions`) was tried and did not help.

When probing, match tool names by **substring** (`'chrome' in name.lower()`), not by a
`chrome_` / `browser_` prefix — the real prefix is `mcp__claude-in-chrome__`, so a
prefix probe returns a false negative.

### Instead: hand the work to the session that holds the bridge

Claude sessions on the same machine can message each other. A Lane B agent does not drive
Chrome itself — it **hands steps A1–A7 to an interactive session that has the bridge**:

1. `ListAgents` — find the interactive session open on this repo (usually named
   `mayhoa-asset-*`; one has historically sat in the tmux session `mayhoa-chrome`).
2. `SendMessage` to that session with the path of the `TASK.md` to run and the expected
   `incoming/` path.
3. Get on with your own offline work; do not sit and wait.

The session taking the job must run **Step 0** itself to confirm it really has the bridge —
being open is not the same as being connected, and the `/chrome` panel reporting
`Status: Enabled` is not evidence either.

---

## LANE A — run the whole flow

### A0. Preflight (all of it, before opening a tab; every item here has broken a run)

```bash
# 1. Chrome must NOT ask where to save — if true, a native dialog blocks the download
#    and the agent cannot click it (native dialogs are out of an extension's reach).
python3 -c "
import json,os
# Profile 1, NOT Default — the extension and the ChatGPT session live in Profile 1.
d=json.load(open(os.path.expanduser('~/Library/Application Support/Google/Chrome/Profile 1/Preferences')))
print('prompt_for_download =', d.get('download',{}).get('prompt_for_download'))
print('download dir        =', d.get('download',{}).get('default_directory') or '(unset -> ~/Downloads)')
ad=d.get('profile',{}).get('content_settings',{}).get('exceptions',{}).get('automatic_downloads',{})
print('chatgpt automatic_downloads =', [v.get('setting') for k,v in ad.items() if 'chatgpt' in k] or 'NOT SET')"
```

`prompt_for_download = True` → **STOP**, ask the user to open
`chrome://settings/downloads` and turn off "Ask where to save each file". An extension
cannot operate `chrome://` pages and cannot turn this off for them. Editing the
`Preferences` file while Chrome is running gets overwritten — do not try.

`download dir` must point at `<repo>/.ai-bridge/incoming`. If it still points at
`~/Downloads`, **STOP** and ask the user to change it in `chrome://settings/downloads` →
Location → Change. Reason: macOS TCC (Privacy → Files and Folders) can revoke an agent's
read access to `~/Downloads` with no warning and no POSIX symptom — `ls` returns
`Operation not permitted` while `stat` still shows `drwx------ kelvin`. It happened
mid-session on 2026-09-12. `.ai-bridge/incoming` sits outside the TCC-gated tree, so every
agent can read it, and it removes the `mv` hop as a bonus.

`chatgpt automatic_downloads` should be `1`. Set 2026-09-12.

> **Correction, 2026-09-12.** An earlier version of this document claimed Chrome silently
> blocks downloads after the first file unless this is set. That diagnosis was wrong — the
> files had landed; the verification step was looking too early. Keep the setting (it is
> harmless and removes one variable), but if downloads appear to fail, check the disk
> before blaming Chrome.

```bash
# 2. The reference file must actually open. soil_tilled v01 has permanent IDAT corruption.
python3 -c "
from PIL import Image
for p in [<reference paths>]:
    im=Image.open(p); im.load(); print('OK', p, im.size, im.mode)"

# 3. Set a time marker so you can identify the new file later
MARK=$(mktemp); touch "$MARK"
```

### A1. Open the project and start a chat

New tab → `https://chatgpt.com/g/g-p-6a86ae171c34819191aad1a59464472e-mayhoa/project`

Let the page render (the chat area is blank for a few seconds on first load — an early
screenshot shows a black area; that is not a failure). The composer is on the project page
itself, labelled **"New chat in mayhoa"**. Typing there creates a new chat **inside the
project**; you do not need the sidebar's "New chat".

Do NOT close the user's existing tabs. Do NOT restart Chrome.

**Generate in Chat mode, never Work mode — standing decision, 2026-09-12.** Every asset
that came back needing alpha repair came from a Work-mode thread; every Chat-mode generate
returned real RGBA. Chat mode also keeps the thread inside the mayhoa project, which is
where the reference history lives.

Verify the mode before sending anything — do not assume it from the URL:

```
browser_evaluate:
  [...document.querySelectorAll('[role=radio]')].map(e => e.innerText + '=' + e.getAttribute('aria-checked'))
  → expect "Chat=true", "Work=false"
```

If the thread already exists, read the header instead: a Work thread carries a `Work` badge
(`document.querySelector('header').innerText`). A project Chat thread shows only the project
name. Wrong mode → switch it before generating; do not "just try it and check the colour
type afterwards", that wastes a generate round.

### A2. Attach reference files

**Do not click the `+` / paperclip button** — it opens a native file picker the agent
cannot see or control. Instead:

```
find    query: "hidden file input element for attaching files"
         → take the first ref (usually the input inside the composer form)
file_upload  paths: [<absolute paths>, ...]   ref: <that ref>
```

Multiple files in one call is fine. Keep the total under 10 MB. Screenshot afterwards to
confirm every thumbnail is present before moving on.

### A3. Pick the tool and send the prompt

1. Click the composer.
2. `type` the string `@Create image` → the dropdown shows **exactly one** result
   ("Create image — Visualize anything") → `key Return` to select it. The composer shows a
   "Create image" pill.
3. `type` the prompt body. **Type it as ONE continuous paragraph, replacing newlines with
   spaces.** A newline character inside `type` sends the message early. A single-paragraph
   prompt still produces correct results, as long as no words are lost.
4. **Verify the composer actually holds your text before sending** — read its content
   length back, do not just screenshot. A message typed right after `navigate` has been
   silently dropped (composer empty, nothing in the thread), and pressing Enter blind makes
   it look sent. Re-focus and retype if it is empty.
5. `key Return` to send, then confirm the message appears in the thread.

### A4. Wait

Normal progression: `Analyzing images` → `Generating a more detailed image — hang tight`
(with the image rendering progressively) → done, with an **Edit** button and a row of icons
beneath the image.

Poll about every 30s with `browser_batch` (3× `wait` 10s + 1 `screenshot`) — much faster
than individual calls. Measured: **~60–90 seconds**, not "a few minutes".

**NEVER resend the prompt while a generate is running.**

### A5. QC before downloading

Click the image → **fullscreen viewer**. Use `zoom` to inspect region by region; do not QC
from a shrunken screenshot.

QC against the acceptance criteria in that species' `TASK.md`. Always additionally check:
no text / frame / watermark, no stray objects.

FAIL → send a correction message **in the same chat**, naming exactly what is wrong. Three
rounds maximum, then stop and report.

### A6. Download

In the fullscreen viewer:

- The middle toolbar holds only **Markup / Comment / Remove BG / Erase / Resize** —
  **there is no download control there.**
- The download control is the **download icon in the top-right header**, next to Share
  (around `(1201, 24)` at a 1280-wide viewport).

> Older documentation described a **"Save"** button on the Remove BG / Erase bar. That has
> been wrong since 2026-09-12 — the UI changed. The chat pane has no download button
> either; do not hunt for one by hovering.

The file lands in the configured download directory, named `ChatGPT Image <date time>.png`.

```bash
find <download-dir> -maxdepth 1 -name 'ChatGPT Image*.png' -newer "$MARK" -print0 \
  | xargs -0 ls -tr        # oldest → newest = the order you clicked download
```

**Verify on disk before concluding anything about the download.** Two separate
misdiagnoses have come from checking too early or from a lost read permission: on
2026-09-11 a successful download was reported as "Chrome is blocking downloads", and on
2026-09-12 a TCC revocation produced the same symptom from a completely different cause.
If you cannot read the download directory, say so — do not infer that the download failed.

A `.com.google.Chrome.XXXXXX` temp file with no new PNG means **a native Save dialog is
open and blocking Chrome**. Preflight A0 was skipped or failed. Do not touch that temp
file behind Chrome's back — ask the user to deal with the dialog.

### A7. Receive the file

```bash
mv "<the file you just identified>" "<repo>/.ai-bridge/<species>/incoming/<canonical name>.png"

python3 -c "
from PIL import Image
im=Image.open('<destination path>'); im.load(); print(im.size, im.mode)"   # must be RGBA
```

### A8. Report

```
SAVED_TO: <absolute path>
```

Include: whether the generate succeeded, how many correction rounds and why the first
image was rejected, the chat URL, and **every place this document no longer matches the
current UI**.

---

## LANE B — you cannot generate images

This is not a failure and there is no way around it. Do the part you can do, then hand off.

**You can do:** write or edit `TASK.md`, create `incoming/`, write and refine prompts, and
**everything after the image is on disk** — dechecker, normalize, build atlas, geometry
measurement, wiring into the game, running tests, committing.

If `incoming/` already holds images from a previous round, just carry on processing them.

**You cannot do:** the in-browser stretch (A1–A7).

Report in this shape; do not just say "I can't":

```
LANE: B — no mcp__claude-in-chrome__*, cannot generate images.
DONE:     <the offline work you completed>
HANDED:   SendMessage to <session name> to run .ai-bridge/<species>/TASK.md
          (or: no session with a bridge found → the user needs to open `claude` in a
           terminal at <repo>; the bridge turns on by itself, no --chrome flag needed)
AWAITING: <the expected incoming/ path>
```

---

## Traps that have already cost time — do not hit them again

- **A raw may come back with a fake checkerboard baked in instead of real alpha — it varies
  per generate, so check, do not assume either way.** Colour types of the raws on disk
  2026-09-12: `raw_tool_hoe_idle` and both `raw_pest_caterpillar-single_*` are type 2 (no
  alpha); `raw_tool_watering-can_idle` and `raw_tool_harvest-hand_idle` are type 6 (real
  alpha). Read the type and run `tools/dechecker.py` only when it is 2.

  **What the evidence actually shows.** Two threads were enumerated in-session, reading
  byte `d[25]` (PNG colour type) of every image in each:

  - Thread A, outside the project, header badge `Work`: **7/7 model-generated images were
    type 2.** The only type-6 file in it was a reference image uploaded by the agent.
  - Thread B, inside the mayhoa project, mode radiogroup read as `Chat=true, Work=false`:
    **3/3 were type 6.**

  A 10/10 split is a strong signal, but it does **not** isolate the cause. The two threads
  differ in at least three variables at once: mode (Work vs Chat), project membership
  (outside vs inside), and date (10–11 Sep vs 11–12 Sep, so a backend change is not ruled
  out). With n = 2 threads, mode cannot be separated from project membership.

  Settling it would need one image generated in a **Work-mode thread inside the project**.
  **The user decided 2026-09-12 not to run it and to standardise on Chat mode instead** (see
  A1), which makes the question moot in practice — under Chat mode the raws come back type 6.

  **Keep reading the colour type anyway.** It costs nothing, and if a Chat-mode raw ever
  comes back type 2 that means something changed upstream — worth knowing, not worth
  silently repairing.
- **Do not conclude a transport is broken from identical file bytes.** Four files sharing
  one md5 in 2026-09-12 were read as "the download is grabbing a stale image"; in fact only
  one generate had ever run for that asset and it had simply been downloaded four times.
  Ask whether a new generate actually happened first.
- **The real grab hazard is the opposite one:** fetching the image before the new one has
  finished loading picks up the *previous* `img` in the DOM — that is how a watering-can
  file once came back from a bug-net generate. Compare bytes or asset id against the
  previous image and only trust a result once it differs. File names carry a fresh
  timestamp even when the contents are stale.
- **Changing the plate shape means re-measuring the code**, not just dropping in a file:
  `SOIL_PLATE_MASTER_W` in `mayhoa-farm-demo/src/core/config.ts` is `349`, measured from
  the old oval plate. Especially relevant for `soil_square`.

## Infrastructure gotchas

- **The bridge dies after a Claude Code CLI update.** `~/.claude/chrome/chrome-native-host`
  hardcodes a version-pinned path
  (`/opt/homebrew/Caskroom/claude-code@latest/<ver>/claude`), so an update leaves it
  pointing at nothing. Run `claude --chrome` again to have it rewrite the wrapper, then hit
  Reconnect in the extension. Do not hand-edit the wrapper and do not trust the `/chrome`
  panel — only `pgrep -fl chrome-native-host` proves a live host.
- **A mid-session update does not kill a live bridge, but it arms the trap.** The wrapper
  regenerates to the new version while the running host is still the old binary; the live
  session keeps working because it matches the *running* host, and the skew only bites on
  the next `--chrome` launch. Compare `pgrep -fl chrome-native-host` against the wrapper's
  exec line to spot it. Mid-queue when the CLI updates? Finish the queue first.
- This flow only works with Chrome and the repo on the **same machine**.
- Requires a paid plan and the `debugger` permission for the extension. Other
  Chromium builds and mobile are not supported.

## Removed — do not rebuild

- **Google Drive + `gws`** — dropped 2026-09-05. The Drive bridge was only needed when the
  executor could not receive binaries directly; driving the browser yourself makes it a
  button click. Dropping it removed a connector call, several Allow prompts, and the risk
  of OAuth expiry (the `gws` token was revoked at exactly the wrong moment).
- **CodexPro2 and every Codex-backed executor** — no remaining role in this flow.
