# Long Range and Transportation Planning pod

**Status:** active, beta tools shipping and a deep data engineering bench in `trpa-agency/Transportation`

## In flight: web tools

- [What Can I Do on My Parcel?](https://trpa-agency.github.io/Planning/LongRange/html/parcel-lookup.html) and [Where Can I Build?](https://trpa-agency.github.io/Planning/LongRange/html/district-explorer.html): zoning and permitted-use lookups.
- [Housing Progress Since 2012](https://trpa-agency.github.io/Planning/LongRange/html/multifamily-housing.html) and [Deed Restriction Explorer](https://trpa-agency.github.io/Planning/LongRange/html/deed-restriction-explorer.html). The housing dashboard is in active staff review cycles, with a pre-commit hook keeping its text review sheet in step with the page: a working model for the pod's QA and review step.
- [Transit Funding Tool](https://trpa-agency.github.io/Transportation/TransitFundingTool/model/transit-funding-model.html): regional transit funding model for the RTP funding and implementation strategy. Single-file model page plus concept mockups, under active review with the domain lead. Lives in `trpa-agency/Transportation/TransitFundingTool`.

## In flight: data engineering (`trpa-agency/Transportation`)

- Travel Demand Model: the most active folder in the repo since August.
- SMART Phase 1: USDOT SMART grant traffic camera ETL. Pulls vehicle, vulnerable road user, safety event, and speed data from AI-enabled cameras into the `Transportation_SMART` feature service, feeding an ArcGIS dashboard, Tahoe Open Data, and a DOI-archived data package.
- Tahoe Effective Population Model (TEPM): Python port of the R-Shiny model. Scenario configs estimate people physically present in the region, shared machinery with the Housing EIS forecast.
- High Injury Network crash analysis: SWITRS and NDOT crash data into per-mode HINs and hot spots on the street network, with a web map.
- RTP charts, traffic counts (AADT, PeMS), Replica, TSMO, and network analysis notebooks.

## In flight: elsewhere

- Transportation Resilience Improvement Plan (TRIP) risk index: multi-hazard vulnerability and criticality analysis, in progress outside this repo.

## Candidate problems

- Several of the data engineering outputs above have no browser-facing view yet; the gap between pipeline and audience is a recurring pod-shaped problem here.
- Add more from the next sit-down.

## Start an engagement

Copy `../_intake-template.md` here as `intake-YYYY-MM-DD.md`.
