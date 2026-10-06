#!/bin/sh
# usage: gen.sh <name> <prompt-file>; refs are a tool + decor master for style
set -u
name="$1"; pf="$2"
A=/Users/kelvin/Projects/yudgnahk/mayhoa-asset/masters
REF1=$A/farm/tools/tool_watering-can_idle_v01.png
REF2=$A/village/decor/decor_bench_v01.png
{ printf '%s\n\n' "Use your built-in image generation tool to create exactly ONE image, then save the PNG as /tmp/mayhoa-ui/out/$name.png (copy it from wherever the tool writes it). The attached images are STYLE references only. Do not write any code to draw the image. Image prompt follows."; cat "$pf"; } | \
  codex1 exec --skip-git-repo-check -s workspace-write -C /tmp/mayhoa-ui -i "$REF1" -i "$REF2" > /tmp/mayhoa-ui/log-$name.txt 2>&1
ls -la /tmp/mayhoa-ui/out/$name.png 2>&1
