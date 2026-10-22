"""Generate the BMP program's fillable PDF forms as standard AcroForms.

The legacy forms were Adobe LiveCycle (XFA) files that browsers cannot display. This
script draws each form with reportlab and adds ordinary AcroForm widgets, so the PDF
opens, fills, and prints in Chrome, Edge, Firefox, Safari, and Acrobat alike.

  "C:\\Program Files\\ArcGIS\\Pro\\bin\\Python\\envs\\arcgispro-py3\\python.exe" scripts/build_forms.py

Outputs:
  forms/bmp-maintenance-log.pdf   BMP Inspection and Maintenance Log (replaces the 2016 XFA log)

The content below mirrors the 2016 log (20 BMP sections, each with a Location column,
Yes and No boxes, and a Documentation / Corrective Action column) with the wording
brought up to date (10 cubic yards, no lava rock or recycled tires). Edit the SECTIONS
list to change the questions; field names are derived from the section and row numbers.
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
    """Draws the log across as many pages as the sections need, with widgets placed as it goes."""

    def __init__(self, path: Path):
        self.c = canvas.Canvas(str(path), pagesize=letter)
        self.c.setTitle("BMP Inspection and Maintenance Log")
        self.c.setAuthor("Tahoe Regional Planning Agency, Stormwater Management Program")
        self.c.setSubject("Inspection and maintenance record for Best Management Practices on a Tahoe Region property")
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
        c.drawString(MARGIN, PAGE_H - 0.5 * inch, "BMP Inspection and Maintenance Log")
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.HexColor("#B4CBE8"))
        c.drawString(MARGIN, PAGE_H - 0.68 * inch, "TRPA Stormwater Management Program  |  BMP Hotline (775) 589-5202  |  bmp@trpa.gov")
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
        c.drawString(MARGIN, 0.35 * inch, f"BMP Inspection and Maintenance Log, {VERSION}. Generated from the Lake Tahoe BMPs site; opens in any browser.")
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


def build_maintenance_log(path: Path):
    f = Form(path)
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
