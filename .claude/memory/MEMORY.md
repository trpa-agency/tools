# Project notes index

One line per note. Each note is a markdown file in this folder.

- [EIP Funding Priorities Survey123](eip-priorities-survey123.md): qa/eip/funding-priorities.html; form 06f26df8…, public view without email, frozen field names, dedupe by hashed email; tiers P1-P3, round FY28, 10 LTRA criteria, FEATURES.voting off (group-by-group view since Oct. 19, 2026)
- [EIP data snapshot](eip-data-snapshot.md): EIP tools read trpa-agency.github.io/EIP/data; LT Info moved to internalapi.laketahoeinfo.org (anonymous, no key), old WebServices routes dead; keep legacy field names
- [TRPA Tools site](trpa-tools-site.md): trpa-agency/tools at trpa-agency.github.io/tools (tools.trpa.gov, no DNS yet); beta under qa/, apps.json registry; maps repo merged in Oct. 14, 2026, github.io/maps 404s; work on mtb-edits, merge to main
- [Internal CORS issue](internal-cors-issue.md): office-network fetches to maps.trpa.org fail on CORS; JSONP callback= works around it, locator uses it as a fallback
- [UMD libs before ArcGIS SDK](plotly-before-arcgis-sdk.md): Plotly, AG Grid, jsPDF must load before Dojo or they never register; jsPDF 2.5.2 is on jsDelivr, not cdnjs
- [Design system tokens](design-system-tokens.md): assets/trpa-tokens.css shared tokens (data-brand="eip" | "tahoe-living"); qa/data/design-system.html documents it; write CSS against --brand-*
- [Cumulative Accounting layer quirks](cumulative-accounting-layer.md): assessor fields all null, El Dorado APNs zero-padded from 2018, genealogy needs apn_old <> apn_new
- [BMP site](bmp-site.md): qa/bmp rebuilds tahoebmp.org for bmp.trpa.gov (needs its own repo for the domain); content in data/*.json, documents still on tahoebmp.org via docBase (488 MB measured), search on BMP_Status/MapServer/5 with client-side APN dash patterns; plan in qa/bmp/docs/DEPLOY.md, verification and improvement plan in qa/bmp/docs/IMPROVEMENTS.md, staff page review reconciled in qa/bmp/docs/CONTENT-PLAN.md (XFA PDFs never open in browsers; 2024 Retrofit Packet lives on trpa.gov); forms rebuilt per qa/bmp/docs/FORMS.md (AcroForm log from scripts/build_forms.py, Survey123 XLSForms in forms/survey123 created in Connect but unpublished, submission destination undecided, links in BMP.config); role to-do list in qa/bmp/docs/NEXT-STEPS.md
- [Locator basin export](locator-basin-export.md): basin inset is all client-side layers (mask cut from the TRPA boundary, no MapServer/15); per-tile service queries outran the 8 s settle cap and left white rectangles; a hidden browser pane pauses rAF and fakes the same symptom
