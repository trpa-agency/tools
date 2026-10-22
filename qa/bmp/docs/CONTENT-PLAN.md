# Content plan: the staff review reconciled with the rebuilt site

Sources: the Stormwater program's page-by-page review of tahoebmp.org (a keep-or-delete spreadsheet and an annotated page map, April 16, 2026) and the program's follow-up on fillable PDFs (Oct. 20, 2026). Both were written for a migration into trpa.gov; this plan maps every decision onto the rebuilt site at `qa/bmp/`, which is the proposed home at `tools.trpa.gov/bmp/` with `bmp.trpa.gov` redirecting to it.

Three things to settle with the program and Communications are at the end (section 6). Everything else can be applied.

## 1. Page by page

### Pages staff want gone

| Legacy page | Staff decision | In the rebuilt site | Action |
|---|---|---|---|
| BMPComments.aspx | Delete, broken | Not built | Nothing. |
| BMPProfessionals.aspx | Delete, but its resources go front and center (calc sheet instructions, winterization, link to standardized BMP requirements) | Not built; calc sheet and winterization are in Resources | Winterization: link the Oct. 2026 trpa.gov guidelines instead of the 2009 PDF. Put the calc sheet and its instructions under a new Installation group. |
| Contact.aspx | Delete, hotline is on trpa.gov and everywhere else | Built as `contact.html` | Remove the page; the hotline and email are already in every footer and on the home page. |
| Fertilizer subpages (Intro, Phosphorus, Resources, Science) | Delete; keep at most one rewritten fertilizer page with no borrowed photos | Already one page, `fertilizer.html`, no photos | Rewrite from the draft in the review packet (section 3 below) and add the SEZ fertilizer language from the Code. |
| LivingWithFire.aspx | Delete | Not built | Nothing. Defensible space stays as a paragraph on About BMPs. |
| MultiFamily.aspx, Residential.aspx, WhoAreYou.aspx | Delete, fold property types into one place | Not built; the home page has four audience cards | Keep the cards. |
| News.aspx, Reporting.aspx | Delete | Not built | Nothing. Reporting (whole-basin export) is covered by the map tool's CSV export and the search's CSV. |
| Realtors.aspx | Delete, but keep the disclosure form and description on the requirements page; drop the wood heater section; find a usable image | Built as `realtors.html` | Fold into Get a Certificate as a "Buying or selling a property" section (disclosure requirement, the 30-day rule, the fillable form). Remove the page and the wood heater link. |

### Pages staff want kept, with edits

| Legacy page | Staff decision | In the rebuilt site | Action |
|---|---|---|---|
| BMPHandbook.aspx | Keep. Label Chapter 4 as "BMP Toolkit (BMP Drawings)". Start the description at "Provides technical...". The complete handbook needs the recent updates. | `handbook.html` | Relabel the chapter and toolkit heading. Trim the intro. The handbook PDFs themselves are the program's to update: bare soil protection, lava rock and recycled tires not acceptable, 7 to 10 cubic yards, drop home landscaping guide references, Chapter 5 wildfire defense into the complete PDF. |
| BMPHandbookCh4.aspx | Keep, make sure every link works | Toolkit section of `handbook.html`, 127 links verified Oct. 20 | Nothing until revised drawings arrive. |
| BMPProblem.aspx | Keep, retitle: BMPs are the solution, not the problem | Section "What is the problem?" on `about-bmps.html` | Retitle the section "Why install BMPs?" |
| BMPResources.aspx | Keep, reorganize (installation, training, maintenance). Remove brochures, fire resources, fire districts, home landscaping guide, the old cost documentation PDF. Forms exist on trpa.gov. Move the Tahoe Keys idea book out of brochures. Spanish NRCS drawings are out of date. Check the contractors manual. Rename "2021 BMP Workshop" to "BMP Installation Training". | `resources.html`, driven by `data/documents.json` | Regroup the registry: Installation (NRCS drawings, toolkit drawings link, calc sheet and instructions, materials list, service providers, contractors manual), Training (installation training video, Q and A, info sheets), Maintenance (logs, checklists, videos), Policy (action plan, Code, Compact, 208 plan). Remove the brochures, fire, fire districts, and cost documentation items. Point forms at trpa.gov Applications and Forms. Spanish drawings and the idea book: see section 6. |
| BMPs.aspx (certificates) | Keep. 7 to 10 cubic yards. Add "contact the BMP team to determine if a property is site constrained." | `get-certified.html`, already says 10 | Add the site-constraint line to the Source Control callout. |
| The eight conceptual drawings (CommBadEx, CommGoodEx, MarinaEx, MultiFamilyEx, RegionalEx, SingleFamEx, TempEx, WinterEx) | Keep and embed, dropdown style. Single-family drawing: fix the pink dripline shading and the infiltration trench placement, which confuses people. | Grid of eight on `about-bmps.html` | Keep the grid (a Calcite accordion is a one-line change if dropdowns are wanted). The single-family drawing needs a redraw; until then add a caption note or drop it. |
| Default.aspx (home) | Keep for now. Quick links must survive: disclosure form, wood heater form, retrofit application, small plan, NRCS drawings, toolkit drawings, calc sheet, mapping tool, certificates, parcel tracker. | `index.html` | Add NRCS drawings and toolkit drawings to Most requested. Rename the parcel tracker link "Find out if a property has a BMP Certificate". Wood heater form lives on trpa.gov Applications and Forms; link it from there, not here. |
| FAQs.aspx | Keep, rewrite with the questions people actually ask, and link it where it will be seen | Not built | Build `faq.html` from the legacy questions, rewritten (section 4), and link it from the nav and home. |
| Fertilizer.aspx | Keep or consolidate | `fertilizer.html` | Rewrite per the draft. |
| Maintenance.aspx | Keep. Add the maintenance steps from the most recent maintenance letter, required documents, how to get help, how to submit. Keep every link. Fix the maintenance log that will not open. | `maintenance.html` | Add a "How to document maintenance" section once the letter text arrives (section 6). The log problem is a file problem, not a link problem (section 2). |
| PrescribedBMPs.aspx | Keep, move to gallery or resources; permanent versus temporary | "BMPs most often prescribed for homes" on `about-bmps.html` | Keep where it is and add a permanent-versus-temporary note; link it from the gallery. |
| SmallBMPRetro.aspx | Keep, very important. Call out that BMPR, BMPP, and BMPM are free. Link the trpa.gov Applications and Forms page. A similar explainer for the BMP Retrofit Permit would help. | `small-retrofit-plan.html` | Add the "free" callout. Add a short "BMP Retrofit Permit" section with the 2024 packet from trpa.gov (the tahoebmp.org copy is the 2021 version; see section 2). |
| WhatAreBMPs.aspx | Keep and expand into the requirements: required by Code, commercial versus residential versus maintenance, source control, defensible space, infiltration of the 20-year one-hour storm, calc sheet, pretreatment, site constrained, treat and release, area-wide projects with story maps, lakefront, fertilizer, temporary BMPs and winterization | `about-bmps.html` | Turn About BMPs into "BMP requirements": a requirements list in that order, each item two or three sentences with a link to the toolkit sheet, plus the rock types and sizes table moved here from the gallery. |
| Photo galleries (seven pages) | Keep. Check that every photo is TRPA's. Give the border photos unique names. Add a vactor truck photo to maintenance. Rock sizes could move to requirements. | `gallery.html` with 77 photos from the legacy site | Unique border captions. Move the rock table to requirements. Photo ownership and the vactor truck photo are the program's. |

### New in the rebuilt site, not in the legacy plan

- `search.html` replaces the BMP Database search with one box over the parcel database and the BMP database. Staff suggested sending the public to the Parcel Tracker instead; the new search already links each parcel to the tracker for the certificate, so keeping it costs nothing and realtors get owner and certificate lookups back.
- `map.html` replaces the gis.trpa.org mapping tool, which staff want to keep linking.

## 2. The fillable PDFs

The program reported that the Inspection and Maintenance Log errors in the browser, that the BMP Retrofit Application on tahoebmp.org differs from the one on trpa.gov, and that nobody knows why some fillable PDFs work and others do not. The files explain it:

| File | Made with | Form technology | Behavior in Chrome, Edge, Firefox, and Safari |
|---|---|---|---|
| Maintenance Log, interactive (2016, revised 2020) | Adobe LiveCycle Designer ES 9 | Dynamic XFA (`NeedsRendering`) | Shows the "Please wait... If this message is not eventually replaced..." page. Only Adobe Reader or Acrobat can open it, which is why "save link as" then opening the download works. |
| Maintenance Log, static (2015, revised 2018) | LiveCycle Designer | Dynamic XFA | Same. |
| Real Estate Disclosure Form, interactive (2015) | LiveCycle Designer | Dynamic XFA | Same. The static copy that trpa.gov links is the one that works. |
| Small BMP Treatments Form (2016) | LiveCycle Designer | Static XFA with a standard AcroForm fallback, 80 fields | Works everywhere, because browsers ignore the XFA part and use the fallback. |
| BMP Retrofit Application on tahoebmp.org (Feb. 2021, built in Word 2007 and Distiller) | Acrobat | AcroForm, 88 fields | Works. Out of date. |
| BMP Retrofit Packet on trpa.gov (April 2024) | Acrobat 24 | AcroForm, 72 fields, Adobe Sign enabled | Works. This is the current application. |

So the rule is simple: **LiveCycle (XFA) forms do not work in browsers; Acrobat (AcroForm) forms do.** Browsers dropped XFA years ago and Adobe discontinued LiveCycle; the person who built these forms has left, and nobody should build new ones that way.

What to do:

1. **Link the trpa.gov 2024 Retrofit Packet** everywhere and stop serving the 2021 application. One line in `data/documents.json` and the two page links.
2. **Rebuild the Inspection and Maintenance Log as an AcroForm.** Two ways. In Acrobat Pro: open the static log, print to PDF to flatten it, then use Prepare Form to add the fields; thirty minutes, and it matches how TRPA's other forms are made. Or with code: a small script in this repo (reportlab draws the log table, pypdf adds the fields) regenerates the PDF whenever the content changes, so the form is versioned with the site and never depends on who built it. Either produces a file that opens in every browser and prints cleanly.
3. **Rebuild the interactive disclosure form the same way**, or keep linking only the static one as trpa.gov does.
4. **Submissions are a different question from forms.** The program wants people to submit maintenance documentation: photos, invoices, logs. Microsoft Forms cannot take file uploads from anyone outside the TRPA tenant, so property owners and contractors could not attach anything, and the results would sit in a SharePoint list away from the parcel record. Two tools TRPA already runs fit better: Survey123 (public form, photo attachments, APN lookup, results land in the GIS where the BMP Database lives) and Accela Citizen Access (where Small BMP Retrofit Plans are already submitted). Recommendation: a Survey123 form for maintenance documentation and evaluation requests, linked from the Maintenance page and the search's "Request an evaluation" button, with the AcroForm log kept for people who want a paper record.

## 3. Fertilizer page

The review packet includes a draft that combines the five legacy fertilizer pages: why nutrients matter at Tahoe (ultra-oligotrophic lake, phosphorus and nitrogen feed algae, the TMDL), choosing zero-phosphorus and slow-release products, timing (May and September, no rain in the forecast), amounts (one-half to three-quarters of a pound of nitrogen per 1,000 square feet per year), watering in cycles, soil testing, native plants, and keeping fertilizer away from streams and shorelines. The rebuilt page already carries the tips; it should take the draft's structure (why, how, why it matters), add the Code language on fertilizer in stream environment zones, and link Chapter 5 of the handbook. No photos.

## 4. FAQ page

Legacy questions, with what the answers should say now:

| Question | Answer now |
|---|---|
| How do I get a BMP Certificate? | Link Get a Certificate (three steps). |
| How do I get a copy of my certificate, or check a property's status? | Property search, then "Print certificate on LT Info". |
| What are BMPs? | Link requirements. |
| Are BMPs required at the point of sale? | Disclosure is required, not installation; the buyer files the form within 30 days. Link the form. |
| What happens if I do not do my BMPs? | Targeted enforcement by land use, pollutant load, proximity to the lake or SEZ, complaints, and public projects; a Notice of Failure to Implement by certified mail names the specialist to call. |
| I cannot afford BMPs. | Phase the work; many BMPs are do-it-yourself; call the hotline for the least-cost options and a schedule. The plan, permit, and inspection are free. |
| Is there a deadline? | Every deadline has passed (the last priority watershed deadline was Oct. 15, 2008); every property without BMPs is out of compliance. |
| Who can install BMPs? | The owner, or a contractor; link the service providers list and the installation videos. |
| How do BMPs work with defensible space? | Five-foot noncombustible zone, rock not mulch next to structures; link Tahoe Living with Fire. |
| Do I really have to pave my driveway? | Compacted dirt driven on in winter is a top sediment source; pave and capture, or restore and block off. |
| New: What is a site constraint, and how do I know if my property has one? | Groundwater, bedrock, slow soils, utilities; contact the BMP team to find out. |
| New: My certificate is years old. Is it still good? | Yes while the BMPs are maintained; commercial and multi-family owners submit documentation to have it reissued. |

The program should confirm these and add the questions the hotline hears most.

## 5. Who edits what

Communications asked for a site they can manage. The rebuilt site splits into two kinds of content:

- **Lists** (every document, the handbook, the gallery) live in three JSON files. Adding a PDF is one entry with a title, a link, and a type. This is already easier than the old ASP.NET pages.
- **Prose** lives in the HTML pages. Editing a paragraph means editing HTML in GitHub's web editor, which works but is not comfortable for a non-developer.

Options, cheapest first:

1. **GIS maintains the site; Communications and the program send edits.** Zero setup. Fine while edits are occasional.
2. **A Git-backed editor over this repo.** Pages CMS or Decap CMS put a form-style editor in front of the HTML and JSON files, with GitHub login and a commit per save. One afternoon to configure; Communications edits text and lists in a browser without seeing code. No server, nothing to host.
3. **Prose on trpa.gov, tools here.** Communications owns the words in WordPress; the search, map, handbook, resources, and gallery stay at tools.trpa.gov/bmp and the WordPress pages link to them. This is the April plan in a smaller form, and it is what "too massive to integrate" argues against.

Recommendation: 1 now, trial 2 before the site leaves qa.

## 6. Decisions needed

1. **Spanish NRCS drawings and the Tahoe Keys idea book:** update, move, or remove. The site keeps both until told.
2. **Maintenance steps:** the text of the most recent maintenance letter, so the Maintenance page can state what to do, what to submit, and how.
3. **Submissions:** Survey123 (recommended), Accela, or Microsoft Forms for maintenance documentation and evaluation requests.
4. **Photos:** the program's check that every gallery photo is TRPA's, plus a vactor truck photo for maintenance and a replacement single-family drawing.

## 7. Change list, applied Oct. 21, 2026

Done without new information: Contact and Realtors pages removed (the disclosure requirement is now the last section of Get a Certificate); "Why install BMPs?" retitled; toolkit relabeled "Chapter 4: BMP Toolkit (BMP Drawings)"; Resources regrouped into Installation, NRCS drawings, Training, Maintenance, Forms, Landscaping and fertilizer, and Policy, with the brochures, fire links, fire districts, cost documentation sheet, interactive (XFA) log and disclosure forms, and 2021 retrofit application dropped; winterization and the retrofit application point at the trpa.gov versions; the residential BMP guidelines, the sample BMP and grading plan, and the 208 Plan added; site-constraint line added; "all three are free" callout and a BMP Retrofit Permit section added; home page Most requested carries the staff quick-link list and the parcel tracker link reads "Find out if a property has a BMP Certificate"; FAQ page built from section 4 and added to the nav; fertilizer page rewritten from the draft; About BMPs is now BMP Requirements with the requirements list and the rock table; border photos captioned Border 1 to Border 9.

Still open: the four decisions in section 6, the handbook PDF updates, the fertilizer Code section citation (the page says fertilizer is restricted in stream environment zones under Chapter 60; the program should confirm the section), and a replacement single-family drawing.
