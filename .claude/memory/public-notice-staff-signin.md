---
name: public-notice-staff-signin
description: "qa/permitting/public-notice.html staff mode: SDK IdentityManager sign-in dialog (TRPA Portal username and password, no OAuth app), then queries go to the secured Parcel_Master layer (OWN_FULL) with the token"
metadata:
  type: project
---

Added Nov. 23, 2026. The Public Notice List has a "Staff sign in" header button. It calls `IdentityManager.getCredential` on `Parcel_Master/FeatureServer/0` (secured, 499 anonymously), which shows the SDK sign-in dialog; the Portal at maps.trpa.org/portal issues the token (maps.trpa.org/server is federated with it). While signed in, parcel queries use Parcel_Master with `token=` (SDK first, JSONP with the token as the fallback), and `OWN_FULL` feeds an Owner grid column, an "Owner name (staff)" label line, and an Owner Name CSV column. With names on, the label dedupe key includes the owner. The token sits in sessionStorage for the tab and is dropped at expiry (8 hours requested) or sign-out. A "Start over" button resets subjects, list, settings, and the share hash in place, keeping the sign-in.

**Why:** owner names are not in the public Parcels layer. A passphrase hash like the QA gate cannot protect them (public repo, data ships to the browser), so staff authenticate with their own Portal account and the server enforces access. TRPA has no OAuth app registered (Nov. 2026), so the username and password dialog is the method.

**How to apply:** the dialog's generateToken call is a browser fetch, so it is exposed to the office-network CORS problem; if staff in the office can't sign in, that is the cause, and registering a Portal OAuth app (popup sign-in, no fetch) is the workaround. Parcel_Master is assumed to share the public layer's field names; missing ones are logged to the console and skipped. Related: [[internal-cors-issue]], [[qa-gate]].
