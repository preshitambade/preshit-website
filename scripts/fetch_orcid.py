"""
fetch_orcid.py
---------------
Weekly job: pull the peer-reviewed publications list from ORCID's
free public API and write it to data/publications.json in the shape
metrics.js expects.

ORCID is the gold standard for this — official, free, no auth required
for public data, and stable.

Env vars:  ORCID_ID  (e.g. "0000-0002-1234-5678")
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "publications.json"
API  = "https://pub.orcid.org/v3.0/{orcid}/works"

def fetch_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "preshit-site/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

def main():
    orcid = os.environ.get("ORCID_ID", "").strip()
    if not orcid:
        print("ORCID_ID env var is not set — nothing to do.", file=sys.stderr)
        sys.exit(0)

    print(f"Fetching ORCID works for {orcid} …")
    try:
        summary = fetch_json(API.format(orcid=orcid))
    except Exception as e:
        print(f"ORCID fetch failed: {e}. Keeping previous list.", file=sys.stderr)
        sys.exit(0)

    put_codes = [w["work-summary"][0]["put-code"] for w in summary.get("group", [])]
    pubs = []
    for code in put_codes:
        try:
            work = fetch_json(f"https://pub.orcid.org/v3.0/{orcid}/work/{code}")
        except Exception as e:
            print(f"  skip {code}: {e}", file=sys.stderr)
            continue

        title = ((work.get("title") or {}).get("title") or {}).get("value", "")
        year_raw = ((work.get("publication-date") or {}).get("year") or {})
        year = int(year_raw.get("value")) if year_raw and year_raw.get("value") else None

        venue = ((work.get("journal-title") or {}) or {}).get("value", "")

        authors = ""
        contribs = (work.get("contributors") or {}).get("contributor") or []
        names = []
        for c in contribs:
            nm = ((c.get("credit-name") or {}) or {}).get("value")
            if nm:
                names.append(nm)
        if names:
            authors = ", ".join(names)

        doi, url = "", ""
        for ext in ((work.get("external-ids") or {}).get("external-id") or []):
            t = (ext.get("external-id-type") or "").lower()
            v = (ext.get("external-id-value") or "").strip()
            if t == "doi" and not doi:
                doi = v
            url_obj = ext.get("external-id-url") or {}
            if not url and url_obj.get("value"):
                url = url_obj["value"]

        pubs.append({
            "authors": authors,
            "year": year,
            "title": title,
            "venue": venue,
            "doi": doi,
            "url": url,
        })

    # sort newest first
    pubs.sort(key=lambda p: (p["year"] or 0), reverse=True)

    payload = {
        "updated": datetime.now(timezone.utc).date().isoformat(),
        "source": f"ORCID {orcid}",
        "publications": pubs,
    }
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {DATA}: {len(pubs)} publications")

if __name__ == "__main__":
    main()
