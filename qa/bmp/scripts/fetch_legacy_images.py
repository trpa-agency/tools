"""Pull gallery and page images from the legacy tahoebmp.org site and write web-sized copies.

Reads data/gallery.json (the single list of images the site uses), downloads each
source image, and saves:

  assets/gallery/<file>         gallery image, longest side GALLERY_MAX px
  assets/gallery/thumbs/<file>  gallery thumbnail, longest side THUMB_MAX px
  assets/img/<file>             page images (hero, banners, obliques), longest side SITE_MAX px

Existing outputs are skipped unless --force is passed. Run from the repo root with the
arcgispro-py3 interpreter (it has Pillow):

  "C:\\Program Files\\ArcGIS\\Pro\\bin\\Python\\envs\\arcgispro-py3\\python.exe" scripts/fetch_legacy_images.py
"""

import argparse
import io
import json
import logging
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "gallery.json"
GALLERY_DIR = ROOT / "assets" / "gallery"
THUMB_DIR = GALLERY_DIR / "thumbs"
IMG_DIR = ROOT / "assets" / "img"

GALLERY_MAX = 1280   # lightbox size; 77 images at this size stay under ~15 MB total
THUMB_MAX = 560
SITE_MAX = 1800
JPEG_QUALITY = 78
USER_AGENT = "Mozilla/5.0 (TRPA bmp.trpa.gov image migration)"

log = logging.getLogger("fetch_legacy_images")


def fetch(url: str) -> bytes:
    # The legacy site serves static files directly; only .aspx pages need the cookie dance.
    safe_url = urllib.parse.quote(url, safe=":/?&=%")
    req = urllib.request.Request(safe_url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def save_resized(data: bytes, out_path: Path, max_side: int) -> tuple[int, int]:
    im = Image.open(io.BytesIO(data))
    im = ImageOps.exif_transpose(im)
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    im.save(out_path, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    return im.size


def process(items, base, outputs, force):
    """outputs: list of (dir, max_side). Returns (done, skipped, failed)."""
    done = skipped = failed = 0
    for item in items:
        targets = [(d / item["file"], m) for d, m in outputs]
        if not force and all(t.exists() for t, _ in targets):
            skipped += 1
            continue
        url = base + item["src"].replace("\\", "/")
        try:
            data = fetch(url)
        except Exception as exc:  # noqa: BLE001 - report and keep going
            log.error("download failed %s: %s", url, exc)
            failed += 1
            continue
        for target, max_side in targets:
            try:
                size = save_resized(data, target, max_side)
                log.info("wrote %s %sx%s", target.relative_to(ROOT), *size)
            except Exception as exc:  # noqa: BLE001
                log.error("resize failed %s: %s", target, exc)
                failed += 1
        done += 1
    return done, skipped, failed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--force", action="store_true", help="re-download and overwrite existing outputs")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    base = manifest["legacyBase"]

    g = process(manifest["images"], base, [(GALLERY_DIR, GALLERY_MAX), (THUMB_DIR, THUMB_MAX)], args.force)
    s = process(manifest.get("siteImages", []), base, [(IMG_DIR, SITE_MAX)], args.force)
    log.info("gallery: %s written, %s skipped, %s failed", *g)
    log.info("site images: %s written, %s skipped, %s failed", *s)
    return 1 if (g[2] or s[2]) else 0


if __name__ == "__main__":
    sys.exit(main())
