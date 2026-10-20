---
name: bmp-site
description: "qa/bmp is the rebuild of tahoebmp.org (TRPA Stormwater Management Program) headed for bmp.trpa.gov: 12 static pages in the EIP brand, a Property BMP Status Search on BMP_Status/MapServer/5, content in data/*.json, documents still served from tahoebmp.org via docBase; deployment plan and open decisions in qa/bmp/docs/DEPLOY.md"
metadata:
  node_type: memory
  type: project
  modified: 2026-10-20T19:00:00.000Z
---

`qa/bmp/` replaces https://www.tahoebmp.org (ASP.NET, "Copyright 2021 Lake Tahoe EIP"), the TRPA Stormwater Management Program site. Built Oct. 20, 2026 from a full inventory of the old site; intended home is bmp.trpa.gov, which needs its own repository because a Pages repo gets one custom domain (see `qa/bmp/docs/DEPLOY.md`, section 0). Registered in `apps.json` as `bmpsite` (the site) and `bmpsearch` (the search tool), both beta, category eip.

Structure: one static HTML file per page with the header, nav, and footer copied into each (change them with a find and replace across `qa/bmp/*.html`); `assets/site.css` imports the shared `trpa-tokens.css` and the page uses `data-brand="eip"`; `assets/site.js` renders document lists, the handbook, the gallery, and the home page counts, and has `BMP.query()` (fetch with the JSONP fallback). Content lives in `data/documents.json` (84 items, `docBase` says where files are served from), `data/handbook.json` (chapters plus the Chapter 4 toolkit, 127 fact sheets and PDF/DWG drawings), and `data/gallery.json` (77 photos, migrated and resized into `assets/gallery/` by `scripts/fetch_legacy_images.py`, which needs Pillow from arcgispro-py3).

`search.html` is the rebuilt BMP Database search: AG Grid 33 plus the ArcGIS SDK against `https://maps.trpa.org/server/rest/services/BMP_Status/MapServer/5` (61,271 parcels; fields `APN`, `ParcelStreet`, `BMPStatus` BMP/SCO/NOBMP, `CertNo`, `CertDate` as `yyyy/mm/dd` strings, `SourceCertNo`, `SiteConstraint` 'True'/'False', `AreaWide`, `AreaWidePlanName`, `EvaluationComplete` 0/1, `Rvkd`, `OwnerName`, `OWN_FULL`). `REPLACE()` is not supported in where clauses, so APN search builds dashed patterns client side (3-3-2 Washoe and Carson City, 3-3-3 El Dorado and Placer, 4-2-3-3 Douglas). Certificates print on LT Info at `parcels.laketahoeinfo.org/parcels/<APN>`; the old toolkit's agent login and online evaluation requests are not replicated. Owner-name search is on for parity with the old tool and is easy to remove.

Documents: all PDFs, DWGs, and forms still point at tahoebmp.org (`docBase`). Measured Oct. 20, 2026: 292 files, 488 MB, of which the 2021 workshop MP4 is 282 MB and the complete handbook PDF 64 MB; everything else is about 143 MB. `scripts/fetch_documents.py --download` mirrors them into `documents/`. `Documents/BMPHandbook/Ch5_4_FertManPlnEx.pdf` was already a dead link on the old site.

**How to apply:** Edit content in the JSON files, not the HTML, when it is a document, drawing, or photo. Keep the folder self-contained (relative links only) so it can move to its own repo. Related: [[trpa-tools-site]], [[design-system-tokens]], [[internal-cors-issue]], [[plotly-before-arcgis-sdk]].
