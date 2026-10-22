# Next steps by role

The prototype phase closed Oct. 21, 2026. The latest build is at https://trpa-agency.github.io/tools/qa/bmp/ (beta, under `qa/`). The next phase is the integration of the site with the BMP Database on the agency SQL Server, done by the GIS Manager, who built and maintains that database and the BMP Toolkit, working with Claude. The plan is in `FORMS.md` under "Integration with the BMP Database". Communications owns the site content and signs off on how the public pieces behave. Deployment detail is in `DEPLOY.md`, content decisions in `CONTENT-PLAN.md`.

## What is new in the latest build

Everything from the April page review is applied. Links are pages under the build address above.

- Home page: the three-step path to a certificate, audience cards, and program counts read live from the BMP Database.
- `about-bmps.html`, now titled BMP Requirements: why, what, the requirements list, rock sizes, the eight interactive site designs (hover or tap a shaded area for the BMP and its fact sheet, as on the old site), and the commonly prescribed BMPs.
- `get-certified.html` with the point-of-sale disclosure section (the Realtors page folded in), and `small-retrofit-plan.html` with the BMP Retrofit Permit section and the free plan review called out.
- `maintenance.html` with the documentation section and submit buttons; they open an email until the web forms are live.
- `resources.html` regrouped into installation, NRCS drawings, training, maintenance, forms, landscaping, and policy.
- `faq.html` (12 questions) and `fertilizer.html` rewritten from the staff draft.
- `search.html`: one box over the parcel database and the BMP Database (parcel number, address, owner, or certificate number) with a detail panel and Parcel Tracker links.
- `map.html`: the BMP Mapping Tool rebuilt inside the site.
- Three fillable PDFs that open in any browser: `forms/bmp-maintenance-log.pdf`, `forms/bmp-real-estate-disclosure.pdf`, and `forms/small-bmp-treatments-form.pdf`. The LiveCycle versions are retired.
- The handbook, gallery (77 photos), and document lists carried over; Contact and Realtors pages removed; hotline and email on every page.
- Built but not yet live: the two Survey123 web forms, BMP Maintenance Documentation and Request a BMP Evaluation. They go live in the integration phase, when submissions have a place to land in the BMP Database.

## Communications (site owner)

- Review the latest build page by page against the list above and send corrections. Content is the one thing the integration phase does not touch.
- Close the content decisions in `CONTENT-PLAN.md` section 6: Spanish NRCS drawings and the idea book, the maintenance letter text, gallery photo credits, and the single-family drawing.
- Confirm the hotline number, the program email, and the 2024 Retrofit Permit packet link on trpa.gov.
- Open the three PDF forms in a browser and send wording or field changes; they regenerate from a script.
- Review the two web forms question by question (a preview can be shared) and name who in the program receives and reviews submissions. That answer shapes the integration.
- Decide the fate of the old server's documents: 488 MB of PDFs and DWGs, with the 282 MB workshop video going to a video host either way.
- The home address will be bmp.trpa.gov, served from a repository of its own after the integration phase (decided Oct. 22, 2026). Until then the beta address above is the one to share internally.
- What to expect during the integration phase: the public pages stay as they are, except the search detail gains the property summary fields and the submit buttons switch from email to the web forms. The old site stays up until cutover.
- Schedule the content-model walkthrough: pages are plain HTML, document lists and the handbook and gallery are JSON files, changes go through the GitHub repo.

## GIS Manager with Claude: the integration phase

The five steps are spelled out in `FORMS.md`. In short:

1. **Discovery, read-only.** Run `scripts/dump_bmp_schema.py` against the BMP Database and share the output; together, write the data dictionary and settle the tables, the document file store, the view behind `BMP_Status`, the flag rules, and which fields are public.
2. **Reads.** Publish a public-safe view of the BMP Database joined to parcels on maps.trpa.org; the search and map switch to it and the detail panel gains the summary fields.
3. **Writes.** Publish the two Survey123 forms as hosted layers in the portal and write the scheduled job that carries submissions and photos into the BMP Database tables and the document store, with the field mapping in a config file.
4. **Staff workflow.** The tracking tool keeps running for data entry and review; submissions arrive in its tables with an email.
5. **Cutover.** Redirects, documents, DNS with DTS, public pages retire, staff pages stay.

Standing items for the GIS Manager alongside the steps:

- Decide the owner name policy. The toolkit hides owner names from the public; the public `BMP_Status` service exposes `OwnerName`, `OWN_FULL`, and the mailing address fields, and the new search shows the owner name. If that should stay private, it comes out of the service in Step 2.
- Confirm the Parcel Tracker certificate print covers source control certificates, and decide whether an evaluation print is needed.
- Rotate the Nearmap API key that sits in the public "BMP Web Map" item on ArcGIS Online, and take it out of the item.
- Decide the long-term home of the tracking tool's data entry (keep it, Pro, or a staff Survey123 form). Not blocking.
