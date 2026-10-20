# Lake Tahoe BMPs: verification and improvement plan

Verification run on Oct. 20, 2026 against the local copy of `qa/bmp/` (served at `http://localhost:8123/qa/bmp/`), the day the site was built. Checks were automated where possible and the method is named for each item so they can be rerun. Items marked **fixed** were changed during the review and are in the same commit as this file.

## 1. What was verified

| Area | Method | Result |
|---|---|---|
| Internal links and anchors | Python parse of all 12 pages; every `href`, `src`, and `data-doc` resolved against the folder | 0 broken files or images. Anchors that JavaScript renders (resource sections, toolkit sections, gallery groups) confirmed present after load. |
| External links | HEAD or GET on 59 distinct URLs from the pages and `documents.json` | 58 return 200. One host (meeksbayfire.com) refuses non-browser clients but loads in a browser. **Fixed:** TRPA code of ordinances (404) now points at `trpa.gov/regional-plan/#code`; North Lake Tahoe FPD moved from `.net` to `nltfpd.org`; the UNR "Fire Adapted Communities" PDF moved to `naes.unr.edu/publication.aspx?PubID=2370`. |
| Legacy documents | HEAD on all 292 relative document paths in `documents.json` and `handbook.json` | 291 reachable on tahoebmp.org (488 MB total). One link was already dead on the old site (Fertilizer Management Plan Example) and was dropped. |
| Parity with tahoebmp.org | Headless Chrome dump of 14 legacy pages; every href compared with the new site and registries | 325 legacy links, all carried over except the dead PDF above, the old site's own CSS and font files, and the Lahontan TMDL link. **Fixed:** TMDL link added on About BMPs. |
| Page structure | Parse: one `h1` per page, no heading level skipped, every `img` has `alt`, every input has a label, `_blank` links carry `noopener` | **Fixed:** Maintenance and Contact opened with an `h3` under the `h1`. Everything else passed. |
| Accessibility (WCAG 2.1 AA plus best practice) | axe-core 4.10.2 run in the browser on all 12 pages, search page with results loaded | Content pages: 0 violations after fixes. **Fixed:** help text (`--gray-text`) was 4.3:1 on the gray page background; now 5.4:1. Solid blue buttons used EIP Blue (4.45:1); now the text-safe step `#0068A8`. Search page: two findings remain inside AG Grid (section 3). |
| Search tool | Browser runs of each mode against the live service | APN with dashes, APN without dashes (`12205101`), Douglas 13-digit APN, address, owner (hits the 2,000-row cap with a notice), certificate number, and a no-match query all behave. Detail panel, map zoom, LT Info link, and CSV export present. **Fixed:** parcels with no situs address carry the literal `NONE`; now shown as "No situs address on file". |
| Home page counts | Live query results compared with direct REST counts | 19,526 BMP, 1,437 source control, 4,709 evaluated without certificate, 61,271 parcels. Match. |
| Responsive layout | Real 375 px viewport in the browser pane: `scrollWidth` equals `innerWidth` on home and search; nav collapses to a menu button; grid scrolls inside its own box | Pass. (Headless captures at 390 px are misleading on Windows because Chrome enforces a wider minimum window.) |
| Page weight | `performance` resource entries | Content pages 280 to 330 KB and 13 to 37 requests. Search page 780 KB and 78 requests (ArcGIS SDK, AG Grid, basemap tiles). Gallery loads thumbnails lazily; full images only in the lightbox. |
| Console | Error-level messages on every page, then a clean headless Chrome run with the server log watched | None from site code. The Claude browser pane logged 404s for `/qa/bmp/trpa-tokens.css` on every page; a headless Chrome load of the same page requests only `assets/trpa-tokens.css` (200) and nothing else, so the 404 is the pane's own prefetch, not the site. |
| TRPA style | Em dash, en dash, symbol, and Oxford comma scan of visible text | No dashes or symbols in prose. Three Oxford comma hits were read and are correct. |
| Secrets and local paths | grep for `file:///`, `localhost`, `C:\\`, tokens | None in the site files. (`localhost` appears only in `.claude/launch.json`.) |

Not verified here: Safari, Firefox, and Edge rendering; real phone testing; behavior on the TRPA office network (the JSONP fallback is in place but was exercised only from outside); Lighthouse scores; screen reader walkthrough.

## 2. Must fix before bmp.trpa.gov goes live

1. **Decide where the documents live** and move them. Today every PDF, DWG, DOC, and XLSX still downloads from tahoebmp.org. Recommended split and the mechanics are in `DEPLOY.md`, section 4 (video to Vimeo, chapters in the repo, decide on the 64 MB complete handbook). Until this is done the old server cannot be turned off.
2. **Promote to `tools.trpa.gov/bmp/`.** The production home is a top-level `bmp/` folder in this repo (decided Oct. 20, 2026); `bmp.trpa.gov` becomes a redirect to it. The move is `git mv qa/bmp bmp` plus the `apps.json` entries, then the redirect request to DTS (`DEPLOY.md`, sections 0 to 3). Everything stays under `qa/` until the items on this list are closed.
3. **Redirects from tahoebmp.org**, page by page, per the table in `DEPLOY.md`. The `?apn=` query string on the old search URL is already honored by the new search.
4. **Decide the fate of the BMP Toolkit agent workflow.** The old `bmptoolkit/` had an agent login and online evaluation requests. The new site routes people to the hotline, email, and LT Info. If staff rely on the agent side, it needs a home (old server, LT Info, or an Accela form) before the old site goes dark.
5. **Owner-name search policy.** It is on for parity. Confirm with the program lead that a public owner lookup is still wanted; removal is one segmented-control item in `search.html`.
6. **Content review by program staff.** The copy was carried over from the old site with light editing to TRPA style. Someone who runs the program should read Get a Certificate, Small BMP Retrofit Plan, and Maintenance for anything that has changed since 2021 (thresholds such as 10 cubic yards and 400 square feet, the 2021 workshop materials, the service providers list).

## 3. Should fix soon

- **AG Grid accessibility findings.** axe reports `aria-required-children` on `.ag-root` and `scrollable-region-focusable` on the grid viewports. These come from AG Grid Community's own DOM, not from site code. `ensureDomOrder: true` is set. Options: upgrade when AG Grid resolves it, or offer a plain list view of results for screen reader users (the detail panel already carries every field as text).
- **Search results on phones.** The grid shows five columns in a horizontally scrolling box, which works but is not comfortable. A card list under 700 px (APN, address, status chip, one line of certificate info) would read better and needs no new data.
- **Map legend and a non-map alternative.** The map colors parcels by status but has no legend. Add the ArcGIS Legend widget (one line) and keep the detail panel as the text equivalent.
- **"Request an evaluation" path.** The button opens a prefilled email. A short form (Survey123 or an Accela link) would give staff structured requests. Check what the program prefers.
- **Gallery image weight.** 77 lightbox images total about 20 MB (1,280 px, quality 78). They load one at a time, so pages stay light, but a WebP pass (`scripts/fetch_legacy_images.py` can be extended) would roughly halve the folder.
- **Print styles for the search detail.** People print certificates and status pages. A `@media print` rule that shows only the detail panel would make "print this page" useful.

## 4. Nice to have

- **Analytics.** The old site had none that is visible. Add the agency's standard analytics snippet (whatever trpa.gov uses) so the program can see which resources are used.
- **Search by catchment or area-wide project.** The service carries `Catchment` and `AreaWidePlanName`; a fifth search mode would let jurisdiction staff list parcels in a drainage area.
- **Status summary chart.** A small Plotly bar of certificates issued per year (from `CertDate`) on the home page or search page would show program progress with no new data source.
- **Spanish.** The NRCS drawings and the contractors manual exist in Spanish and are linked. A Spanish version of the home page and Get a Certificate page would match the audience the Spanish materials were made for.
- **BMP finder by situation.** A short guided flow ("I have a dirt driveway", "my roof drips onto bare soil") that maps answers to the commonly prescribed BMPs and the matching toolkit sheets.
- **Lightbox captions with practice links.** Each gallery photo could link to the toolkit fact sheet for that practice; `gallery.json` would gain a `toolkit` key per image.
- **Dark mode.** The tokens file has no dark palette yet; out of scope until the design system adds one.

## 5. Keeping it verified

Rerun before any deploy:

1. `python scripts/fetch_documents.py` (document reachability and size).
2. Open every page with the browser console showing; no errors.
3. Search: one query per mode, including a 13-digit Douglas APN and a nonsense address.
4. axe on `index.html`, `resources.html`, and `search.html` with results loaded.
5. A phone, not an emulator, on the home page and the search page.
6. The `trpa-dashboard-qa` checklist on `search.html`.
