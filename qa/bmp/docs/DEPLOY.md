# Deploying bmp.trpa.gov

Target: `https://bmp.trpa.gov`, replacing `https://www.tahoebmp.org` (ASP.NET on a TRPA or DTS server).

## 0. Where it lives today

The site is developed as a beta app in the TRPA Tools repo at `qa/bmp/` and reviewed at `https://trpa-agency.github.io/tools/qa/bmp/` (listed on the QA gallery under Environmental Improvement). Every link inside the site is relative, so the folder can be served from any root.

**Recommended production home: `https://tools.trpa.gov/bmp/`** (decided Oct. 20, 2026). The site stays in this repo and moves from `qa/bmp/` to `bmp/` at the top level when it is ready, like the other production apps. GitHub Pages allows one custom domain per repository, so `bmp.trpa.gov` becomes a redirect to `tools.trpa.gov/bmp/` rather than a second Pages site. Reasons: one repo and one deploy to maintain, the shared tokens and gallery registry stay in sync, and the domain verification and DNS work already planned for tools.trpa.gov covers it. The trade-off is that the short URL on brochures and the hotline recording will always be a redirect; that is acceptable.

The alternative, a separate `trpa-agency/bmp` repo with `bmp.trpa.gov` as its own Pages domain, remains possible later because every link inside the folder is relative. Only the footer's TRPA Tools link (`../../`) would need to become absolute.

## 1. Promote from qa to production

1. Finish the must-fix items in `IMPROVEMENTS.md` (documents, redirects, agent workflow, owner search, content review).
2. Move the folder: `git mv qa/bmp bmp` on `mtb-edits`, update the two `apps.json` entries (`bmpsite`, `bmpsearch`, plus `bmpmap` if present) from `qa/bmp/...` to `bmp/...` and drop `"beta": true`, then merge to `main`. Pages publishes within about a minute.
3. The site is then at `https://trpa-agency.github.io/tools/bmp/` and, once the tools.trpa.gov DNS exists, `https://tools.trpa.gov/bmp/`.

## 2. DNS and the short URL (DTS request)

`tools.trpa.gov` first: the CNAME to `trpa-agency.github.io.` and the `CNAME` file in this repo, as described in the TRPA Tools notes. Verify `trpa.gov` for the `trpa-agency` organization while DTS is in the DNS (Organization settings, Pages, Verified domains; GitHub gives a TXT record `_github-pages-challenge-trpa-agency.trpa.gov`), so no one outside the org can claim a `*.trpa.gov` Pages site.

Then `bmp.trpa.gov` as a redirect. Options, in order of preference:

| Option | How |
|---|---|
| Redirect on the old tahoebmp.org server | Point `bmp.trpa.gov` (A or CNAME) at the IIS server that hosts tahoebmp.org and add a site binding plus a rewrite rule that 301s every path to `https://tools.trpa.gov/bmp/<mapped path>` (table in section 3). Reuses the server that must redirect tahoebmp.org anyway. |
| Redirect at the DNS or CDN provider | If TRPA's DNS host offers HTTP redirect records (many do), `bmp.trpa.gov -> https://tools.trpa.gov/bmp/` with no server involved. Path mapping is lost, so the old `.aspx` URLs land on the home page. |
| A tiny Pages repo | `trpa-agency/bmp` with `CNAME` and a one-file `index.html` plus `404.html` that JavaScript-redirects to `tools.trpa.gov/bmp/` with the legacy path map. Free and path-aware, but one more repo. |

## 3. Redirect the old site

Keep `tahoebmp.org` alive long enough to redirect. Two parts:

**Pages** (301 to the new site). IIS `web.config` rewrite rules for the old server, or the equivalent on whatever fronts it:

New paths below are relative to `https://tools.trpa.gov/bmp/` (while in QA, `https://trpa-agency.github.io/tools/qa/bmp/`).

| Old | New |
|---|---|
| `/`, `/Default.aspx` | `/` |
| `/BMPs.aspx`, `/BMPS.aspx` | `/get-certified.html` |
| `/SmallBMPRetro.aspx` | `/small-retrofit-plan.html` |
| `/BMPProblem.aspx`, `/WhatAreBMPs.aspx`, `/PrescribedBMPs.aspx`, `/photogallery_rock.aspx` | `/about-bmps.html` |
| `/SingleFamEx.aspx` | `/about-bmps.html#design-single-family` |
| `/MultiFamilyEx.aspx` | `/about-bmps.html#design-multi-family` |
| `/CommGoodEx.aspx` | `/about-bmps.html#design-commercial-with-bmps` |
| `/CommBadEx.aspx` | `/about-bmps.html#design-commercial-without-bmps` |
| `/RegionalEx.aspx` | `/about-bmps.html#design-regional` |
| `/MarinaEx.aspx` | `/about-bmps.html#design-marina` |
| `/WinterEx.aspx` | `/about-bmps.html#design-winterization` |
| `/TempEx.aspx` | `/about-bmps.html#design-temporary-construction` |
| `/Maintenance.aspx` | `/maintenance.html` |
| `/BMPHandbook.aspx` | `/handbook.html` |
| `/BMPHandbookCh4.aspx` | `/handbook.html#toolkit` |
| `/BMPResources.aspx`, `/BMPProfessionals.aspx` | `/resources.html` |
| `/photogallery.aspx`, `/Photogallery_*.aspx` | `/gallery.html` |
| `/Realtors.aspx` | `/get-certified.html#disclosure` |
| `/FAQs.aspx` | `/faq.html` |
| `/Fertilizer*.aspx` | `/fertilizer.html` |
| `/Contact.aspx`, `/WhoAreYou.aspx`, `/Residential.aspx`, `/MultiFamily.aspx`, `/News.aspx`, `/Reporting.aspx`, `/LivingWithFire.aspx`, `/BMPComments.aspx` | `/` |
| `/bmptoolkit/searchBMP.asp` | `/search.html` (query string `?apn=` is honored) |

The Tools repo's root `404.html` can carry the same lookup table (keyed on the lowercase legacy path under `/bmp/`), so a blanket redirect of `tahoebmp.org/* -> tools.trpa.gov/bmp/*` still lands users on the right page.

**Files.** `data/documents.json` has `"docBase": "https://www.tahoebmp.org/"`, so every PDF, DWG, DOC, and XLSX still comes from the old server's `Documents/`, `NRCSDocuments/`, and `documents/` folders. Do not redirect those paths until the files have moved.

## 4. Move the documents

`python scripts/fetch_documents.py` prints the size of every registered file. On Oct. 20, 2026 that was 292 files and 488 MB, but two files are most of it: the 2021 workshop video (`Documents/Videos/BMP_Workshop_Presentation.mp4`, 282 MB) and the complete handbook PDF (64 MB). Everything else, including all 51 DWG drawings (18 MB), is about 143 MB. One legacy link is already dead: `Documents/BMPHandbook/Ch5_4_FertManPlnEx.pdf` (Fertilizer Management Plan Example) returns 404 and has been dropped from `handbook.json`.

Recommended split:

- Put the workshop video on TRPA's Vimeo account (the other BMP videos are already there) and point the `workshop` section item at it.
- Keep the complete handbook as a single PDF only if the 64 MB download is worth it; the chapters cover the same content. GitHub rejects files over 100 MB and warns over 50 MB.
- Mirror the rest into the repo:

- **Host in the repo.** `python scripts/fetch_documents.py --download` mirrors them into `documents/` with the same relative paths. Set `"docBase": "documents/"` and commit. GitHub allows files up to 100 MB and sites up to 1 GB, so this works, but a 150 MB repo is slower to clone. Git LFS is not served by Pages.
- **Host on trpa.gov.** Upload to the WordPress media library or a `/bmp/` folder and set `docBase` to that URL. Paths would need to match, or `documents.json` gets re-pointed item by item.
- **Keep them on the old server** behind a `docs.tahoebmp.org` or similar name until a later phase.

Either way the site only changes in one place, `docBase`, plus the `data-doc` links already in the pages.

## 5. What the static site does not replicate

- The old BMP Toolkit at `tahoebmp.org/bmptoolkit/` had an **Agent Login** and online **evaluation requests**. The new search links to the LT Info Parcel Tracker (which prints certificates) and to the BMP Hotline and email. If staff need the agent workflow, it stays on the old server or moves into LT Info.
- **Certificate printing** happens on LT Info (`parcels.laketahoeinfo.org/parcels/<APN>`, "Print Certificate"). The search detail panel links there.
- **Owner-name search** is on by default for parity with the old tool. The field (`OwnerName`, `OWN_FULL`) is public in the `BMP_Status` service; the site never shows mailing addresses. To turn it off, remove the `owner` item from the segmented control in `search.html`.

## 6. Before go-live

- Run the `trpa-dashboard-qa` checklist on `search.html` (the only app page).
- Confirm `BMP_Status/MapServer/5` field names have not changed (`APN`, `ParcelStreet`, `BMPStatus`, `CertNo`, `CertDate`, `SourceCertNo`, `SiteConstraint`, `AreaWide`, `EvaluationComplete`, `Rvkd`).
- Flip the `bmpsite`, `bmpsearch`, and `bmpmap` entries in `apps.json` from beta to production URLs (category `eip`); retire the gis.trpa.org BMP Mapping Tool card once the new map page replaces it.
- Ask the LT Info product manager to have the Parcel Tracker's "View this Parcel in the BMP Database" link point at `tools.trpa.gov/bmp/search.html?apn=<APN>`.
- Update trpa.gov links that point at tahoebmp.org.
