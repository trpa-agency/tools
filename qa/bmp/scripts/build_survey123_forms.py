"""Write the XLSForm workbooks for the two Survey123 forms the BMP program needs.

Survey123 forms are defined in XLSForm spreadsheets (survey, choices, settings sheets).
This script writes them so the form design lives in the repo and can be reviewed and
versioned like everything else. Publishing is manual: open the .xlsx in Survey123
Connect (New survey, File), check the preview, and publish to the TRPA ArcGIS Online
organization as a public survey. docs/FORMS.md has the steps.

  python scripts/build_survey123_forms.py        # writes forms/survey123/*.xlsx

Standard library plus openpyxl (in arcgispro-py3 and most Python installs).
"""

import datetime as dt
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "forms" / "survey123"
VERSION = dt.date.today().strftime("%Y%m%d")

SURVEY_COLUMNS = ["type", "name", "label", "hint", "required", "required_message", "constraint", "constraint_message",
                  "relevant", "appearance", "default", "calculation", "bind::esri:fieldType", "bind::esri:fieldLength",
                  "repeat_count", "body::esri:style"]
CHOICE_COLUMNS = ["list_name", "name", "label"]
SETTINGS_COLUMNS = ["form_title", "form_id", "version", "instance_name", "default_language", "style", "submission_url"]

# Assessor's parcel number formats: 123-456-78 (Washoe, Carson City), 123-456-789 (El Dorado, Placer),
# 1234-56-789-012 (Douglas). Dashes optional on entry; the constraint accepts 8, 9, or 13 digits.
APN_CONSTRAINT = "regex(., '^[0-9]{3}-?[0-9]{3}-?[0-9]{2,3}$') or regex(., '^[0-9]{4}-?[0-9]{2}-?[0-9]{3}-?[0-9]{3}$')"
APN_MESSAGE = "Enter the full parcel number, for example 122-051-02 or 1319-07-002-013."
EMAIL_CONSTRAINT = "regex(., '^[^@ ]+@[^@ ]+\\.[^@ ]+$')"

CHOICES = {
    "yes_no": [("yes", "Yes"), ("no", "No")],
    "property_type": [
        ("single_family", "Single-family home"), ("multi_family", "Multi-family or condominium"),
        ("commercial", "Commercial"), ("tourist", "Tourist accommodation"), ("public", "Public or institutional"),
        ("other", "Other"),
    ],
    "contact_role": [
        ("owner", "Property owner"), ("manager", "Property manager or HOA"), ("agent", "Agent or representative"),
        ("contractor", "Contractor"), ("other", "Other"),
    ],
    "performed_by": [("owner", "Owner or occupant"), ("contractor", "Contractor"), ("management", "Property management or HOA")],
    "bmp_types": [
        ("sediment_trap", "Sediment trap cleaned"), ("infiltration", "Infiltration trench, basin, or drywell cleaned or rock replaced"),
        ("dripline", "Roof dripline trench or armor cleaned"), ("slotted_drain", "Slotted channel drain cleaned"),
        ("swale", "Swale or drainage channel cleared"), ("pervious", "Pervious pavement swept or vacuumed"),
        ("barriers", "Parking barriers repaired or replaced"), ("revegetation", "Bare soil revegetated or mulched"),
        ("slope", "Slope stabilization repaired"), ("snow", "Snow storage area cleaned of sediment"),
        ("treatment", "Treatment vault, baffle, or filter serviced"), ("other", "Other (describe below)"),
    ],
    "eval_reason": [
        ("new_owner", "I am a new owner and want to know what is required"), ("planning", "I am planning BMPs and want a site evaluation"),
        ("constraint", "I think the property may be site constrained"), ("sale", "A sale is pending and I need the BMP status"),
        ("notice", "I received a notice from TRPA"), ("reissue", "I need a certificate reissued after maintenance"),
        ("other", "Other"),
    ],
    "contact_pref": [("email", "Email"), ("phone", "Phone"), ("either", "Either")],
}


def row(type_, name, label, **kw):
    r = {c: "" for c in SURVEY_COLUMNS}
    r.update({"type": type_, "name": name, "label": label})
    r.update(kw)
    return r


def common_contact(prefix=""):
    return [
        row("begin group", "contact", "Who is submitting this", appearance="field-list"),
        row("text", "contact_name", "Your name", required="yes", **{"bind::esri:fieldLength": "120"}),
        row("select_one contact_role", "contact_role", "Your role", required="yes"),
        row("text", "contact_email", "Email", hint="We will reply to this address.", required="yes",
            constraint=EMAIL_CONSTRAINT, constraint_message="Enter a valid email address.", **{"bind::esri:fieldLength": "160"}),
        row("text", "contact_phone", "Phone", appearance="numbers", **{"bind::esri:fieldLength": "40"}),
        row("end group", "", ""),
    ]


def property_group():
    return [
        row("begin group", "property", "The property", appearance="field-list"),
        row("text", "apn", "Assessor's parcel number (APN)", hint="On the tax bill, or look it up with the Property BMP Status Search.",
            required="yes", constraint=APN_CONSTRAINT, constraint_message=APN_MESSAGE, **{"bind::esri:fieldLength": "20"}),
        row("text", "address", "Property address", required="yes", **{"bind::esri:fieldLength": "200"}),
        row("select_one property_type", "property_type", "Property type", required="yes"),
        row("geopoint", "location", "Property location (optional)", hint="Tap to place the point on the property if you are on site."),
        row("end group", "", ""),
    ]


MAINTENANCE_SURVEY = [
    row("note", "intro", "BMP Maintenance Documentation",
        hint="Use this form to document BMP maintenance so TRPA can reissue a BMP Certificate with a new date. Commercial and multi-family properties submit documentation after each maintenance season. Attach photos, invoices, or a maintenance log. Questions: BMP Hotline (775) 589-5202 or bmp@trpa.gov."),
    *property_group(),
    *common_contact(),
    row("begin group", "work", "The maintenance", appearance="field-list"),
    row("date", "maintenance_date", "Date maintenance was completed", required="yes"),
    row("select_one performed_by", "performed_by", "Who did the work", required="yes"),
    row("text", "contractor_name", "Contractor or company", relevant="selected(${performed_by}, 'contractor') or selected(${performed_by}, 'management')",
        **{"bind::esri:fieldLength": "120"}),
    row("select_multiple bmp_types", "bmps_maintained", "What was maintained", required="yes", appearance="minimal"),
    row("text", "bmps_other", "Describe the other work", relevant="selected(${bmps_maintained}, 'other')", appearance="multiline"),
    row("text", "work_description", "Describe the work and the condition of the BMPs", hint="For example: cleaned both driveway sediment traps, replaced 2 inches of drain rock in the dripline trench, swept the pervious pavers.",
        required="yes", appearance="multiline", **{"bind::esri:fieldLength": "2000"}),
    row("select_one yes_no", "all_functional", "Are all BMPs on the property working as designed?", required="yes"),
    row("text", "problems", "What is not working, and what is planned", relevant="selected(${all_functional}, 'no')", appearance="multiline", **{"bind::esri:fieldLength": "1000"}),
    row("end group", "", ""),
    row("begin repeat", "photos", "Photos of the maintained BMPs", hint="Add one photo per BMP. Up to 10.", repeat_count="10"),
    row("image", "photo", "Photo", appearance="multiline"),
    row("text", "photo_caption", "What this photo shows", **{"bind::esri:fieldLength": "200"}),
    row("end repeat", "", ""),
    row("begin group", "documents", "Supporting documents", appearance="field-list"),
    row("file", "maintenance_log", "Maintenance log (PDF)", hint="The BMP Inspection and Maintenance Log, if you keep one."),
    row("file", "invoice", "Contractor invoice (PDF or image)", hint="If a contractor did the work."),
    row("end group", "", ""),
    row("acknowledge", "certify", "I certify that the information in this form is accurate and that I am authorized to submit it for this property.", required="yes"),
]

EVALUATION_SURVEY = [
    row("note", "intro", "Request a BMP Evaluation",
        hint="TRPA staff visit the property, identify the BMPs it needs, and send a written evaluation at no cost. Use this form to request one, or to ask about a property's BMP requirements. Questions: BMP Hotline (775) 589-5202 or bmp@trpa.gov."),
    *property_group(),
    *common_contact(),
    row("begin group", "request", "The request", appearance="field-list"),
    row("select_one eval_reason", "reason", "Why are you contacting us?", required="yes"),
    row("text", "reason_other", "Tell us more", relevant="selected(${reason}, 'other') or selected(${reason}, 'notice')", appearance="multiline", **{"bind::esri:fieldLength": "1000"}),
    row("text", "notes", "Anything we should know before the visit", hint="Gates, dogs, parking, best days, or what you have already installed.", appearance="multiline", **{"bind::esri:fieldLength": "1000"}),
    row("select_one contact_pref", "contact_pref", "How should we reach you?", required="yes"),
    row("select_one yes_no", "owner_consent", "Are you the owner, or do you have the owner's permission for a site visit?", required="yes"),
    row("end group", "", ""),
    row("begin repeat", "site_photos", "Photos (optional)", hint="Driveway, roof driplines, bare soil, or anything you have questions about.", repeat_count="6"),
    row("image", "site_photo", "Photo", appearance="multiline"),
    row("end repeat", "", ""),
]

FORMS = [
    {
        "file": "bmp-maintenance-documentation.xlsx",
        "settings": {"form_title": "BMP Maintenance Documentation", "form_id": "bmp_maintenance_documentation", "version": VERSION,
                     "instance_name": "concat('Maintenance ', ${apn}, ' ', ${maintenance_date})", "default_language": "English (en)", "style": "theme-grid"},
        "survey": MAINTENANCE_SURVEY,
    },
    {
        "file": "bmp-evaluation-request.xlsx",
        "settings": {"form_title": "Request a BMP Evaluation", "form_id": "bmp_evaluation_request", "version": VERSION,
                     "instance_name": "concat('Evaluation ', ${apn})", "default_language": "English (en)", "style": "theme-grid"},
        "survey": EVALUATION_SURVEY,
    },
]


def write_sheet(ws, columns, rows):
    ws.append(columns)
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in rows:
        ws.append([r.get(c, "") for c in columns])
    for i, c in enumerate(columns, 1):
        width = max(len(c), *(len(str(r.get(c, ""))) for r in rows)) if rows else len(c)
        ws.column_dimensions[get_column_letter(i)].width = min(max(12, width + 2), 70)
    ws.freeze_panes = "A2"


def build(form):
    wb = Workbook()
    ws = wb.active
    ws.title = "survey"
    write_sheet(ws, SURVEY_COLUMNS, form["survey"])
    used_lists = {r["type"].split(" ", 1)[1] for r in form["survey"] if r["type"].startswith(("select_one ", "select_multiple "))}
    choices = [{"list_name": ln, "name": n, "label": lbl} for ln in CHOICES if ln in used_lists for n, lbl in CHOICES[ln]]
    write_sheet(wb.create_sheet("choices"), CHOICE_COLUMNS, choices)
    write_sheet(wb.create_sheet("settings"), SETTINGS_COLUMNS, [form["settings"]])
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / form["file"]
    wb.save(out)
    return out, len(form["survey"]), len(choices)


def main() -> int:
    for form in FORMS:
        out, n_q, n_c = build(form)
        print(f"wrote {out.relative_to(ROOT)}: {n_q} survey rows, {n_c} choices, version {VERSION}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
