"""
fetch_scholar.py
-----------------
Weekly job: fetch citation count, h-index, i10-index from Google Scholar
and write them to data/metrics.json.

Google Scholar has NO official API. We use the `scholarly` library, which
scrapes the site. Scholar occasionally blocks scrapers with a CAPTCHA —
when that happens, this script exits without overwriting the existing
values, so the site keeps showing the last known numbers.

Requires:  pip install scholarly
Env vars:  SCHOLAR_USER  (e.g. "abc123XyZ" — the ID from your Scholar URL)
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "metrics.json"

def main():
    user_id = os.environ.get("SCHOLAR_USER", "").strip()
    if not user_id:
        print("SCHOLAR_USER env var is not set — nothing to do.", file=sys.stderr)
        sys.exit(0)  # exit clean so the workflow doesn't fail on missing secret

    try:
        from scholarly import scholarly
    except ImportError:
        print("scholarly not installed. Run: pip install scholarly", file=sys.stderr)
        sys.exit(1)

    print(f"Fetching Scholar profile for user_id={user_id} …")
    try:
        author = scholarly.search_author_id(user_id)
        author = scholarly.fill(author, sections=["basics", "indices", "counts"])
    except Exception as e:
        # Most common: Scholar returned a CAPTCHA or a 429.
        print(f"Scholar fetch failed: {e}. Keeping previous metrics.", file=sys.stderr)
        sys.exit(0)

    # merge with whatever's currently on disk so we don't clobber the scholar_url
    current = {}
    if DATA.exists():
        current = json.loads(DATA.read_text())

    new = dict(current)
    new.update({
        "citations":    author.get("citedby", current.get("citations", 0)),
        "h_index":      author.get("hindex",  current.get("h_index", 0)),
        "i10_index":    author.get("i10index", current.get("i10_index", 0)),
        "publications": len(author.get("publications", []) or []) or current.get("publications", 0),
        "scholar_url":  f"https://scholar.google.com/citations?user={user_id}",
        "updated":      datetime.now(timezone.utc).date().isoformat(),
    })
    new.pop("_note", None)

    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(new, indent=2))
    print(f"Wrote {DATA}: citations={new['citations']}, h={new['h_index']}, i10={new['i10_index']}")

if __name__ == "__main__":
    main()
