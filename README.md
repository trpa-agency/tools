# TRPA Tools

Official maps, apps, and tools of TRPA, to be served at **tools.trpa.gov** via GitHub Pages (today at trpa-agency.github.io/tools). This site replaces the gallery at gis.trpa.org as apps are migrated and new apps are built. It carries forward the history of `trpa-agency/maps` (apps.trpa.gov), which it replaces.

## Structure

```
tools/
├── index.html          # Main gallery, all apps grouped by category
├── apps.json           # Single source of truth for the app registry
├── 404.html            # Branded not-found page
├── assets/
│   ├── site.css        # Shared styles (TRPA brand)
│   ├── gallery.js      # Shared gallery renderer
│   ├── trpa-tokens.css # Shared design tokens (see general/design-system.html)
│   ├── fonts/          # Self-hosted Open Sans and Lexend Deca
│   └── thumbs/         # App thumbnails
├── planning/           # Planning apps (zoning, housing, shoreline)
├── transportation/     # Transportation apps (transit, active transportation, Transportation Tracker)
├── permitting/         # Permitting apps (parcels, permits, public notice, completeness review)
├── eip/                # Environmental Improvement Program apps (stormwater, forest health, SEZ)
├── general/            # General viewers, galleries, and the Design System reference
├── monitoring/         # Threshold, climate, lake clarity, wildfire, and smoke dashboards (smoke-map.html + purpleair-tahoe.json)
├── storymaps/          # Story Map Gallery, live from ArcGIS Online
├── surveys/            # Survey Gallery, live from ArcGIS Online; surveys.json groups, describes, and hides forms
├── data/               # Open data, the Tahoe Data Inventory, and the Open Data Policy
└── docs/               # Planning documents
```

Each category folder has an `index.html` landing page that lists only its apps. Apps built here live inside their category, as a single file (`permitting/public-notice.html`) or a subfolder for multi-file apps (`planning/localplans/` to `tools.trpa.gov/planning/localplans/`). There is no top-level `tools/` folder; on tools.trpa.gov that path would read twice.

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

The Tahoe Data Inventory ([data/data-inventory.html](data/data-inventory.html)) reads its rows
from `data/data-inventory.json`, which is rebuilt by `scripts/build_inventory.py` (stdlib-only
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

Then open http://localhost:8000.

## Deployment

Pushed to `main` → published by GitHub Pages at `trpa-agency.github.io/tools`.

To cut over to the tools.trpa.gov custom domain later:

1. Add a DNS CNAME record pointing `tools.trpa.gov` to `trpa-agency.github.io`.
2. Add a `CNAME` file at the repo root containing `tools.trpa.gov` (or set the custom domain in Settings → Pages, which commits the file).
3. Enforce HTTPS in Settings → Pages once the certificate provisions.

Do not commit the `CNAME` file before DNS is in place, GitHub Pages redirects the github.io URL to the custom domain, which breaks the site if the domain does not resolve.
