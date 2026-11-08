"""
fetch_openalex.py
-----------------
Weekly job: fetch citation count, h-index, and i10-index from OpenAlex and write
them to data/metrics.json.

OpenAlex (https://openalex.org) is a free, open, stable scholarly index — the
modern replacement for brittle Google Scholar scraping. No API key, no
JavaScript rendering, no CAPTCHA risk. Just a plain REST call that returns
every stat we need for the home-page metrics strip.

Requires:  stdlib only (no external packages needed)
Env vars:  ORCID_ID        (e.g. "0000-0002-6919-7206")
           OPENALEX_EMAIL  (optional — polite-pool contact email per OpenAlex guidance)
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "metrics.json"
API  = "https://api.openalex.org/authors/orcid:{orcid}"


def fetch_json(url, email):
    ua = f"preshit-site/1.0 (mailto:{email})" if email else "preshit-site/1.0"
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": ua,
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    orcid = os.environ.get("ORCID_ID", "").strip()
    if not orcid:
        print("ORCID_ID env var is not set — nothing to do.", file=sys.stderr)
        sys.exit(0)

    email = os.environ.get("OPENALEX_EMAIL", "").strip()

    print(f"Fetching OpenAlex author profile for ORCID {orcid} …")
    try:
        author = fetch_json(API.format(orcid=orcid), email)
    except Exception as e:
        print(f"OpenAlex fetch failed: {e}. Keeping previous metrics.", file=sys.stderr)
        sys.exit(0)

    stats = author.get("summary_stats") or {}

    citations = int(author.get("cited_by_count") or 0)
    h_index   = int(stats.get("h_index") or 0)
    i10_index = int(stats.get("i10_index") or 0)

    current = {}
    if DATA.exists():
        try:
            current = json.loads(DATA.read_text())
        except json.JSONDecodeError:
            current = {}

    new = dict(current)
    new.update({
        "citations":    citations,
        "h_index":      h_index,
        "i10_index":    i10_index,
        "publications": 0,
        "scholar_url":  current.get(
            "scholar_url",
            "https://scholar.google.com/citations?user=KSbxiGAAAAAJ",
        ),
        "updated":      datetime.now(timezone.utc).date().isoformat(),
        "source":       "OpenAlex",
    })
    new.pop("_note", None)

    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(new, indent=2))
    print(f"Wrote {DATA}: citations={citations}, h={h_index}, i10={i10_index}")


if __name__ == "__main__":
    main()
