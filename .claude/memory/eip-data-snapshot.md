---
name: eip-data-snapshot
description: "EIP tools in the tools repo read the trpa-agency/EIP nightly snapshot, which reads the re-platformed Lake Tahoe Info API (internalapi.laketahoeinfo.org, anonymous, no key); the old WebServices routes are dead"
metadata:
  node_type: memory
  type: project
  originSessionId: 5bcc5440-ef8d-419f-bb0a-f08468122ed7
  modified: 2026-10-20T04:44:52.320Z
---

EIP tools in the tools repo (Funding Priorities at qa/eip/funding-priorities.html, the Projects Map, the locator) read the nightly snapshot at https://trpa-agency.github.io/EIP/data/ (projects.geojson for located projects, projects_aspatial.json for regional and unlocated ones; CORS is open). As of Oct. 5, 2026 the snapshot covers all 1,409 Tracker projects in every stage, including Deferred and Terminated, with legacy GetProject field names plus SecuredFunding, UnfundedNeed, and Tags.

Lake Tahoe Info was re-platformed in 2026. The old www.laketahoeinfo.org/WebServices/...{key} routes return the Angular app shell. The backend the Tracker pages call is https://internalapi.laketahoeinfo.org with anonymous GET routes (/projects, /eip-projects/by-number/{eip}, /eip-projects/five-year-list, /eip-projects/mapped-point/feature-collection, /projects/{id}/expenditures, /projects/{id}/location-as-feature-collection, /eip-focus-areas/taxonomy). Swagger and list routes under /eip-projects return 401. The ETL in trpa-agency/EIP (scripts/Build_EIP_ProjectLocations.py) was rebuilt on these routes on Oct. 5, 2026 after the nightly Action had failed since September.

Coverage after the rebuild: 404 active EIP projects (Planning/Design or Implementation), 353 with EstimatedTotalCost and UnfundedNeed, 101 of them fully funded. Jurisdiction and watershed are comma-joined strings whose values contain commas, so match against a known list instead of splitting.

**Why:** Funding Priorities allocates an envelope by UnfundedNeed, and the Projects Map reads the same files; both break if the field names change.

**How to apply:** Keep the legacy field names in the snapshot. If the Tracker API changes again, check what eip.laketahoeinfo.org pages call (performance resource entries) before guessing routes. Related: [[eip-priorities-survey123]], [[trpa-tools-site]].
