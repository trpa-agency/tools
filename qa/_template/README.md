# Beta app template

The starting point for every pod-built beta app. Single-file HTML on the TRPA stack: Calcite, Plotly, AG Grid, and the ArcGIS Maps SDK, loaded from CDN in that order (UMD libraries must load before the SDK or Dojo swallows them).

## Stamp it out

1. Copy `index.html` to `qa/<category>/<app-slug>.html`. The relative asset paths (`../../assets/`) assume that depth; adjust if the app gets its own folder like `qa/bmp/`.
2. Fill the TODOs: title, description, header, APP config, data wiring. Delete the tabs, libraries, and builders the app does not use; an app with no map should not load the SDK.
3. Pick the brand: agency is the default, `data-brand="eip"` or `data-brand="tahoe-living"` on `<body>` switches the tokens. Swap the Google Fonts link and the `BRAND_COLORS`, `BRAND_FONT`, and `BRAND_TEXT` constants to match (values in the brand skills and `qa/data/design-system.html`).
4. Register the app in `apps.json` with `"beta": true`, a thumbnail in `assets/thumbs/`, and the `qa/...` URL so it appears in the QA gallery.
5. Before anyone outside the pod sees it, run the `trpa-dashboard-qa` checklist.

## Conventions baked in

- Styles are written against the semantic tokens in `assets/trpa-tokens.css` (`--brand-*`, `--gray-*`), never raw hex, so one file carries any brand.
- Plotly: `displayModeBar: false`, `responsive: true`, `hovermode: 'x unified'`, transparent backgrounds, brand colorway.
- AG Grid 33 Theming API (`themeQuartz.withParams`), no legacy theme CSS. Pagination on for reporting tables, off for working surfaces.
- `queryFeatures` handles ArcGIS REST pagination. Office-network CORS on maps.trpa.org has a JSONP workaround; see `.claude/memory/internal-cors-issue.md`.
- `noindex` and the BETA chip stay until the app is promoted out of `qa/`.

The pod process that uses this template is in `pods/README.md`.
