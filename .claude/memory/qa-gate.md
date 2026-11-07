---
name: qa-gate
description: "Every page under qa/ loads assets/qa-gate.js first in <head>: a client-side password gate that compares the salted SHA-256 of the entry with a constant and remembers the unlock in localStorage for 30 days; change the password with scripts/qa_gate_hash.py"
metadata:
  type: project
---

Since Nov. 6, 2026 every HTML page under `qa/` (33 pages as of Nov. 6, 2026, including `qa/_template/index.html` so stamped betas inherit it) loads `assets/qa-gate.js` as the first script in `<head>`, right after the viewport meta. The script hides the page (`visibility: hidden` on body children, so maps and charts keep their layout) behind a TRPA-styled password card until the visitor enters the shared QA password. It hashes `SALT + entry` with `crypto.subtle` SHA-256 and compares it to `HASH` in the script. A match is stored in localStorage under `trpa-tools-qa-gate` as `{hash, until}` with a 30-day expiry; because the stored record carries the hash, changing `HASH` relocks everyone. `window.qaGate.lock()` clears the unlock and reloads.

Change the password: `python scripts/qa_gate_hash.py "new password"` prints the hash to paste into `HASH`. `SALT` (`tools.trpa.gov/qa`) must match in both files. The password itself is shared with staff out of band and never written in the repo or these notes.

**Why:** staff and partners kept landing on half-built betas from the "Apps in development" link; the gate makes `qa/` an opt-in space without any server. It is obscurity, not security: the repo is public, the pages and their data still ship to the browser, and `crypto.subtle` needs https or localhost (file:// shows a message instead of the form).

**How to apply:** new qa pages get the same script tag first in `<head>` with the right `../` depth (the template already has it; a page with a minified head, such as a Claude artifact export, takes it right after `<head>`). The gate sets explicit backgrounds and `color-scheme: light` on its own controls so dark-themed host pages cannot restyle them. Never put content that must stay private under `qa/` on the strength of the gate. Production pages at the top level stay ungated. The card has a "Request the password" mailto button to the GIS team inbox (REQUEST_MAILTO in the script). Related: [[trpa-tools-site]], [[department-pods]].
