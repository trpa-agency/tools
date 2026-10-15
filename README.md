# TRPA Tools

Official maps, apps, and tools of TRPA, to be served at **tools.trpa.gov** via GitHub Pages (today at trpa-agency.github.io/tools). This site replaces the gallery at gis.trpa.org as apps are migrated and new apps are built. It carries forward the history of `trpa-agency/maps` (apps.trpa.gov), which it replaces.

## Structure

```
tools/
├── index.html          # Production gallery: apps without "beta": true
├── apps.json           # Single source of truth for the app registry (production and QA)
├── 404.html            # Branded not-found page
├── assets/
│   ├── site.css        # Shared styles (TRPA brand)
│   ├── gallery.js      # Shared gallery renderer (production or QA mode)
│   ├── trpa-tokens.css # Shared design tokens (see qa/data/design-system.html)
│   ├── fonts/          # Self-hosted Open Sans and Lexend Deca
│   └── thumbs/         # App thumbnails
├── planning/           # Planning apps (zoning, housing, shoreline)
├── transportation/     # Transportation apps (transit, active transportation, Transportation Tracker)
├── permitting/         # Permitting apps (parcels, permits)
├── eip/                # Environmental Improvement Program apps (stormwater, forest health, SEZ)
├── general/            # General viewers
├── monitoring/         # Threshold, climate, lake clarity, wildfire, and smoke dashboards
├── data/               # Open data and developer resources
├── qa/                 # Apps in development and review, same category structure as the root
│   ├── index.html      # QA gallery: apps with "beta": true
│   ├── planning/ ... data/   # QA category pages and the beta apps hosted in this repo
│   ├── storymaps/      # Story Map Gallery, live from ArcGIS Online
│   └── surveys/        # Survey Gallery, live from ArcGIS Online; surveys.json groups, describes, and hides forms
└── docs/               # Planning documents
```

Each category folder has an `index.html` landing page that lists only its apps. Apps built here live inside their category, as a single file (`qa/permitting/public-notice.html`) or a subfolder for multi-file apps (`planning/localplans/` to `tools.trpa.gov/planning/localplans/`). There is no top-level `tools/` folder; on tools.trpa.gov that path would read twice.

## Production and QA

The site has two galleries built from the same `apps.json`:

| | Production | QA |
|---|---|---|
| URL | tools.trpa.gov | tools.trpa.gov/qa/ |
| Lists | apps without `"beta": true` | apps with `"beta": true` |
| App files | `<category>/` | `qa/<category>/` |
| Pages | indexed | `noindex`, orange "In development" banner |

The root holds production apps only. Everything still in development or review lives under `qa/`, which repeats the root's category structure (`qa/planning/`, `qa/eip/`, and so on). The production home links to QA from its footer ("Apps in development"), and every QA page links back to production. Apps hosted elsewhere (github.io pages, vendor sites) have no files here; their `beta` flag alone decides which gallery lists them.

`gallery.js` handles both: each page sets `window.GALLERY_CONFIG = { base, category, qa }`. `base` always points at the repo root (where `apps.json` and `assets/` live), so QA category pages use `base: '../..'` and `qa: true`.

### Review process

1. **Build in QA.** Put a new app in `qa/<category>/` and add it to `apps.json` with `"beta": true` and a `url` starting `qa/`. Shared files are two levels up: `../../assets/`.
2. **Review.** Share the `/qa/` link with reviewers. Run the `trpa-dashboard-qa` checklist against it. Collect fixes in issues or PR comments.
3. **Promote.** When the app is approved, in one PR:
   - `git mv qa/<category>/<app> <category>/<app>` (keeps history).
   - Change `../../assets/` to `../assets/` in the moved files, and fix any links to other QA apps.
   - In `apps.json`, drop the `qa/` prefix from `url` and remove `"beta": true`.
   - If the app writes data from a script or workflow, update its output path.
4. **Verify.** Serve locally, confirm the app shows on the production gallery and is gone from QA, then merge.

To pull an app back for rework, run the same steps in reverse.

## Adding or updating an app

Edit `apps.json`, every page reads from it, so no HTML changes are needed:

```json
{
  "id": "myapp",
  "title": "My App",
  "category": "planning",
  "url": "planning/myapp/",
  "thumbnail": "assets/thumbs/myapp.png",
  "description": "One or two sentences. TRPA style: spell out acronyms on first use.",
  "tags": ["Zoning"],
  "external": false
}
```

- `category` must match a `slug` in the `categories` array (`planning`, `transportation`, `permitting`, `eip`, `general`, `monitoring`, `data`).
- `url` can be relative (apps hosted in this repo) or absolute (apps still on gis.trpa.org or external sites like Lake Tahoe Info).
- Set `"external": true` for non-TRPA-hosted sites. Thumbnails are 200 x 133 PNGs in `assets/thumbs/`.

## Migrating an app from gis.trpa.org

1. Copy the app's files into a subfolder of the right category, e.g. `eip/bmpmappingtool/`.
2. Update its entry in `apps.json` to the new relative URL.
3. Set up a redirect from the old gis.trpa.org URL once DNS and traffic cut over.

## Data inventory refresh

The Tahoe Data Inventory ([qa/data/data-inventory.html](qa/data/data-inventory.html)) reads its rows
from `qa/data/data-inventory.json`, which is rebuilt by `scripts/build_inventory.py` (stdlib-only
Python). The script crawls the Tahoe Open Data DCAT feed, the maps.trpa.org REST directory, and
eight partner agency directories; the LT Info rows come from the static seed
`scripts/inventory_seed.json` (no crawlable directory exists, edit that file to change them).

A GitHub Action (`.github/workflows/refresh-inventory.yml`) reruns the script on the first of
each month and opens a PR when the data changed, review the diff and merge to publish. Run it
on demand from the Actions tab ("Refresh data inventory" → Run workflow), or locally with
`python scripts/build_inventory.py`. Failsafe: if an agency's crawl fails or shrinks by more
than 30 percent, its previous rows are kept and the PR body flags it.

## Local preview

Serve the repo root (fetch of `apps.json` requires http, not file://):

```
python -m http.server 8000
```

Then open http://localhost:8000 (production) or http://localhost:8000/qa/ (QA).

## Deployment

Pushed to `main` → published by GitHub Pages at `trpa-agency.github.io/tools`.

To cut over to the tools.trpa.gov custom domain later:

1. Add a DNS CNAME record pointing `tools.trpa.gov` to `trpa-agency.github.io`.
2. Add a `CNAME` file at the repo root containing `tools.trpa.gov` (or set the custom domain in Settings → Pages, which commits the file).
3. Enforce HTTPS in Settings → Pages once the certificate provisions.

Do not commit the `CNAME` file before DNS is in place, GitHub Pages redirects the github.io URL to the custom domain, which breaks the site if the domain does not resolve.
