---
name: locator-basin-export
description: "Locator exports: the offscreen basin view draws only client-side layers (lake embedded, boundaries pulled once, mask cut locally from the TRPA boundary) because per-tile service queries outran the 8 s settle cap and shipped white rectangles"
metadata:
  type: project
---

The Project Locator (qa/general/locator.html) renders its basin inset on an offscreen MapView. Since Oct. 20, 2026 every layer on that view is client-side: the lake from the embedded LAKE_RINGS, the state line (Boundaries/MapServer/16), City of South Lake Tahoe (MapServer/2), and TRPA boundary (MapServer/4) each pulled once with basinClientLayer (SDK queryFeatures, JSONP fallback), and the navy outside mask cut with geometryEngine as a wide rectangle minus the boundary. Boundaries/MapServer/15 (states cutout) is no longer used.

**Why:** Service FeatureLayers fetch one query per 512 px tile at draw time. At export size (1700 by 2014 px) that is 16 or more round trips to maps.trpa.org, and when the server was answering in about 3 s per query (Oct. 20, 2026) the draw took 27 s, the export's 8 s settle cap expired, and the Basin Only export shipped with a missing tile as a white rectangle.

**How to apply:** Keep the basin view free of service layers. When testing exports in the Claude desktop browser pane, show the pane: hidden, it pauses requestAnimationFrame and every SDK view sits in `updating` forever, which looks like the same bug but is not. Related: [[internal-cors-issue]].
