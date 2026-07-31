# Automated updates — setup guide

Your site pulls two things automatically, so you rarely have to touch it after the initial setup:

| What | Where it appears | How it's fetched | How often |
|---|---|---|---|
| **Publications list** | `research.html` | ORCID public API (official, free, rock-solid) | Weekly |
| **Scholar metrics** (citations, h-index, i10-index, pub count) | Home page stats strip | `scholarly` Python library scrapes Google Scholar | Weekly |

Both jobs run inside a single GitHub Actions workflow (`.github/workflows/update-data.yml`), which writes fresh JSON into `data/` and commits it back to your repo. The site loads those JSON files on page load — nothing else changes.

---

## One-time setup (5 minutes)

### 1. Get your IDs

- **ORCID iD** — sign up at [orcid.org](https://orcid.org) if you don't have one. Format is `0000-0002-1234-5678`. Make sure your public works list on ORCID is what you want the site to show (add/remove entries there; the site follows).
- **Google Scholar user ID** — open your Scholar profile and copy the value after `user=` in the URL. For example, `https://scholar.google.com/citations?user=abc123XyZ` → your ID is `abc123XyZ`.

### 2. Add them as GitHub secrets

In your GitHub repo:

1. Go to **Settings → Secrets and variables → Actions → New repository secret**
2. Add two secrets:
   - `ORCID_ID` = your ORCID iD (e.g. `0000-0002-1234-5678`)
   - `SCHOLAR_USER` = your Scholar user ID (e.g. `abc123XyZ`)

That's it. The workflow will pick them up automatically.

### 3. Run it once manually

- Go to **Actions → Update publications & Scholar metrics → Run workflow**
- Wait ~2 minutes
- You should see a new commit from `github-actions[bot]` updating `data/metrics.json` and `data/publications.json`
- Reload your site — the numbers and publications should now be live

From then on, the workflow runs every Monday at 06:00 UTC automatically.

---

## What if Google Scholar blocks the scrape?

This happens sometimes — Scholar throws CAPTCHAs at bots. The script handles this gracefully:

- If Scholar blocks the fetch, `fetch_scholar.py` exits without overwriting the existing values
- Your site keeps showing the **last known metrics** — no broken numbers, no errors
- Next week's run will try again
- ORCID publications keep working regardless — they use a different, official API

If Scholar keeps failing, options are:
- **Just leave it** — an outdated Scholar count is not the end of the world
- **Manually update** `data/metrics.json` when you notice
- **Upgrade to SerpAPI** (~$50/mo) — it has an official Scholar endpoint that never breaks. If you go this route, ask for the swap.

---

## Adding new writing / articles

The op-eds on `writing.html` are still edited by hand — there's no reliable public API for personal blog posts. When you publish something new:

1. Open `writing.html`
2. Copy any existing `<a class="article-item">...</a>` block
3. Change the date, title, and `href` — done

If you want this automated too (say, from a Medium RSS feed or a WordPress site), tell me the source and I'll wire it up.

---

## Local testing

If you want to test the fetch scripts before letting GitHub run them:

```bash
pip install scholarly
export ORCID_ID="0000-0002-1234-5678"
export SCHOLAR_USER="your_scholar_id"
python scripts/fetch_orcid.py
python scripts/fetch_scholar.py
```

Then open `index.html` and `research.html` and confirm the numbers and pubs show up.

<!-- git push pipeline verified: 2026-07-31 -->
