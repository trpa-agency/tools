---
name: internal-cors-issue
description: "On the TRPA office network, browser fetch calls from github.io pages to maps.trpa.org fail (CORS headers dropped on the internal route); JSONP via callback= still works and the locator uses it as a fallback"
metadata:
  node_type: memory
  type: project
  originSessionId: 5bcc5440-ef8d-419f-bb0a-f08468122ed7
  modified: 2026-10-20T04:45:04.835Z
---

On the TRPA private office network, fetch-based calls (including the ArcGIS JS SDK's own requests) from pages on trpa-agency.github.io to maps.trpa.org fail on CORS. From outside the office the server echoes any Origin, so this is an internal-route problem (split-horizon DNS bypassing the public proxy that adds the headers). IT has had the ticket since July 2026; as of Oct. 2, 2026 it still reproduced (a staff locator demo: EIP projects, served from GitHub Pages, searched fine while addresses and APNs, served from maps.trpa.org, returned nothing; it looked style-dependent but was not).

**Why:** Any app on the tools site that queries maps.trpa.org will show the same failure for in-office users until IT's fix lands.

**How to apply:** maps.trpa.org ArcGIS REST honors `callback=` (JSONP, content-type application/javascript), which a `<script>` request can use without CORS. The locator (qa/general/locator.html) falls back to JSONP for parcel queries and rebuilds its basin boundary layers client-side from a JSONP pull when the SDK layers fail to load; the same pattern works for other apps. The SDK splits a layer URL into `url` and `layerId`, so rebuild the query URL as `${layer.url}/${layer.layerId}/query`. Related: [[trpa-tools-site]].
