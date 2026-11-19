---
name: design-system-tokens
description: "The tools repo has a shared token stylesheet (assets/trpa-tokens.css) and a reference page (qa/data/design-system.html); new tools link the tokens, write CSS against --brand-*, and switch sub-brands with data-brand"
metadata:
  node_type: memory
  type: project
  originSessionId: 5bcc5440-ef8d-419f-bb0a-f08468122ed7
  modified: 2026-10-20T04:45:14.421Z
---

Since Oct. 9, 2026 the repo carries `assets/trpa-tokens.css` (raw palettes, semantic `--brand-*`, `--gray-*`, `--status-*`, `--chart-1..8`, plus the `--calcite-*` mapping) with three brand layers: default agency, `[data-brand="eip"]`, and `[data-brand="tahoe-living"]`. The design system page, now at `qa/data/design-system.html`, documents it with live specimens and a brand switcher; it is in apps.json (id `designsystem`, beta).

A fourth layer, `[data-brand="ltinfo"]`, previews Lake Tahoe Info embeds (platform tokens, not a TRPA brand). `data-site` picks the module: monitoring (default), thresholds, transportation, climate, eip, clarity, parcels, stormwater. Module colors (`--lti-mon-*`, `--lti-thr-*`, `--lti-trn-*`, `--lti-eip-*`, `--lti-clr-*`, `--lti-par-*`, `--lti-sw-*`, `--lti-cl-*`) were sampled from the live sites on Nov. 18, 2026; the shared nav bar is `#0b1f41`, not `--ltinfo-blue`. Climate chart colors come from the Python in trpa-agency/ClimateResilienceDashboard, not from its 2024 style guide document, which describes a palette no chart uses. The page documents this in section 18 (Modules, Climate Resilience Dashboard).

Monitoring Dashboard chart and map palettes (qualitative, sequential green, blue, orange, diverging blue to orange and teal to brown, each in 3, 5, 7, 10 classes, plus two 3 by 3 bivariate grids) live in `assets/ltinfo-monitoring-palettes.json`, with the 10 categories also as `--lti-mon-cat-1..10`; section 19 renders them from the JSON. Built in OKLab with linear lightness (Phosphor's method) and checked with the dataviz validator on `#f7f7f7`.

**Why:** Existing tools each inline their own `:root` tokens with small drifts (gray-text values, EIP blue text step, radius). The token file is the single place to fix that; the page documents what ships, not aspirations.

**How to apply:** New tools link the tokens file (or paste its `:root` block when they must be self-contained) and write CSS against `--brand-*` rather than `--trpa-*`. Put `data-brand` on `<body>` for EIP or Tahoe Living tools; the shell stays agency. Keep the page in sync when a component convention changes. Related: [[plotly-before-arcgis-sdk]], [[trpa-tools-site]].
