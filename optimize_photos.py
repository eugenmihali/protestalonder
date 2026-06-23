"""Resize + compress gallery photos for the web.
Reads originals from gallery/, writes web-ready JPEGs to assets/photos/,
and emits assets/photos/manifest.json listing them. Re-run after adding photos."""
import os, json, re
from PIL import Image, ImageOps

SRC = "gallery"
OUT = os.path.join("assets", "photos")
MAX_EDGE = 1600          # longest side in px
QUALITY = 82             # JPEG quality
EXTS = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif")

os.makedirs(OUT, exist_ok=True)

def safe_name(name):
    base = os.path.splitext(name)[0]
    base = re.sub(r"[^A-Za-z0-9._-]+", "-", base).strip("-")
    return base + ".jpg"

files = sorted(f for f in os.listdir(SRC) if f.lower().endswith(EXTS))
manifest = []
for f in files:
    src = os.path.join(SRC, f)
    out_name = safe_name(f)
    out = os.path.join(OUT, out_name)
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)          # honor phone rotation
    im = im.convert("RGB")
    im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
    im.save(out, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    kb = os.path.getsize(out) // 1024
    manifest.append(out_name)
    print(f"  {f}  ->  {out_name}  ({kb} KB)")

with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as fh:
    json.dump(manifest, fh, indent=2)

print(f"\nDone: {len(manifest)} photos -> {OUT}")
