# Assets folder

Drop images and any downloadable files the site references here. The site expects the following exact filenames — if the file exists at this path, the page renders it automatically.

## Currently referenced

| File | Used by | Notes |
|---|---|---|
| `preshit-ambade.jpg` | Home hero photo (`index.html`) | Your headshot. Any modern format works — just rename it to `.jpg`. Aim for ~800×1000 px, portrait orientation. |
| `surgeon-general-framework.png` | Augusta+ Scale page (`augusta-scale.html`) | Download the official framework diagram from [hhs.gov/surgeongeneral/priorities/workplace-well-being](https://www.hhs.gov/surgeongeneral/priorities/workplace-well-being/index.html) → right-click the wheel image → Save Image As. |

## Not yet used, but planned

| File | Would be used by | Notes |
|---|---|---|
| `sample-syllabus.pdf` | Teaching page | Sample course syllabus |
| `observation-colleague.pdf` | Teaching page | Letter of observation by a colleague |
| `sample-presentation.pdf` | Teaching page | Sample lecture slides |
| `sample-assignment.pdf` | Teaching page | Sample student assignment |
| `observation-mentor.pdf` | Teaching page | Letter of observation by a mentor |

If you don't upload one of these, the "View document →" card on the Teaching page will just 404 when clicked — nothing else breaks. Remove the card from `teaching.html` if you don't plan to publish that document.

## Naming rules

- Use lowercase, hyphenated names (`my-photo.jpg`, not `My Photo.JPG` or `my_photo.jpg`) — case matters on GitHub Pages
- No spaces
- Keep original file extensions (`.jpg`, `.png`, `.pdf`)

## Uploading to GitHub

Same as any other file: **Add file → Upload files** → drag them into `assets/` on the GitHub website. Site updates in ~1 minute.
