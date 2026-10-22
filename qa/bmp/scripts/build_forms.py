"""Generate the BMP program's fillable PDF forms as standard AcroForms.

The legacy forms were Adobe LiveCycle (XFA) files that browsers cannot display. This
script draws each form with reportlab and adds ordinary AcroForm widgets, so the PDF
opens, fills, and prints in Chrome, Edge, Firefox, Safari, and Acrobat alike.

  "C:\\Program Files\\ArcGIS\\Pro\\bin\\Python\\envs\\arcgispro-py3\\python.exe" scripts/build_forms.py

Outputs:
  forms/bmp-maintenance-log.pdf          BMP Inspection and Maintenance Log (replaces the 2016 XFA log)
  forms/bmp-real-estate-disclosure.pdf   BMP Real Estate Disclosure Form (replaces the 2015 XFA form)
  forms/small-bmp-treatments-form.pdf    Small BMP Treatments Form (replaces the 2016 XFA form)

The content mirrors the legacy forms field for field, with the wording brought up to
date (10 cubic yards, no lava rock or recycled tires, current contacts and links). Edit
the SECTIONS list, NRCS_TREATMENTS, and the text constants to change them; field names
are stable so filled copies stay comparable across versions.
"""

import datetime as dt
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "forms"
VERSION = dt.date.today().strftime("%b. %Y").replace("May.", "May").replace("June.", "June").replace("July.", "July")

NAVY = colors.HexColor("#0B1F41")
BLUE = colors.HexColor("#007DC3")
GREEN = colors.HexColor("#6EBE44")
ORANGE = colors.HexColor("#F16022")
GRAY = colors.HexColor("#5B6677")
LINE = colors.HexColor("#C9D2DE")
WELL = colors.HexColor("#F5F7FA")
FIELD_BG = colors.HexColor("#F0F6FB")

PAGE_W, PAGE_H = letter
MARGIN = 0.5 * inch
CONTENT_W = PAGE_W - 2 * MARGIN

# ── The log's content: (title, chapter reference, note or None, [questions])
SECTIONS = [
    ("Gravel Infiltration System (trench, drywell)", "Chapter 4.1-c", None, [
        "Is stormwater from impervious surfaces conveyed to and captured by the infiltration trench?",
        "Is compaction minimal?",
        "Have invasive weeds been cleared?",
        "Has accumulated sediment from upslope contributing sources been cleared?",
        "Is standing water properly infiltrating or evaporating 96 hours after storm events?",
        "For dripline trenches: is the 5-foot zone next to the structure free of combustible material, per fire defensible space guidelines?",
    ]),
    ("Infiltration Basin", "Chapter 4.1-b", "For vegetated basins, inspect plant health and replace dead plants.", [
        "Is stormwater conveyed to functioning inlets and outlets?",
        "Is erosion or undercutting at the inlets and outlets stabilized, especially along adjacent pavement?",
        "Is the basin clear of trash and debris (inlet, outlet, and within the structure)?",
        "Have invasive weeds been cleared?",
        "Is standing water properly infiltrating or evaporating 96 hours after storm events? If no, the basin may need to be cleaned or rebuilt.",
    ]),
    ("Sediment Trap", "Chapter 4.4-i", None, [
        "Is the sediment trap structurally intact and properly capturing and conveying stormwater?",
        "Is the trap clear of trash and debris (inlet, outlet, and within the structure)?",
        "Is standing water properly infiltrating or evaporating 96 hours after storm events?",
    ]),
    ("Drop Inlet (Drain Inlet)", "Chapter 4.3-e", None, [
        "Is the drop inlet structurally intact and properly capturing and conveying stormwater?",
        "Is the system clear of trash and debris (inlet, outlet, and within the structure)?",
        "Has accumulated sediment from upslope contributing sources been cleared?",
        "Is standing water properly infiltrating or evaporating 96 hours after storm events?",
    ]),
    ("Drop Inlet Insert (Drain Inlet Insert)", "Chapter 4.4-d", None, [
        "Is the insert in place?",
        "Does the insert appear to be functioning properly? Refer to the manufacturer's instructions.",
    ]),
    ("Slotted Channel Drain", "Chapter 4.3-g", "Drains without removable grates may need a vacuum truck to clean.", [
        "Is the drain structurally intact and properly capturing and conveying stormwater?",
        "Is the drain clear of trash and debris (inlet, outlet, and within the structure)?",
        "Has accumulated sediment from upslope contributing sources been cleared?",
        "Is standing water properly infiltrating or evaporating 96 hours after storm events?",
    ]),
    ("Curb and Gutter", "Chapter 4.3-b", None, [
        "Are the curbs and gutters structurally intact and properly conveying stormwater?",
        "Are the curbs and gutters clear of trash and debris?",
    ]),
    ("Asphalt or Concrete Swale", "Chapter 4.3-h", None, [
        "Is the swale structurally intact and properly capturing and conveying stormwater?",
        "Has accumulated sediment from upslope contributing sources been cleared?",
    ]),
    ("Rock-Lined or Vegetated Swale", "Chapter 4.3-j", None, [
        "Is stormwater from impervious surfaces properly reaching and conveyed by the swale?",
        "Is the swale clear of trash and debris?",
        "Has accumulated sediment that would reduce swale capacity been cleared?",
        "Is erosion or undercutting at the inlets and outlets stabilized, especially along adjacent pavement?",
        "Rock-lined: have dislodged or unstable rocks been reoriented?",
        "Vegetated: is adequate vegetation present to prevent erosion?",
        "Vegetated: is the vegetation adequately mowed or pruned?",
    ]),
    ("Vegetation (including under driplines)", "Chapter 4.1-c", "Per fire defensible space guidelines, keep combustible material out of the 5-foot zone next to structures.", [
        "Have eroding areas been stabilized?",
        "Is the area clear of trash, debris, and excess sediment?",
        "Is adequate vegetation present to prevent erosion and support infiltration? Inspect plant health and replace dead plants.",
        "Have invasive weeds been cleared?",
    ]),
    ("Subsurface Infiltration System", "Chapter 4.1-d", None, [
        "Are the system components structurally intact and functioning as designed?",
        "Is the system clear of sediment and debris (inlet, outlet, and within the structure)?",
        "Has the system been serviced (vacuum truck) according to the manufacturer's specifications?",
    ]),
    ("Parking and Vehicle Barriers", "Chapter 4.2-l", "Chapter 60.4 of the TRPA Code of Ordinances requires vehicle access to be limited to paved areas.", [
        "Is vehicle access restricted to paved areas?",
        "Are all barriers structurally intact, and properly spaced and sized to prevent vehicle access?",
        "Have barriers that were moved for site management, such as snow storage, been put back?",
    ]),
    ("Baffled Vault or Hydrodynamic Separator", "Chapter 4.4-f, 4.4-g", None, [
        "Has the system been serviced (vacuum truck) according to the manufacturer's specifications?",
    ]),
    ("Slope Stabilization", "Chapter 4.2-d through 4.2-h", None, [
        "Is loose or bare soil stabilized by an appropriate measure (vegetation, terracing, rock, retaining wall)?",
    ]),
    ("Pervious Pavement or Paver Stones", "Chapter 4.1-a", None, [
        "Is the surface structurally intact and properly capturing and infiltrating stormwater?",
        "Has accumulated sediment been cleared manually or by a contracted service?",
        "If there is an outlet pipe, is it functioning properly?",
        "Are all areas upslope of the surface stabilized?",
    ]),
    ("Snow Storage", "Chapter 4.2-c", "Snow storage areas should never be located in stream environment zones or on top of infiltration BMPs.", [
        "Is the snow storage location sited upslope of capture and conveyance BMPs?",
        "Is the snow storage area sized at roughly 20 percent of the area to be plowed?",
    ]),
    ("Sweeping and Pavement", "Chapter 4.2-b, 4.2-i", "Commercial street sweepers remove fine sediment that hand sweeping leaves behind.", [
        "Is pavement structurally intact and properly conveying stormwater?",
        "Has accumulated sediment been cleared manually or by a contracted service?",
    ]),
    ("Dumpster Management", "Chapter 4.2-m", None, [
        "Are dumpsters located on paved surfaces?",
        "Are dumpsters closed, latched, and secure against wildlife?",
    ]),
    ("Hazardous Material Management", "Chapter 4.2-n", "Proper storage keeps fuels, oils, and chemicals out of stormwater.", [
        "Are storage and containment structures intact, without deteriorating joints or leaks?",
        "Have all spills been contained, cleaned up, and properly disposed of?",
    ]),
    ("Fertilizer Management", "Chapter 5.4.2", "Sites with more than 1 cumulative acre of turf need a fertilizer management plan.", [
        "Have required monitoring reports been submitted to the proper jurisdictions?",
        "Are site management personnel trained on the fertilizer management plan?",
    ]),
]

INTRO = ("BMP inspection and maintenance is necessary to keep BMPs functioning and to keep a BMP Certificate active. "
         "Inspect each BMP on the property after major storms and at least twice a year, in spring after snowmelt and in fall before "
         "Oct. 15. Check the box next to each BMP type present on the property, answer each question, and note the location and any "
         "corrective action. Keep this log on file; commercial and multi-family owners submit it with photos and invoices so TRPA can "
         "reissue the certificate with a new date. Refer to the BMP Handbook for each practice.")

DECLARATION = ("I declare under penalty of perjury that the information in this log is true and correct to the best of my knowledge, "
               "and that I am the owner of the property or authorized to act for the owner.")


class Form:
    """Draws a form across as many pages as it needs, placing AcroForm widgets as it goes."""

    def __init__(self, path: Path, title: str, subject: str, subtitle: str = "TRPA Stormwater Management Program  |  BMP Hotline (775) 589-5202  |  bmp@trpa.gov"):
        self.c = canvas.Canvas(str(path), pagesize=letter)
        self.c.setTitle(title)
        self.c.setAuthor("Tahoe Regional Planning Agency, Stormwater Management Program")
        self.c.setSubject(subject)
        self.title = title
        self.subtitle = subtitle
        self.page = 0
        self.y = 0
        self.form = self.c.acroForm

    # ── page furniture
    def new_page(self):
        if self.page:
            self.footer()
            self.c.showPage()
        self.page += 1
        c = self.c
        c.setFillColor(NAVY)
        c.rect(0, PAGE_H - 0.9 * inch, PAGE_W, 0.9 * inch, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(MARGIN, PAGE_H - 0.5 * inch, self.title)
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.HexColor("#B4CBE8"))
        c.drawString(MARGIN, PAGE_H - 0.68 * inch, self.subtitle)
        # accent stripe in the EIP colors
        y = PAGE_H - 0.9 * inch - 4
        for color, x0, x1 in ((BLUE, 0, 0.6), (GREEN, 0.6, 0.85), (ORANGE, 0.85, 1)):
            c.setFillColor(color)
            c.rect(x0 * PAGE_W, y, (x1 - x0) * PAGE_W, 4, stroke=0, fill=1)
        self.y = PAGE_H - 1.2 * inch

    def footer(self):
        c = self.c
        c.setFont("Helvetica", 7.5)
        c.setFillColor(GRAY)
        c.drawString(MARGIN, 0.35 * inch, f"{self.title}, {VERSION}. Generated from the Lake Tahoe BMPs site; opens in any browser.")
        c.drawRightString(PAGE_W - MARGIN, 0.35 * inch, f"Page {self.page}")

    def need(self, height):
        if self.y - height < 0.6 * inch:
            self.new_page()

    # ── widgets
    def text_field(self, name, x, y, w, h, tooltip="", multiline=False, size=9):
        self.form.textfield(name=name, tooltip=tooltip, x=x, y=y, width=w, height=h, fontName="Helvetica", fontSize=size,
                            borderWidth=0.5, borderColor=LINE, fillColor=FIELD_BG, textColor=NAVY,
                            fieldFlags="multiline" if multiline else "", forceBorder=True)

    def checkbox(self, name, x, y, size=10, tooltip=""):
        self.form.checkbox(name=name, tooltip=tooltip, x=x, y=y, size=size, buttonStyle="check",
                           borderWidth=0.7, borderColor=NAVY, fillColor=colors.white, textColor=NAVY, forceBorder=True)

    def choice(self, name, x, y, w, h, options, tooltip="", editable=False, size=8):
        self.form.choice(name=name, tooltip=tooltip, x=x, y=y, width=w, height=h, options=options, value=options[0],
                         fontName="Helvetica", fontSize=size, borderWidth=0.5, borderColor=LINE, fillColor=FIELD_BG, textColor=NAVY,
                         fieldFlags="combo edit" if editable else "combo", forceBorder=True)

    def labeled_field(self, name, label, x, y, w, h=16, tooltip=None):
        """A small gray label with a text field under it; returns nothing, caller manages y."""
        self.c.setFont("Helvetica", 7.5)
        self.c.setFillColor(GRAY)
        self.c.drawString(x, y - 2, label)
        self.text_field(name, x, y - 4 - h, w, h, tooltip=tooltip or label)

    def check_row(self, label, x, y, items, size=11):
        """'label' then [(name, text), ...] checkboxes laid out left to right on one line."""
        c = self.c
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(NAVY)
        c.drawString(x, y - 9, label)
        cx = x + c.stringWidth(label, "Helvetica-Bold", 8) + 10
        for name, text in items:
            self.checkbox(name, cx, y - 11.5, size=size, tooltip=f"{label} {text}")
            c.setFont("Helvetica", 8.5)
            c.setFillColor(NAVY)
            c.drawString(cx + size + 4, y - 9, text)
            cx += size + 8 + c.stringWidth(text, "Helvetica", 8.5) + 14

    def bullets(self, items, size=8, color=NAVY, width=CONTENT_W - 14):
        for item in items:
            lines = simpleSplit(item, "Helvetica", size, width)
            self.need(len(lines) * (size + 2.5))
            self.c.setFont("Helvetica", size)
            self.c.setFillColor(color)
            self.c.drawString(MARGIN + 4, self.y - size, "•")
            for line in lines:
                self.c.drawString(MARGIN + 14, self.y - size, line)
                self.y -= size + 2.5
            self.y -= 1.5

    def heading(self, text, size=9.5):
        self.need(size + 10)
        self.c.setFont("Helvetica-Bold", size)
        self.c.setFillColor(NAVY)
        self.c.drawString(MARGIN, self.y - size, text)
        self.y -= size + 6

    def rule(self):
        self.c.setStrokeColor(LINE)
        self.c.setLineWidth(0.5)
        self.c.line(MARGIN, self.y, MARGIN + CONTENT_W, self.y)
        self.y -= 8

    # ── content blocks
    def property_block(self):
        c = self.c
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(NAVY)
        c.drawString(MARGIN, self.y, "Property")
        self.y -= 14
        col_w = CONTENT_W / 2
        rows = [("apn", "APN", "name", "Owner or manager name"),
                ("address", "Property address", "contact", "Contact phone and email"),
                ("land_use", "Land use (single-family, multi-family, commercial)", "inspection_date", "Date of this inspection")]
        for left_name, left_label, right_name, right_label in rows:
            for i, (n, label) in enumerate(((left_name, left_label), (right_name, right_label))):
                x = MARGIN + i * col_w
                c.setFont("Helvetica", 7.5)
                c.setFillColor(GRAY)
                c.drawString(x, self.y - 2, label)
                self.text_field(n, x, self.y - 20, col_w - 8, 16, tooltip=label)
            self.y -= 30
        self.y -= 4

    def paragraph(self, text, size=8.5, color=NAVY, bold=False, width=CONTENT_W, leading=None):
        font = "Helvetica-Bold" if bold else "Helvetica"
        lines = simpleSplit(text, font, size, width)
        lead = leading or size + 2.5
        self.need(len(lines) * lead)
        self.c.setFont(font, size)
        self.c.setFillColor(color)
        for line in lines:
            self.c.drawString(MARGIN, self.y - size, line)
            self.y -= lead
        return len(lines)

    def section(self, index, title, ref, note, questions):
        c = self.c
        # measure the whole section so it does not straddle a page unless it has to
        q_heights = [max(18, len(simpleSplit(q, "Helvetica", 8, self.q_w - 6)) * 10 + 7) for q in questions]
        header_h = 18 + (12 if note else 0) + 13
        self.need(min(header_h + sum(q_heights), 4.5 * inch))
        # section header with the "present" checkbox
        c.setFillColor(WELL)
        c.rect(MARGIN, self.y - 18, CONTENT_W, 18, stroke=0, fill=1)
        self.checkbox(f"s{index:02d}_present", MARGIN + 4, self.y - 15, size=11, tooltip=f"This property has: {title}")
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(NAVY)
        c.drawString(MARGIN + 20, self.y - 12.5, f"{index}. {title}")
        c.setFont("Helvetica", 7.5)
        c.setFillColor(GRAY)
        c.drawRightString(MARGIN + CONTENT_W - 4, self.y - 12.5, ref)
        self.y -= 18
        if note:
            c.setFont("Helvetica-Oblique", 7.5)
            c.setFillColor(GRAY)
            c.drawString(MARGIN + 20, self.y - 9, note)
            self.y -= 12
        # column headings
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(GRAY)
        c.drawString(self.x_q + 2, self.y - 9, "INSPECTION QUESTION")
        c.drawCentredString(self.x_yes + 6, self.y - 9, "YES")
        c.drawCentredString(self.x_no + 6, self.y - 9, "NO")
        c.drawString(self.x_loc + 2, self.y - 9, "LOCATION")
        c.drawString(self.x_act + 2, self.y - 9, "DOCUMENTATION / CORRECTIVE ACTION")
        self.y -= 13
        for qi, (q, h) in enumerate(zip(questions, q_heights), 1):
            self.need(h)
            top = self.y
            c.setStrokeColor(LINE)
            c.setLineWidth(0.4)
            c.line(MARGIN, top, MARGIN + CONTENT_W, top)
            c.setFont("Helvetica", 8)
            c.setFillColor(NAVY)
            for li, line in enumerate(simpleSplit(q, "Helvetica", 8, self.q_w - 6)):
                c.drawString(self.x_q + 2, top - 10 - li * 10, line)
            fid = f"s{index:02d}_q{qi}"
            self.checkbox(f"{fid}_yes", self.x_yes, top - 14, size=11, tooltip=f"Yes: {q}")
            self.checkbox(f"{fid}_no", self.x_no, top - 14, size=11, tooltip=f"No: {q}")
            self.text_field(f"{fid}_location", self.x_loc + 1, top - h + 3, self.loc_w - 3, h - 6, tooltip="Location of this BMP on the property", multiline=h > 20, size=8)
            self.text_field(f"{fid}_action", self.x_act + 1, top - h + 3, self.act_w - 3, h - 6, tooltip="Documentation or corrective action", multiline=h > 20, size=8)
            self.y -= h
        c.setStrokeColor(LINE)
        c.line(MARGIN, self.y, MARGIN + CONTENT_W, self.y)
        self.y -= 10

    @property
    def x_q(self): return MARGIN
    @property
    def q_w(self): return 2.55 * inch
    @property
    def x_yes(self): return MARGIN + self.q_w + 4
    @property
    def x_no(self): return self.x_yes + 22
    @property
    def x_loc(self): return self.x_no + 24
    @property
    def loc_w(self): return 1.25 * inch
    @property
    def x_act(self): return self.x_loc + self.loc_w + 4
    @property
    def act_w(self): return MARGIN + CONTENT_W - self.x_act

    def notes_and_signature(self):
        self.need(3.2 * inch)
        c = self.c
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(NAVY)
        c.drawString(MARGIN, self.y - 10, f"{len(SECTIONS) + 1}. Other BMPs and notes")
        c.setFont("Helvetica", 7.5)
        c.setFillColor(GRAY)
        c.drawString(MARGIN, self.y - 21, "Describe erosion, surface runoff, other BMPs on the property, work done by a contractor (attach the invoice), and anything TRPA should know.")
        self.text_field("notes", MARGIN, self.y - 24 - 1.4 * inch, CONTENT_W, 1.4 * inch, tooltip="Other BMPs and notes", multiline=True)
        self.y -= 24 + 1.4 * inch + 14
        self.paragraph("Declaration", size=9, bold=True)
        self.paragraph(DECLARATION, size=8, color=GRAY)
        self.y -= 4
        sig_w = CONTENT_W * 0.62
        c.setFont("Helvetica", 7.5)
        c.setFillColor(GRAY)
        c.drawString(MARGIN, self.y - 2, "Signature (type your name)")
        c.drawString(MARGIN + sig_w + 8, self.y - 2, "Date")
        self.text_field("signature", MARGIN, self.y - 20, sig_w, 16, tooltip="Signature")
        self.text_field("signature_date", MARGIN + sig_w + 8, self.y - 20, CONTENT_W - sig_w - 8, 16, tooltip="Date signed")
        self.y -= 34
        self.paragraph("Submit: email the saved PDF with photos and invoices to bmp@trpa.gov with the APN in the subject line, or use the online "
                       "BMP Maintenance Documentation form linked from the Maintenance page of the Lake Tahoe BMPs site. Keep a copy for your records.",
                       size=8, color=NAVY)

    def save(self):
        self.footer()
        self.c.save()


# ── Real Estate Disclosure Form (mirrors the Feb. 2015 form)
DISCLOSURE_INTRO = ("TRPA requires installation and maintenance of BMPs on all developed properties in the Tahoe Region. BMPs minimize soil "
                    "erosion, maintain fire defensible space, and capture polluted stormwater before it enters Lake Tahoe.")
DISCLOSURE_REQ = ("TRPA Best Management Practices requirements: pursuant to Chapter 60.4 of the TRPA Code of Ordinances, all property owners "
                  "within the Lake Tahoe Region are required to implement and maintain stormwater Best Management Practices (BMPs) and obtain "
                  "a BMP Certificate. Look up a property's certificate number and date of issue on the Lake Tahoe Info Parcel Tracker "
                  "(parcels.laketahoeinfo.org) or the Lake Tahoe BMPs property search.")
DISCLOSURE_NOTES = [
    "Property owners can print a copy of the certificate and the maintenance requirements for their records from the Lake Tahoe Info Parcel Tracker.",
    "Certificates are only valid and transferable as long as BMPs are maintained and remain effective.",
    "Deed holders of properties with shared use areas, including but not limited to shared access, parking, homeowner association common areas, "
    "and easements, may be collectively responsible for BMPs in these areas.",
]
DISCLOSURE_NO_CERT = [
    "All compliance deadlines to install BMPs for developed properties under the jurisdiction of TRPA expired Oct. 15, 2008. Property owners out "
    "of compliance with BMP requirements may be subject to enforcement and fines pursuant to Article 9 of TRPA's Rules of Procedure.",
    "Read the TRPA Permitting Guidelines for Residential BMPs (trpa.gov) for single-family and multi-family properties, or ask the BMP Hotline "
    "for commercial and industrial guidance.",
    "The Small BMP Retrofit Plan, the BMP Retrofit Permit, and the final inspection are free. For more information on installing and maintaining "
    "BMPs, visit the Lake Tahoe BMPs site or call the BMP Hotline at (775) 589-5202.",
    "The ability of TRPA or other agencies to conduct BMP site evaluations and inspections may be weather dependent.",
]
DISCLOSURE_SUBMIT = ("Section 60.4.4.C of the TRPA Code of Ordinances requires the new property deed holder to submit a completed copy of this "
                     "form to TRPA within 30 days of sale. Submit by email to bmp@trpa.gov, by mail to PO Box 5310, Stateline, NV 89449, or in "
                     "person at the TRPA front counter, 128 Market Street, Stateline, NV.")
DISCLOSURE_DECLARATION = ("I hereby declare under penalty of perjury that all information submitted as part of this disclosure is true and accurate "
                          "to the best of my knowledge, and I understand that should any information submitted be inaccurate, erroneous, or "
                          "incomplete, TRPA may take appropriate action.")
DISCLOSURE_FINES = ("Property owners out of compliance with BMP requirements may be subject to enforcement and fines (up to $5,000 per day) "
                    "pursuant to the Bi-State Compact and Article 9 of TRPA's Rules of Procedure.")


def build_disclosure_form(path: Path):
    f = Form(path, "BMP Real Estate Disclosure Form", "Disclosure of a Tahoe Region property's BMP status at sale, required by TRPA Code of Ordinances 60.4.4.C")
    f.new_page()
    c = f.c
    f.paragraph("Tahoe Regional Planning Agency (TRPA) Best Management Practices (BMPs) Disclosure", size=11, bold=True)
    f.paragraph(DISCLOSURE_INTRO, size=8.5)
    f.y -= 2
    f.paragraph(DISCLOSURE_REQ, size=8, color=GRAY)
    f.y -= 6

    f.heading("Property")
    half = CONTENT_W / 2
    f.labeled_field("apn", "Assessor's parcel number (APN)", MARGIN, f.y, half - 8)
    f.labeled_field("county", "County", MARGIN + half, f.y, half)
    f.y -= 30
    f.labeled_field("address", "Physical address", MARGIN, f.y, half - 8)
    f.labeled_field("city", "City", MARGIN + half, f.y, half * 0.5 - 8)
    f.labeled_field("state", "State", MARGIN + half + half * 0.5, f.y, half * 0.2 - 4)
    f.labeled_field("zip", "ZIP code", MARGIN + half + half * 0.7, f.y, half * 0.3)
    f.y -= 32
    f.check_row("Property type (check one):", MARGIN, f.y, [("type_single_family", "Single-family residence"), ("type_multi_family", "Multi-family residence"), ("type_commercial", "Commercial or industrial")])
    f.y -= 22

    f.heading("BMP status")
    f.check_row("Check one:", MARGIN, f.y, [("status_bmp", "BMP Certificate"), ("status_source", "Source Control Certificate"), ("status_none", "No certificate")])
    f.y -= 22
    f.labeled_field("certificate_numbers", "Certificate number(s)", MARGIN, f.y, half - 8)
    f.labeled_field("certificate_date", "Date issued", MARGIN + half, f.y, half * 0.5)
    f.y -= 30
    f.check_row("Is the property included in an area-wide water quality treatment project subject to in-lieu fees?", MARGIN, f.y, [("areawide_yes", "Yes"), ("areawide_no", "No")])
    f.y -= 20
    f.bullets(DISCLOSURE_NOTES, size=7.8, color=GRAY)
    f.y -= 4

    f.heading("For properties with no certificate, the undersigned new deed holder acknowledges:")
    f.bullets(DISCLOSURE_NO_CERT, size=7.8, color=NAVY)
    f.y -= 4

    f.heading("New deed holder(s)")
    f.labeled_field("sale_date", "Estimated date of sale", MARGIN, f.y, half * 0.6)
    f.y -= 30
    f.labeled_field("printed_names", "Printed name(s)", MARGIN, f.y, CONTENT_W)
    f.y -= 30
    f.labeled_field("signature_1", "Signature (type your name)", MARGIN, f.y, half - 8)
    f.labeled_field("signature_2", "Second signature, if any", MARGIN + half, f.y, half * 0.6 - 8)
    f.labeled_field("signature_date", "Date", MARGIN + half + half * 0.6, f.y, half * 0.4)
    f.y -= 34
    f.paragraph("Declaration", size=8.5, bold=True)
    f.paragraph(DISCLOSURE_DECLARATION, size=7.8, color=GRAY)
    f.y -= 4
    f.paragraph(DISCLOSURE_SUBMIT, size=8)
    f.y -= 2
    f.paragraph(DISCLOSURE_FINES, size=7.8, color=GRAY)
    f.save()
    return f.page


# ── Small BMP Treatments Form (mirrors the June 2016 form)
# reportlab's choice() needs a non-empty default value, so the first option is a placeholder
NRCS_TREATMENTS = [
    "Choose a treatment", "Other treatment (type it in)",
    "BMP-001 Drip Line Infiltration Trench", "BMP-002 Roof Valley Drip Line Treatment", "BMP-003 Conveyance and Infiltration Components",
    "BMP-004 Drip Line Conveyance Swale", "BMP-005 Subsurface Conveyance System", "BMP-006 Infiltration System Components",
    "BMP-007 Infiltration System", "BMP-008 Infiltration Basin", "BMP-009 Armored Drip Line",
    "BMP-010 Erosion Control for Elevated Structures", "BMP-011 Erosion Control for Low Elevated Structures",
    "BMP-020 Slotted Channel Drain", "BMP-021 Slotted Channel Drain, Reverse Flow", "BMP-022 Driveway Conveyance Swale",
    "BMP-023 Driveway Infiltration Trench", "BMP-024 Driveway Edge Armor", "BMP-026 Parking Barriers",
    "BMP-030 Sediment Trap", "BMP-030A Sediment Trap Sizing Sheet", "BMP-040 Rock Slope Protection (No Fabric)",
    "BMP-041 Rock Slope Protection", "BMP-042 Stacked Rock Wall", "BMP-043 Timber Wall",
    "BMP-060 Filter Fabric for Infiltration Systems", "Restore compacted bare soil areas (till, amend, vegetate, and mulch)",
]
TREATMENTS_SCOPE = ("For BMP retrofit projects that disturb or grade less than 10 cubic yards of soil. Not for projects with engineered "
                    "structures, extensive grade alterations, excavations over 5 feet, paving more than 400 square feet, subsurface conveyance "
                    "systems (piping) and drop inlets, or infiltration systems capturing runoff from more than 2,500 square feet; those need a "
                    "BMP Retrofit Permit.")
TREATMENTS_HOW = ("Label each BMP on the site plan (A, B, C or 1, 2, 3), list the same label here with the treatment from the NRCS standard "
                  "drawings and its dimensions, and submit this form with the site plan and the Calculation Spreadsheet through Accela Citizen "
                  "Access. The review, the permit, and the final inspection are free.")
TREATMENTS_DISCLAIMER = ("This BMP site design is for the installation of Best Management Practices only. It is not a verification of land "
                         "coverage, land capability, unit of use, or other development capacities regulated by the Tahoe Regional Planning Agency "
                         "(TRPA), nor is it a conceptual approval of any unrelated future project. These verifications require the submittal of a "
                         "separate application to TRPA for review and approval. The property owner is ultimately responsible for the selection, "
                         "installation, performance, and maintenance of the BMPs on their property.")
TREATMENT_ROWS = 14


def build_treatments_form(path: Path):
    f = Form(path, "Small BMP Treatments Form", "Treatments proposed on a Small BMP Retrofit Plan, with dimensions, for TRPA review")
    f.new_page()
    c = f.c
    f.paragraph(TREATMENTS_SCOPE, size=8, color=GRAY)
    f.y -= 2
    f.paragraph(TREATMENTS_HOW, size=8.5)
    f.y -= 6
    half = CONTENT_W / 2
    f.heading("Parcel")
    for left, right in ((("apn", "Assessor's parcel number (APN)"), ("owner_name", "Owner name")),
                        (("address", "Property address"), ("owner_phone", "Owner phone")),
                        (("design_date", "Design date"), ("owner_email", "Owner email"))):
        f.labeled_field(left[0], left[1], MARGIN, f.y, half - 8)
        f.labeled_field(right[0], right[1], MARGIN + half, f.y, half)
        f.y -= 30
    f.heading("Designer contact information (if different from above)")
    for left, right in ((("designer_name", "Designer name"), ("designer_phone", "Phone")),
                        (("designer_license", "Professional license number"), ("designer_email", "Email"))):
        f.labeled_field(left[0], left[1], MARGIN, f.y, half - 8)
        f.labeled_field(right[0], right[1], MARGIN + half, f.y, half)
        f.y -= 30
    f.heading("Site description and notes")
    f.text_field("site_notes", MARGIN, f.y - 54, CONTENT_W, 52, tooltip="Site description and notes", multiline=True)
    f.y -= 62

    f.heading("Treatments")
    label_w, dims_w = 0.75 * inch, 1.9 * inch
    treat_w = CONTENT_W - label_w - dims_w - 12
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(GRAY)
    c.drawString(MARGIN + 2, f.y - 9, "BMP LABEL")
    c.drawString(MARGIN + label_w + 8, f.y - 9, "TREATMENT (NRCS STANDARD DRAWING, OR TYPE YOUR OWN)")
    c.drawString(MARGIN + label_w + treat_w + 14, f.y - 9, "DIMENSIONS")
    f.y -= 13
    row_h = 20
    for i in range(1, TREATMENT_ROWS + 1):
        f.need(row_h + 4)
        top = f.y
        c.setStrokeColor(LINE); c.setLineWidth(0.4); c.line(MARGIN, top, MARGIN + CONTENT_W, top)
        f.text_field(f"row{i:02d}_label", MARGIN + 1, top - row_h + 2, label_w - 2, row_h - 4, tooltip=f"Row {i}: label on the site plan", size=8)
        f.choice(f"row{i:02d}_treatment", MARGIN + label_w + 6, top - row_h + 2, treat_w, row_h - 4, NRCS_TREATMENTS, tooltip=f"Row {i}: treatment", editable=True)
        f.text_field(f"row{i:02d}_dimensions", MARGIN + label_w + treat_w + 12, top - row_h + 2, dims_w - 1, row_h - 4, tooltip=f"Row {i}: dimensions", size=8)
        f.y -= row_h
    c.line(MARGIN, f.y, MARGIN + CONTENT_W, f.y)
    f.y -= 10
    f.paragraph(TREATMENTS_DISCLAIMER, size=7.5, color=GRAY)
    f.y -= 6

    f.need(60)
    c.setFillColor(WELL)
    c.rect(MARGIN, f.y - 58, CONTENT_W, 58, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(GRAY)
    c.drawString(MARGIN + 8, f.y - 12, "FOR TRPA USE ONLY")
    f.checkbox("review_meets_code", MARGIN + 8, f.y - 30, size=11, tooltip="Design meets Chapter 60.4")
    c.setFont("Helvetica", 8)
    c.setFillColor(NAVY)
    c.drawString(MARGIN + 24, f.y - 27, "Based on the information provided, this design meets the requirements of Chapter 60.4 of the TRPA Code of Ordinances.")
    f.labeled_field("reviewed_by", "Reviewed by", MARGIN + 8, f.y - 36, half, h=14)
    f.labeled_field("review_date", "Date", MARGIN + half + 16, f.y - 36, half * 0.5, h=14)
    f.y -= 66
    f.save()
    return f.page


def build_maintenance_log(path: Path):
    f = Form(path, "BMP Inspection and Maintenance Log", "Inspection and maintenance record for Best Management Practices on a Tahoe Region property")
    f.new_page()
    f.property_block()
    f.paragraph(INTRO, size=8.5, color=NAVY)
    f.y -= 8
    for i, (title, ref, note, questions) in enumerate(SECTIONS, 1):
        f.section(i, title, ref, note, questions)
    f.notes_and_signature()
    f.save()
    return f.page


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "bmp-maintenance-log.pdf"
    pages = build_maintenance_log(out)
    print(f"wrote {out.relative_to(ROOT)}: {pages} pages, {len(SECTIONS)} BMP sections, {sum(len(s[3]) for s in SECTIONS)} questions, version {VERSION}")
    out = OUT_DIR / "bmp-real-estate-disclosure.pdf"
    print(f"wrote {out.relative_to(ROOT)}: {build_disclosure_form(out)} page(s)")
    out = OUT_DIR / "small-bmp-treatments-form.pdf"
    print(f"wrote {out.relative_to(ROOT)}: {build_treatments_form(out)} page(s), {TREATMENT_ROWS} treatment rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
