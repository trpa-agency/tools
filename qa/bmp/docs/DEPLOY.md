# Deploying bmp.trpa.gov

Target: `https://bmp.trpa.gov`, replacing `https://www.tahoebmp.org` (ASP.NET on a TRPA or DTS server).

## 0. Where it lives today

The site is developed as a beta app in the TRPA Tools repo at `qa/bmp/` and reviewed at `https://trpa-agency.github.io/tools/qa/bmp/` (listed on the QA gallery under Environmental Improvement). Every link inside the site is relative, so the folder can be served from any root, and the folder carries its own copy of `assets/trpa-tokens.css`.

**Production home, decided Oct. 22, 2026: its own repository, `trpa-agency/bmp`, served by GitHub Pages at `https://bmp.trpa.gov`.** Not yet. The site stays in this repo under `qa/` through the BMP Database integration phase (`FORMS.md`), and the move is the last step before cutover. Reasons for a repo of its own: the short URL on brochures, the hotline recording, and the certificates resolves directly instead of through a redirect; GitHub Pages allows one custom domain per repository, so the domain needs its own repo; the program's content (pages, JSON, forms, documents) gets its own history and its own access list, so Communications can be given write access without touching the rest of TRPA Tools; and the BMP Database integration scripts travel with the site. The cost is a second deploy to keep in step with the shared tokens, and the TRPA Tools gallery links out to the site instead of hosting it.

This supersedes the Oct. 20, 2026 plan (a top-level `bmp/` folder in this repo at `tools.trpa.gov/bmp/`, with `bmp.trpa.gov` as a redirect), which `IMPROVEMENTS.md` and the project notes referred to.

### In plain language: a site of its own on GitHub, or a section of trpa.gov in WordPress

A site of its own at bmp.trpa.gov:

- Everything the program needs is one site: the property search, the map, the interactive drawings, the handbook, the forms. None of those can be built inside WordPress; they would be embedded in frames and maintained separately anyway.
- Nothing to patch and nothing to hack. There is no server, no database, and no plugins on the public side, which is what failed on the old tahoebmp.org server. Hosting is free.
- Changes go live in about a minute and every change is recorded with who made it and when, so anything can be undone.
- A WordPress update cannot break the tools, and the tools cannot slow trpa.gov down.
- The cost: content is edited as plain files in GitHub rather than in the WordPress editor, which takes a short walkthrough, and it is a second site to track in analytics and audits.

A section of trpa.gov in WordPress:

- One site, one editor Communications already uses, one menu, one search, one analytics account.
- The tools still have to be built and hosted outside WordPress and embedded, so both have to be maintained, and embeds are the part that breaks with theme updates and on phones.
- About 300 documents (488 MB of PDFs and drawings) would go into the media library, which is not built to organize a collection that size.
- Each edit goes through the WordPress workflow with no preview site, and the structured content (127 fact sheets, 77 photos, the document registry) becomes hand-maintained pages.

The middle path, if the program wants its prose in WordPress: a short trpa.gov/bmp landing page that Communications owns, linking to the tools on bmp.trpa.gov. The words live where the editor is; the tools live where they can be maintained.

## 1. Move to the new repository

When the must-fix items in `IMPROVEMENTS.md` are closed and the integration steps in `FORMS.md` are done:

1. Create `trpa-agency/bmp`, public like this repo, with Pages set to deploy from `main` at the root.
2. Carry the folder's history over rather than copying files: in this repo, `git subtree split --prefix=qa/bmp -b bmp-export`, then push that branch to the new repo's `main`. The folder's contents become the repository root, so `index.html` is the site root and every relative link keeps working.
3. In the new repo: add a `CNAME` file containing `bmp.trpa.gov`; change the footer's TRPA Tools link from `../../` to `https://tools.trpa.gov/`; add the `404.html` with the legacy path map from section 3; keep `assets/trpa-tokens.css` in step with the copy in this repo when the design system changes. The scripts in `scripts/` already resolve paths from the folder root and need no change; the integration job's config lives there too, with its secrets in a gitignored `.env`.
4. In this repo: remove `qa/bmp/`, keep the three thumbnails, and point the `bmpsite`, `bmpsearch`, and `bmpmap` entries in `apps.json` at `https://bmp.trpa.gov/...` as external links without `"beta": true`.
5. Pages publishes within about a minute at `https://trpa-agency.github.io/bmp/`, and at `https://bmp.trpa.gov` once the DNS in section 2 resolves.

## 2. DNS and the domain (DTS request)

1. Verify `trpa.gov` for the `trpa-agency` organization first (Organization settings, Pages, Verified domains; GitHub gives a TXT record `_github-pages-challenge-trpa-agency.trpa.gov`), so no one outside the org can claim a `*.trpa.gov` Pages site. This is the same step tools.trpa.gov needs, so it may already be done.
2. Ask DTS for `bmp.trpa.gov` as a CNAME to `trpa-agency.github.io.` (a subdomain needs no A records). A short TTL during cutover makes a rollback quick.
3. In the new repo's Pages settings, enter the custom domain. GitHub checks the DNS and issues the certificate, usually within the hour; then turn on Enforce HTTPS.
4. Leave `tools.trpa.gov` as it is; the BMP cards there link out to the new domain.

If the program wants the short URL before the move, DTS can point `bmp.trpa.gov` at the old IIS server with a rewrite rule to the QA address in the meantime; it is optional and goes away at the move.

## 3. Redirect the old site

Keep `tahoebmp.org` alive long enough to redirect. Two parts:

**Pages** (301 to the new site). IIS `web.config` rewrite rules for the old server, or the equivalent on whatever fronts it:

New paths below are relative to `https://bmp.trpa.gov/` (while in QA, `https://trpa-agency.github.io/tools/qa/bmp/`).

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

The new repo's `404.html` carries the same lookup table (keyed on the lowercase legacy path), so a blanket redirect of `tahoebmp.org/* -> bmp.trpa.gov/*` still lands users on the right page.

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
- Point the `bmpsite`, `bmpsearch`, and `bmpmap` entries in `apps.json` at `bmp.trpa.gov` (category `eip`, no longer beta); retire the gis.trpa.org BMP Mapping Tool card once the new map page replaces it.
- Ask the LT Info product manager to have the Parcel Tracker's "View this Parcel in the BMP Database" link point at `bmp.trpa.gov/search.html?apn=<APN>`.
- Update trpa.gov links that point at tahoebmp.org.
