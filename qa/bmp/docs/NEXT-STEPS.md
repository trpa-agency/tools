# Next steps by role

What it takes to turn `qa/bmp` into the live BMP site. Written Oct. 21, 2026. Communications owns the site and its content; the GIS Manager owns the BMP Database and the services behind the search. Deployment detail is in `DEPLOY.md`, content decisions in `CONTENT-PLAN.md`, forms in `FORMS.md`.

## Communications (site owner)

- Click through the rebuilt site at the QA address page by page and confirm the April page review was applied the way the program meant it: Contact and Realtors removed, the disclosure folded into Get a Certificate, BMP Requirements expanded, Resources regrouped, the FAQ and fertilizer pages.
- Close the open content decisions in `CONTENT-PLAN.md` section 6: Spanish NRCS drawings and idea book, the maintenance letter text, photo ownership and credits for the gallery, and the single-family drawing.
- Confirm the hotline number and program email on every page, and the 2024 Retrofit Permit packet link on trpa.gov.
- Open the three rebuilt PDF forms in a browser (maintenance log, real estate disclosure, small BMP treatments) and check wording and fields. Say what to change; they regenerate from a script, so edits are a rerun, not a redesign.
- Review the two Survey123 web forms (maintenance documentation and evaluation request) question by question in Connect before they are published, and decide who receives and reviews submissions.
- Decide what happens to the old server's documents: 488 MB of PDFs and DWGs that the new site still links on tahoebmp.org. They either move into the repo (minus the 282 MB workshop video, which goes to a video host) or stay until the old site is retired.
- Approve the home address: tools.trpa.gov/bmp, with bmp.trpa.gov redirecting to it. The redirect table for old links is in `DEPLOY.md`.
- Learn the content model so the site can be managed without a developer: pages are plain HTML, document lists and the handbook and gallery are JSON files, and changes go through the GitHub repo. A short walkthrough is the ask.

## GIS Manager (BMP Database owner)

- Document where the BMP Database lives (server, instance, database), which tables hold certificates, evaluations, disclosures, flags, and maintenance documents, where the document files are stored, and how the `BMP_Status` map service view joins it to parcels. The new site reads layer 5 of that service.
- Choose where web form submissions land. `FORMS.md` lays out three paths: a hosted layer with a sync, feature services published from the collection geodatabase (the working plan), or an integration with the BMP Database tables the old toolkit writes to. Nothing has been created in any geodatabase yet.
- If the collection path stands: create the two feature classes and two related tables described in `FORMS.md` (GlobalIDs, attachments, editor tracking, relationship classes), publish them as Create-only feature services on the federated server, share them with Everyone, and send the service URLs so the XLSForms get their `submission_url`.
- Decide what replaces the agent login and tracking tool when tahoebmp.org retires. The static site has no staff data entry; the options are editing the BMP tables in Pro, a staff Survey123 form, or keeping the tracking tool running internally.
- Extend the `BMP_Status` service, or publish a view, with the property summary fields the old toolkit showed and the new search cannot: priority watershed, soil type and KSAT, land capability, SEZ or shorezone, implementation required by, certificate updated date, disclosure received and date, enforcement action, maintenance requested, evaluation agency and date, and maintenance documents on file.
- Decide the owner name policy. The old toolkit showed owner names only after login; the public `BMP_Status` service already exposes `OwnerName`, `OWN_FULL`, and the mailing address fields, and the new search shows the owner name. If that should stay private, it comes out of the service, not just the page.
- Confirm certificate printing: the new site sends people to the LT Info parcel page for a certificate instead of `printCertificate.asp`. Confirm that covers the source control certificate, and decide whether the evaluation print needs an equivalent.
- Rotate the Nearmap API key that sits in the public "BMP Web Map" item on ArcGIS Online, and take it out of the item.
- Plan the retirement of the old web server with DTS: DNS for bmp.trpa.gov, the redirects, and the document files.
