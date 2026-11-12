#!/usr/bin/env bash
# usage: build/render.sh deck.pptx outdir   -> outdir/slide-XX.jpg
set -e
S=$(dirname "$(find /mnt/skills /root/.claude/skills -path "*pptx/scripts/office/soffice.py" 2>/dev/null | head -1)")/../..
deck=$(readlink -f "$1"); out=$(readlink -f -m "$2"); mkdir -p "$out"; rm -f "$out"/slide-*.jpg "$out"/*.pdf
cp "$deck" "$out/deck.pptx"
( cd "$out" && timeout 300 python "$S/scripts/office/soffice.py" --headless --convert-to pdf deck.pptx >/dev/null 2>&1 )
pdftoppm -jpeg -r 80 "$out/deck.pdf" "$out/slide"
rm -f "$out/deck.pptx"
ls -1 "$out"/slide-*.jpg
