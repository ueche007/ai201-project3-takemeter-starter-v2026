"""Download public r/running Atom feeds, slowly, into a raw folder.

Reddit's JSON API needs a login; the public .rss feeds do not, but they
rate-limit hard (HTTP 429 after one or two quick requests). So this waits
between requests and backs off on 429. Raw feeds are kept as provenance.

Usage:
    python tools/fetch_rss.py OUT_DIR PATH [PATH ...]
    e.g. python tools/fetch_rss.py data/raw_rss "top/.rss?t=year&limit=100"
A PATH is relative to https://www.reddit.com/r/running/.
Already-downloaded files are skipped, so it can be re-run safely.
"""
import hashlib
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://www.reddit.com/r/running/"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
DELAY = 12        # seconds between requests
MAX_TRIES = 6


def fname(path):
    safe = "".join(c if c.isalnum() else "_" for c in path)[:80]
    return f"{safe}_{hashlib.md5(path.encode()).hexdigest()[:6]}.xml"


def fetch(url):
    wait = 60
    for attempt in range(1, MAX_TRIES + 1):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < MAX_TRIES:
                print(f"  429, waiting {wait}s (try {attempt})", flush=True)
                time.sleep(wait)
                wait = min(wait * 2, 600)
                continue
            raise
        except urllib.error.URLError:
            if attempt < MAX_TRIES:
                time.sleep(wait)
                continue
            raise


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for path in sys.argv[2:]:
        dest = out / fname(path)
        if dest.exists():
            print(f"skip {path}")
            continue
        try:
            body = fetch(BASE + path)
        except Exception as e:
            print(f"FAIL {path}: {e}", flush=True)
            continue
        dest.write_bytes(body)
        print(f"ok   {path} -> {dest.name} ({body.count(b'<entry>')} entries)", flush=True)
        time.sleep(DELAY)


if __name__ == "__main__":
    main()
