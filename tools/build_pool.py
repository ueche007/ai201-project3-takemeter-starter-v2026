"""Turn the raw r/running Atom feeds into one clean candidate pool.

    python tools/build_pool.py data/raw_rss data/candidate_posts.csv

Each row is one post or comment: id, kind, permalink, published, text.
Usernames are dropped (including the "submitted by /u/x" line on link posts).
Bot posts and removal notices, deleted/removed text and duplicates are skipped. The text is kept whole; it is not trimmed to fit the model.

This is the pool posts are picked from. It is NOT labels.csv.
"""
import csv
import html
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {"a": "http://www.w3.org/2005/Atom"}
SKIP_AUTHORS = {"/u/AutoModerator", "/u/running-ModTeam"}
MIN_CHARS = 40


def html_to_text(raw):
    s = raw or ""
    s = s.split("<!-- SC_ON -->")[0]          # drop "submitted by /u/... [link] [comments]"
    s = s.replace("<!-- SC_OFF -->", "")
    # Keep quoted text (replies often only make sense with it), marked Reddit-style.
    s = re.sub(r"<blockquote>(.*?)</blockquote>",
               lambda m: re.sub(r"<p>", "<p>&gt; ", m.group(1)), s, flags=re.S)
    s = re.sub(r"<(br|/p|/li|/h\d)\s*/?>", "\n", s)
    s = re.sub(r"<li>", "- ", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    s = "\n".join(line.strip() for line in s.split("\n"))
    s = re.sub(r"\n\s*\n+", "\n", s)
    # Link posts have no SC_ON marker, so strip their "submitted by /u/x [link] [comments]".
    s = re.sub(r"\s*submitted by\s+/u/\S+.*$", "", s, flags=re.S)
    s = re.sub(r"\bu/[A-Za-z0-9_-]+", "u/[user]", s)   # mentions of other users
    return s.strip()


MOD_THREADS = ("super moronic monday", "miscellaneous monday chit chat")


def is_bot(text):
    t = text.lower()
    return ("this is a bot message" in t or "automatically removed by" in t
            or t.startswith(MOD_THREADS))     # scheduled mod threads, boilerplate body


def rows_from(path):
    root = ET.parse(path).getroot()
    for e in root.findall("a:entry", NS):
        eid = (e.findtext("a:id", "", NS) or "").strip()
        author = (e.findtext("a:author/a:name", "", NS) or "").strip()
        link = e.find("a:link", NS)
        permalink = link.get("href") if link is not None else ""
        published = e.findtext("a:published", "", NS) or e.findtext("a:updated", "", NS)
        body = html_to_text(e.findtext("a:content", "", NS))
        title = html.unescape(e.findtext("a:title", "", NS) or "").strip()
        kind = "post" if eid.startswith("t3_") else "comment"
        if author in SKIP_AUTHORS:
            continue
        if body.lower() in {"[deleted]", "[removed]"}:
            continue
        if kind == "post":
            text = f"{title}\n{body}".strip() if body else title
        else:
            text = body
        if len(text) < MIN_CHARS or is_bot(text):
            continue
        yield {"id": eid, "kind": kind, "permalink": permalink,
               "published": (published or "")[:10], "text": text}


def main():
    src, dest = Path(sys.argv[1]), Path(sys.argv[2])
    seen_id, seen_text, out = set(), set(), []
    for f in sorted(src.glob("*.xml")):
        for r in rows_from(f):
            key = re.sub(r"\W+", " ", r["text"].lower()).strip()
            if r["id"] in seen_id or key in seen_text:
                continue
            seen_id.add(r["id"])
            seen_text.add(key)
            out.append(r)
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "kind", "permalink", "published", "text"])
        w.writeheader()
        w.writerows(out)
    posts = sum(r["kind"] == "post" for r in out)
    print(f"{len(out)} rows ({posts} posts, {len(out) - posts} comments) -> {dest}")


if __name__ == "__main__":
    main()
