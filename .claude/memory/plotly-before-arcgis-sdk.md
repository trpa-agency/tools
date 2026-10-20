---
name: plotly-before-arcgis-sdk
description: "In TRPA dashboards, every UMD library (Plotly, AG Grid, jsPDF) must load BEFORE the ArcGIS Maps SDK or Dojo's loader swallows it; jsPDF 2.5.2 is not on cdnjs, use jsDelivr"
metadata:
  node_type: memory
  type: project
  originSessionId: 5bcc5440-ef8d-419f-bb0a-f08468122ed7
  modified: 2026-10-20T04:45:10.265Z
---

On any page that loads a UMD library (Plotly.js, AG Grid, jsPDF) together with the ArcGIS Maps SDK for JavaScript (the standard TRPA dashboard stack), the library's `<script>` must come **before** the `js.arcgis.com` script tag.

UMD bundles check for an AMD loader. If Dojo's loader already exists, the bundle registers an anonymous `define()` instead of setting its global. Plotly then corrupts the loader (a `multipleDefine` error on `esri/Map`; `require([...])` callbacks silently never fire, so the map never initializes while the rest of the page renders normally). jsPDF and AG Grid simply never appear on `window`.

**Why it is hard to spot:** the page looks half-working (panels, legends, and Calcite components all render), and the console error names `esri/Map`, not Plotly. Requiring the same modules later from the console succeeds, which makes it look like a timing problem rather than a load-order one.

**How to apply:** put every UMD script first in `<head>`, above the ArcGIS SDK. Diagnosed while building the smoke map (now qa/monitoring/smoke-map.html); applies to any page pairing `trpa-dashboard-stack` charts, grids, or PDF export with a map.

**CDN gotcha (Oct. 2026):** `cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.2/jspdf.umd.min.js` is a 404 (cdnjs stops at 2.5.1). Load jsPDF from `cdn.jsdelivr.net/npm/jspdf@2.5.2/dist/jspdf.umd.min.js`, same CDN as AG Grid (qa/permitting/public-notice.html does). Related: [[design-system-tokens]].
