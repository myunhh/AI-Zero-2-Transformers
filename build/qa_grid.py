"""usage: python qa_grid.py deck.pptx outdir  -> renders and writes outdir/grid-N.jpg (6 per grid)"""
import glob, os, subprocess, sys
from PIL import Image, ImageDraw
deck, out = sys.argv[1], sys.argv[2]
subprocess.run([os.path.join(os.path.dirname(os.path.abspath(__file__)), "render.sh"), deck, out], check=True, stdout=subprocess.DEVNULL)
fs = sorted(glob.glob(os.path.join(out, "slide-*.jpg")))
for f in glob.glob(os.path.join(out, "grid-*.jpg")): os.remove(f)
for k in range(0, len(fs), 6):
    g = Image.new("RGB", (1600, 1350), "white"); dr = ImageDraw.Draw(g)
    for i, f in enumerate(fs[k:k + 6]):
        im = Image.open(f).resize((800, 450)); x, y = (i % 2) * 800, (i // 2) * 450
        g.paste(im, (x, y)); dr.rectangle([x, y, x + 799, y + 449], outline="#999999")
        dr.text((x + 760, y + 5), str(k + i + 1), fill="red")
    g.save(os.path.join(out, f"grid-{k // 6 + 1}.jpg"))
print(len(fs), "slides;", (len(fs) + 5) // 6, "grids in", out)
