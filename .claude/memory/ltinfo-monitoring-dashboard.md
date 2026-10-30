---
name: ltinfo-monitoring-dashboard
description: LT Info Monitoring Dashboard pages live in trpa-agency/ltinfo-monitoring-dashboard; the QA gallery carries one card to its index
metadata:
  type: project
---

The LT Info Monitoring Dashboard prototype pages live in trpa-agency/ltinfo-monitoring-dashboard, served at trpa-agency.github.io/ltinfo-monitoring-dashboard/. Its index.html is generated from templates/index.html by scripts/scaffold_programs.py, with one single-page dashboard per program under a folder per threshold category.

The tools QA gallery shows it as one beta card in apps.json (id `ltinfo-monitoring-dashboard`) that links out to the index. No per-program or per-page cards. On Oct. 30, 2026 that card replaced four cards that pointed at trpa-agency.github.io/Monitoring/ltinfo/ (bike-ped, noise, forest-health, and the review frame).

Lake Tahoe Currents still lives at trpa-agency.github.io/Monitoring/Currents/ and was not part of the move.

qa/data/design-system.html, section 19 (LT Info Monitoring), still loads the fragment kit and links its files from trpa-agency/Monitoring/ltinfo (`DEFAULT_BASE`). If that folder is retired, repoint or drop the section.

**Why:** one repo owns the monitoring program pages, so the tools site links to it instead of mirroring its pages.
**How to apply:** add new monitoring program pages in that repo, not as cards here; keep the single card's description current if the index changes shape.
