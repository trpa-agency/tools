"""Inventory or mirror every document the site links to.

Reads data/documents.json and data/handbook.json, collects each relative href (the ones
that resolve against docBase), and either reports their sizes (--report, the default) or
downloads them into documents/ with the same relative paths (--download). After a
download, set "docBase": "documents/" in data/documents.json and the site serves the
files itself.

  python scripts/fetch_documents.py            # HEAD every file, print a size table
  python scripts/fetch_documents.py --download # mirror into documents/

Standard library only, so the base Python works. Items that already exist locally are
skipped unless --force is given.
"""

import argparse
import json
import logging
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_JSON = ROOT / "data" / "documents.json"
HANDBOOK_JSON = ROOT / "data" / "handbook.json"
OUT_DIR = ROOT / "documents"
USER_AGENT = "Mozilla/5.0 (TRPA bmp.trpa.gov document migration)"

log = logging.getLogger("fetch_documents")


def is_relative(href: str) -> bool:
    return bool(href) and not href.startswith(("http://", "https://", "#", "mailto:"))


def collect() -> tuple[str, list[str]]:
    docs = json.loads(DOCS_JSON.read_text(encoding="utf-8"))
    hb = json.loads(HANDBOOK_JSON.read_text(encoding="utf-8"))
    paths: list[str] = []

    def add(h):
        if is_relative(h):
            paths.append(urllib.parse.unquote(h))

    for sec in docs["sections"]:
        for it in sec["items"]:
            add(it.get("href"))
            add(it.get("es"))
    add(hb["complete"]["href"])
    for ch in hb["chapters"]:
        add(ch.get("href"))
        for s in ch.get("supplements", []):
            add(s.get("href"))
    for sec in hb["toolkit"]:
        add(sec.get("intro"))
        for f in sec["factSheets"]:
            add(f.get("href"))
        for d in sec["drawings"]:
            add(d.get("pdf"))
            add(d.get("dwg"))

    # de-duplicate, keep order
    seen, unique = set(), []
    for p in paths:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return docs["docBase"], unique


def url_for(base: str, rel: str) -> str:
    return base.rstrip("/") + "/" + urllib.parse.quote(rel, safe="/")


def head(url: str) -> int | None:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return int(resp.headers.get("Content-Length") or 0)
    except urllib.error.HTTPError as exc:
        log.warning("%s -> HTTP %s", url, exc.code)
    except Exception as exc:  # noqa: BLE001
        log.warning("%s -> %s", url, exc)
    return None


def download(url: str, dest: Path) -> int:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(req, timeout=120) as resp, dest.open("wb") as fh:
        total = 0
        while chunk := resp.read(1 << 16):
            fh.write(chunk)
            total += len(chunk)
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--download", action="store_true", help="mirror files into documents/")
    parser.add_argument("--force", action="store_true", help="re-download files that already exist")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    base, paths = collect()
    log.info("%s documents registered, base %s", len(paths), base)
    total = 0
    missing = 0
    for rel in paths:
        url = url_for(base, rel)
        if args.download:
            dest = OUT_DIR / rel
            if dest.exists() and not args.force:
                total += dest.stat().st_size
                continue
            try:
                size = download(url, dest)
                total += size
                log.info("%8.1f MB  %s", size / 1e6, rel)
            except Exception as exc:  # noqa: BLE001
                missing += 1
                log.error("failed %s: %s", rel, exc)
        else:
            size = head(url)
            if size is None:
                missing += 1
                continue
            total += size
            print(f"{size / 1e6:8.1f} MB  {rel}")
    print(f"\nTotal {total / 1e6:.1f} MB across {len(paths) - missing} files; {missing} missing or unreachable")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
