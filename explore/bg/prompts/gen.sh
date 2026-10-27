#!/bin/sh
# usage: gen.sh <name> <prompt-file> [refs...]
set -u
name="$1"; pf="$2"; shift 2
refargs=""
for r in "$@"; do refargs="$refargs -i $r"; done
stamp=/tmp/mayhoa-bg/.stamp-$name; touch "$stamp"
P="Use your built-in image generation tool to create exactly ONE image, then save the PNG as /tmp/mayhoa-bg/out/$name.png (the tool writes it under /Users/kelvin/.codex1/generated_images/<thread_id>/; copy the newest png from there, do not search the whole disk). Any attached images are STYLE references only. Do not write any code to draw the image. Image prompt follows. $(cat "$pf")"
# shellcheck disable=SC2086
~/.local/bin/codex1 exec --json --skip-git-repo-check --ephemeral -s workspace-write -C /tmp/mayhoa-bg --add-dir /tmp/mayhoa-bg/out --add-dir /Users/kelvin/.codex1/generated_images $refargs -- "$P" </dev/null > /tmp/mayhoa-bg/log-$name.jsonl 2>&1
if [ ! -f /tmp/mayhoa-bg/out/$name.png ]; then
  f=$(find /Users/kelvin/.codex1/generated_images -name '*.png' -newer "$stamp" | head -1)
  [ -n "$f" ] && cp "$f" /tmp/mayhoa-bg/out/$name.png
fi
ls -la /tmp/mayhoa-bg/out/$name.png 2>&1
