---
name: trpa-tools-site
description: "TRPA's app gallery is trpa-agency/tools (TRPA Tools, future tools.trpa.gov, no DNS yet), serving at trpa-agency.github.io/tools; production at top level by category, beta under qa/; the old maps repo and github.io/maps URL are gone (404, no redirect); legacy gis.trpa.org gallery pulls from AGOL group 473e99cc9ecf433a9e04457c71881579"
metadata:
  node_type: memory
  type: project
  originSessionId: 5bcc5440-ef8d-419f-bb0a-f08468122ed7
  modified: 2026-10-20T04:45:00.557Z
---

TRPA's app gallery is the `trpa-agency/tools` repo (local clone Documents\GitHub\tools), branded TRPA Tools and intended for tools.trpa.gov. On Oct. 14, 2026 the old `trpa-agency/maps` repo was merged with history into it, the site was renamed, and beta apps moved under `qa/` with their own gallery pages (qa/eip, qa/general, qa/monitoring, qa/permitting, qa/planning, qa/data, qa/transportation, qa/surveys, qa/storymaps). Production pages stay at the top level by category (planning, transportation, permitting, eip, monitoring, general, data). `apps.json` is the registry (38 apps as of Oct. 19, 2026, 17 of them beta) and `assets/gallery.js` renders the galleries from it.

The custom domain is NOT live: no CNAME file (removed until DNS exists) and no DNS record. The site serves at https://trpa-agency.github.io/tools/. The old https://trpa-agency.github.io/maps/ URL and every path under it return 404 as of Oct. 19, 2026, and github.com/trpa-agency/maps is not public, so old bookmarks, trpa.gov links, and LT Info embeds pointing there are dead; there is no redirect stub. The local Documents\GitHub\maps clone still exists but is frozen; edit the tools repo. Day-to-day work happens on the `mtb-edits` branch and is merged into `main` (Pages serves main, live within about a minute of a push).

Naming history: planned as maps.trpa.gov, renamed apps.trpa.gov on Oct. 13, 2026 after Amy asked for a name that does not collide with maps.trpa.org, then TRPA Tools / tools.trpa.gov on Oct. 14. docs/maps-trpa-gov-proposal.md in the repo is the superseded proposal. DTS adds DNS first, then the CNAME file goes back.

It replaces the legacy gallery at gis.trpa.org, an Esri Public Map Gallery template in an iframe that pulls its app list from ArcGIS Online group `473e99cc9ecf433a9e04457c71881579` (query `https://www.arcgis.com/sharing/rest/content/groups/473e99cc9ecf433a9e04457c71881579/search?f=json` when checking for apps not yet migrated). Eight production gallery entries still point at gis.trpa.org apps on the internal server.

Claude project notes live in `.claude/memory/` in this repo (imported by CLAUDE.md) since Oct. 20, 2026. Older copies in the per-machine maps auto-memory folder are frozen.

**How to apply:** Share links as trpa-agency.github.io/tools/... until DNS exists. Do not point anyone at github.io/maps. Related: [[design-system-tokens]], [[eip-priorities-survey123]], [[internal-cors-issue]].
