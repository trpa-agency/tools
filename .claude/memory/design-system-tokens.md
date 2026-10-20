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

**Why:** Existing tools each inline their own `:root` tokens with small drifts (gray-text values, EIP blue text step, radius). The token file is the single place to fix that; the page documents what ships, not aspirations.

**How to apply:** New tools link the tokens file (or paste its `:root` block when they must be self-contained) and write CSS against `--brand-*` rather than `--trpa-*`. Put `data-brand` on `<body>` for EIP or Tahoe Living tools; the shell stays agency. Keep the page in sync when a component convention changes. Related: [[plotly-before-arcgis-sdk]], [[trpa-tools-site]].
