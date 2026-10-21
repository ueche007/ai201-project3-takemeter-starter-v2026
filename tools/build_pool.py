"""Turn the raw r/running Atom feeds into one clean candidate pool.

    python tools/build_pool.py data/raw_rss data/candidate_posts.csv

Each row is one post or comment: id, kind, permalink, published, text.
Usernames are dropped. Bot posts, deleted/removed text and duplicates are
skipped. The text is kept whole; it is not trimmed to fit the model.

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
    return s.strip()


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
        if len(text) < MIN_CHARS:
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
