---
name: cumulative-accounting-layer
description: "Quirks of the Cumulative_Accounting parcel history service (null value fields, El Dorado 2018 renumbering, genealogy noise) learned while building the Parcel Change Explorer (qa/permitting/parcel-explorer.html)"
metadata:
  node_type: memory
  type: project
  originSessionId: 5bcc5440-ef8d-419f-bb0a-f08468122ed7
  modified: 2026-10-20T04:45:20.306Z
---

Cumulative_Accounting/MapServer/0 (Parcel Development History) is one polygon per parcel per year, 2012 to 2025, about 61,000 rows per year, maxRecordCount 2000, pagination and statistics supported.

- AS_SUM, TAX_SUM, YEAR_BUILT, APO_ADDRESS, OWNERSHIP_TYPE, EXISTING_LANDUSE, COUNTY_LANDUSE_DESCRIPTION, Assessor_Units, and PPNO are NULL in every row of every year. Current values must come from Parcels/FeatureServer/0, where they are populated.
- El Dorado County (COUNTY = 'EL', includes CSLT) renumbered all parcels in 2018: XXX-XXX-XX became XXX-XXX-0XX (leading zero added to the last segment). 2012 to 2017 rows use the 10-character form, 2018 onward the 11-character form. Pad to join. The genealogy table does NOT record this renumbering.
- Cumulative_Accounting/MapServer/1 (Tahoe APN Genealogy) has 42,000 rows but about 29,000 are ACCELA "rename" events where apn_old = apn_new. Always filter `apn_old <> apn_new` (about 12,500 real split, merge, and rename rows).
- REGIONAL_LANDUSE codes: RES, TOR, COM/PS, REC, CONS, plus null and ' ' (space) for unknown.
- The Parcel Change Explorer built on this was added to the maps repo Sept. 29, 2026 and now lives at `qa/permitting/parcel-explorer.html` in the tools repo.

**Why:** These took a round of profiling to discover and will bite any future analysis of this layer.

**How to apply:** When querying parcel history, pad EL APNs, ignore the null assessor fields, and filter genealogy self-renames. Related: [[trpa-tools-site]].
