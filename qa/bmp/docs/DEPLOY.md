# Deploying bmp.trpa.gov

Target: `https://bmp.trpa.gov`, replacing `https://www.tahoebmp.org` (ASP.NET on a TRPA or DTS server).

## 0. Where it lives today

The site is developed as a beta app in the TRPA Tools repo at `qa/bmp/` and reviewed at `https://trpa-agency.github.io/tools/qa/bmp/` (listed on the QA gallery under Environmental Improvement). Every link inside the site is relative, so the folder can be served from any root.

GitHub Pages allows one custom domain per repository, and the Tools repo's domain is `tools.trpa.gov`. So `bmp.trpa.gov` needs one of:

- **Its own repository** (`trpa-agency/bmp`): move the `qa/bmp/` folder there, add a `CNAME` file containing `bmp.trpa.gov`, and a root `404.html` that maps the legacy `.aspx` paths (table in section 3). This is the clean option and the one the rest of this document assumes.
- **A path under tools.trpa.gov** (`tools.trpa.gov/bmp/`) with `bmp.trpa.gov` redirecting to it from the old server or a redirect service. Simpler to host, but the short URL on brochures would be a redirect forever.

## 1. Repository and Pages (own-repo option)

1. Create `trpa-agency/bmp` (public) and push the `qa/bmp/` contents to `main`, plus `CNAME` and the legacy-path `404.html`.
2. Settings, Pages: Source "Deploy from a branch", branch `main`, folder `/ (root)`.
3. The `CNAME` file names `bmp.trpa.gov`; GitHub fills the custom domain field from it.
4. Once DNS resolves (next section), check "Enforce HTTPS". The certificate issues within an hour of DNS propagating.
5. Interim URL while DNS is pending: `https://trpa-agency.github.io/bmp/`.

## 2. DNS (DTS request)

Ask DTS to add:

| Record | Host | Value | TTL |
|---|---|---|---|
| CNAME | `bmp.trpa.gov` | `trpa-agency.github.io.` | 3600 |

Recommended first: verify `trpa.gov` for the `trpa-agency` organization (Organization settings, Pages, Verified domains). GitHub gives a TXT record (`_github-pages-challenge-trpa-agency.trpa.gov`) that DTS adds once; after that no one outside the org can claim a `*.trpa.gov` Pages site. The same verification covers `tools.trpa.gov` and `data.trpa.gov`.

## 3. Redirect the old site

Keep `tahoebmp.org` alive long enough to redirect. Two parts:

**Pages** (301 to the new site). IIS `web.config` rewrite rules for the old server, or the equivalent on whatever fronts it:

| Old | New |
|---|---|
| `/`, `/Default.aspx` | `https://bmp.trpa.gov/` |
| `/BMPs.aspx`, `/BMPS.aspx` | `/get-certified.html` |
| `/SmallBMPRetro.aspx` | `/small-retrofit-plan.html` |
| `/BMPProblem.aspx`, `/WhatAreBMPs.aspx`, `/PrescribedBMPs.aspx`, `/*Ex.aspx` | `/about-bmps.html` |
| `/Maintenance.aspx` | `/maintenance.html` |
| `/BMPHandbook.aspx` | `/handbook.html` |
| `/BMPHandbookCh4.aspx` | `/handbook.html#toolkit` |
| `/BMPResources.aspx` | `/resources.html` |
| `/photogallery.aspx`, `/Photogallery_*.aspx` | `/gallery.html` |
| `/Realtors.aspx` | `/realtors.html` |
| `/Fertilizer.aspx` | `/fertilizer.html` |
| `/Contact.aspx` | `/contact.html` |
| `/bmptoolkit/searchBMP.asp` | `/search.html` (query string `?apn=` is honored) |

A root `404.html` on the new site that maps these paths (a small lookup table in JavaScript keyed on the lowercase legacy path) means a blanket redirect of `tahoebmp.org/* -> bmp.trpa.gov/*` lands users on the right page.

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
- Flip the `bmpsite` and `bmpsearch` entries in `apps.json` from beta to production URLs (category `eip`, alongside the BMP Mapping Tool card).
- Ask the LT Info product manager to have the Parcel Tracker's "View this Parcel in the BMP Database" link point at `bmp.trpa.gov/search.html?apn=<APN>`.
- Update trpa.gov links that point at tahoebmp.org.
