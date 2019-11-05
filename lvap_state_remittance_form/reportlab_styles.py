import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
    getSampleStyleSheet,
    ListStyle,
)
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    Frame,
    flowables,
    BaseDocTemplate,
    PageTemplate,
    PageBreak,
    ListFlowable,
    ListItem,
)
from reportlab.graphics.barcode import code39
from reportlab.graphics.shapes import Drawing
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, flowables
from reportlab.pdfbase.pdfmetrics import registerFontFamily, stringWidth

pdfmetrics.registerFont(
    TTFont("Arial", os.path.join(os.getcwd(), "fonts", "arial.ttf"))
)
pdfmetrics.registerFont(
    TTFont("Arial-Bold", os.path.join(os.getcwd(), "fonts", "arialbd.ttf"))
)
pdfmetrics.registerFont(
    TTFont("Arial-Narrow", os.path.join(os.getcwd(), "fonts", "arialn.ttf"))
)
pdfmetrics.registerFont(
    TTFont("Arial-Narrow-Bold", os.path.join(os.getcwd(), "fonts", "arialnbd.ttf"))
)
pdfmetrics.registerFont(
    TTFont(
        "LiberationSerif",
        os.path.join(os.getcwd(), "fonts", "LiberationSerif-Regular.ttf"),
    )
)
pdfmetrics.registerFont(
    TTFont(
        "LiberationSerif-Bold",
        os.path.join(os.getcwd(), "fonts", "LiberationSerif-Bold.ttf"),
    )
)


registerFontFamily(
    "Arial",
    normal="Arial",
    bold="Arial-Bold",
    italic="Arial-Bold",
    boldItalic="Arial-Bold",
)

width, height = letter

# left, right, top, bottom
gutters = (inch / 4, inch / 4, inch / 4, inch / 4)
margins = (inch / 4, inch / 4, inch / 2, inch / 2)
usable_width = width - (gutters[0] + gutters[1])
usable_height = height - (gutters[2] + gutters[3])

# heading, heading line, contact info, and date
styles = dict(
    body=ParagraphStyle(
        "default",
        fontName="Times-Roman",
        fontSize=12,
        leading=15,
        leftIndent=margins[0],
        rightIndent=margins[1],
        firstLineIndent=0,
        alignment=TA_LEFT,
        spaceBefore=0,
        spaceAfter=5,
        bulletFontName="Times-Roman",
        bulletFontSize=12,
        bulletIndent=0,
        backColor=None,
        wordWrap=None,
        borderWidth=0,
        borderPadding=0,
        borderColor=None,
        borderRadius=None,
        allowWidows=1,
        allowOrphans=0,
        textTransform=None,  # 'uppercase' | 'lowercase' | None
        endDots=None,
        splitLongWords=1,
    )
)
styles["heading"] = ParagraphStyle(
    "bold",
    parent=styles["body"],
    leading=18,
    textTransform="uppercase",
    fontName="Times-Roman",
    bulletFontName="Times-Roman",
    alignment=TA_CENTER,
)

styles["detail"] = ParagraphStyle(
    "detail",
    parent=styles["body"],
    fontSize=10,
    leading=11,
    leftIndent=3,
    rightIndent=3,
)

# used for notes underline
styles["note"] = ParagraphStyle(
    "note",
    parent=styles["body"],
    fontSize=8,
    leading=9.6,
    leftIndent=0,
    rightIndent=0,
    vAlign='TOP'
)

styles["detail-utc"] = ParagraphStyle(
    "detail",
    parent=styles["body"],
    fontSize=10,
    leading=11,
    leftIndent=3,
    rightIndent=3,
    spaceBefore=-20,
    spaceAfter=-15,
)
styles["detail-bold"] = ParagraphStyle(
    "detail", parent=styles["detail"], fontName="Helvetica-Bold"
)
styles["detail-bold-center"] = ParagraphStyle(
    "detail", parent=styles["detail"], fontName="Helvetica-Bold", alignment=TA_CENTER
)
styles["detail-mini"] = ParagraphStyle(
    "detail",
    parent=styles["detail-utc"],
    fontSize=9,
    leftIndent=0,
    rightIndent=0,
    spaceAfter=0,
    leading=9.6,
)

styles["detail-mini-utc"] = ParagraphStyle(
    "detail-mini-utc",
    parent=styles["detail-utc"],
    fontName="Times-Roman",
    fontSize=6.5,
    leftIndent=-5,
    rightIndent=0,
    spaceAfter=0,
    leading=8,
)
styles["detail-mini-utc-addons"] = ParagraphStyle(
    "detail-mini-utc",
    parent=styles["detail-utc"],
    fontName="Times-Roman",
    fontSize=7.5,
    leftIndent=-5,
    rightIndent=0,
    spaceAfter=0,
    leading=8,
)
styles["detail-mini-utc-right"] = ParagraphStyle(
    "detail-mini-utc",
    parent=styles["detail-utc"],
    fontName="Times-Roman",
    fontSize=6.5,
    leftIndent=-5,
    rightIndent=0,
    spaceAfter=0,
    leading=8,
    alignment=TA_RIGHT,
)

styles["detail-mini-utc-left"] = ParagraphStyle(
    "detail-mini-utc",
    parent=styles["detail-utc"],
    fontName="Times-Roman",
    fontSize=8.5,
    leftIndent=-5,
    rightIndent=10,
    spaceAfter=10,
    leading=12,
    alignment=TA_JUSTIFY,
)
styles["detail-mini-utc-center"] = ParagraphStyle(
    "detail-mini-utc-center",
    parent=styles["detail-utc"],
    fontName="Times-Roman",
    fontSize=8.5,
    leftIndent=-5,
    rightIndent=10,
    spaceAfter=10,
    leading=12,
    alignment=TA_CENTER,
)
styles["detail-mini-utc-tiny"] = ParagraphStyle(
    "detail-mini-utc-tiny",
    parent=styles["detail-utc"],
    fontName="Times-Roman",
    fontSize=4,
    leftIndent=0,
    rightIndent=0,
    spaceAfter=0,
    leading=2,
)
styles["detail-mini-overweight-cb"] = ParagraphStyle(
    "detail-mini-utc-tiny",
    parent=styles["detail-utc"],
    fontName="Times-Roman",
    fontSize=4,
    leftIndent=0,
    rightIndent=3,
    firstLineIndent=0,
    spaceAfter=2,
    leading=5,
)
styles["header"] = ParagraphStyle(
    "header", parent=styles["body"], fontSize=10, leading=16, leftIndent=0
)
styles["boxed"] = ParagraphStyle(
    "boxed",
    parent=styles["body"],
    borderWidth=1,
    borderPadding=3,
    borderColor=colors.black,
    alignment=TA_CENTER,
)
styles["heading-compact"] = ParagraphStyle(
    "heading-compact", parent=styles["heading"], spaceAfter=0, leading=12
)
styles["detail-compact"] = ParagraphStyle(
    "detail-compact",
    parent=styles["detail"],
    spaceAfter=0,
    leading=10,
    leftIndent=3,
    rightIndent=3,
)

styles["detail-compact-thp"] = ParagraphStyle(
    "detail-compact",
    parent=styles["detail"],
    fontSize=8,
    spaceAfter=0,
    leading=10,
    leftIndent=3,
    rightIndent=3,
)

styles["detail-compact-thp2"] = ParagraphStyle(
    "detail-compact",
    parent=styles["detail"],
    fontSize=7,
    spaceAfter=0,
    leading=6,
    leftIndent=-3,
    rightIndent=3,
)
styles["detail-compact-thp2-bold"] = ParagraphStyle(
    "detail-compact-thp2-bold-center",
    parent=styles["detail-compact-thp2"],
    fontName="Times-Bold",
)
styles["detail-compact-thp2-bold-center"] = ParagraphStyle(
    "detail-compact-thp2-bold-center",
    parent=styles["detail-compact-thp2"],
    fontName="Times-Bold",
    alignment=TA_CENTER,
)
styles["detail-compact-thp2-top"] = ParagraphStyle(
    "detail-compact",
    parent=styles["detail"],
    fontSize=7,
    spaceAfter=0,
    leading=6,
    leftIndent=-3,
    rightIndent=3,
    vAlign="TOP",
)
styles["detail-compact-thp2-right-skinny"] = ParagraphStyle(
    "detail-compact",
    parent=styles["detail"],
    fontSize=7,
    spaceAfter=0,
    leading=6,
    leftIndent=0,
    rightIndent=3,
    alignment=TA_RIGHT,
)
styles["detail-compact-thp3"] = ParagraphStyle(
    "detail-compact",
    parent=styles["detail"],
    fontSize=6,
    spaceAfter=0,
    leading=6,
    leftIndent=-3,
    rightIndent=3,
)
styles["detail-compact-thp3-space"] = ParagraphStyle(
    "detail-compact",
    parent=styles["detail"],
    fontSize=6,
    spaceAfter=2,
    leading=6,
    leftIndent=-3,
    rightIndent=3,
)

styles["detail-compact-thp3-right"] = ParagraphStyle(
    "detail-compact",
    parent=styles["detail"],
    fontSize=6,
    spaceAfter=0,
    leading=6,
    leftIndent=-3,
    rightIndent=3,
    alignment=TA_RIGHT,
)

styles["detail-compact-bold"] = ParagraphStyle(
    "detail-compact-bold",
    parent=styles["detail-utc"],
    spaceAfter=0,
    leading=10,
    leftIndent=3,
    rightIndent=3,
    alignment=TA_CENTER,
    fontName="Times-Bold",
)

styles["detail-flush"] = ParagraphStyle(
    "detail-compact",
    parent=styles["detail"],
    spaceBefore=0,
    spaceAfter=0,
    leading=11,
    leftIndent=0,
    rightIndent=0,
)
styles["detail-shrink"] = ParagraphStyle(
    "detail-flush", parent=styles["detail"], leading=10, fontSize=8
)

styles["sidebar"] = ParagraphStyle(
    "sidebar",
    parent=styles["detail"],
    fontName="Helvetica-Bold",
    spaceAfter=0,
    leading=10,
    leftIndent=0,
    rightIndent=0,
    backColor="black",
    textColor="white",
    alignment=TA_CENTER,
)
styles["trastop"] = ParagraphStyle(
    "trastop",
    parent=styles["detail-compact"],
    fontSize=8,
    leftIndent=0,
    rightIndent=0,
    spaceAfter=8,
)
styles["utt"] = ParagraphStyle(
    "bold",
    parent=styles["body"],
    # leading=18,
    textTransform="uppercase",
    # fontName='Times-Bold',
    # bulletFontName='Times-Bold',
    alignment=TA_CENTER,
    fontSize=7,
    spaceBefore=0,
    spaceAfter=0,
    leftIndent=0,
    rightIndent=0,
    leading=0,
)
styles["utt_text"] = ParagraphStyle(
    "bold",
    parent=styles["body"],
    # leading=18,
    textTransform="uppercase",
    # fontName='Times-Bold',
    # bulletFontName='Times-Bold',
    alignment=TA_CENTER,
    fontSize=7,
    fontName="Helvetica",
    spaceBefore=0,
    spaceAfter=0,
    leading=0,
)
styles["rotated_detail"] = ParagraphStyle(
    "detail",
    parent=styles["detail-utc"],
    textColor="white",
    backColor="black",
    alignment=TA_CENTER,
    fontSize=8,
    leading=11,
    leftIndent=-40,
    rightIndent=-20,
)
styles["rotated_detail_ov"] = ParagraphStyle(
    "detail",
    parent=styles["detail-utc"],
    textColor="white",
    backColor="black",
    alignment=TA_CENTER,
    fontSize=8,
    leading=11,
    leftIndent=-10,
    rightIndent=-20,
)


styles["rotated_detail_complaint"] = ParagraphStyle(
    "detail",
    parent=styles["detail-utc"],
    textColor="white",
    backColor="black",
    alignment=TA_CENTER,
    fontSize=8,
    leading=11,
    leftIndent=-70,
    rightIndent=-20,
)


styles["rotated_detail_complaint_ov"] = ParagraphStyle(
    "detail",
    parent=styles["detail-utc"],
    textColor="white",
    backColor="black",
    alignment=TA_CENTER,
    fontSize=8,
    leading=11,
    leftIndent=-25,
    rightIndent=10,
    borderColor="#FF0000",
    borderWidth=1,
)

styles["rotated_detail_defendant"] = ParagraphStyle(
    "detail",
    parent=styles["detail-utc"],
    textColor="white",
    backColor="black",
    alignment=TA_CENTER,
    fontSize=8,
    leading=11,
    leftIndent=-40,
    rightIndent=-10,
)

styles["rotated_detail_defendant_ov"] = ParagraphStyle(
    "detail",
    parent=styles["detail-utc"],
    textColor="white",
    backColor="black",
    alignment=TA_CENTER,
    fontSize=8,
    leading=11,
    leftIndent=-25,
    rightIndent=10,
    borderColor="#FF0000",
    borderWidth=1,
)

styles["rotated_detail_vehicle"] = ParagraphStyle(
    "detail",
    parent=styles["detail-utc"],
    textColor="white",
    backColor="black",
    alignment=TA_CENTER,
    fontSize=8,
    leading=11,
    leftIndent=-47,
    rightIndent=-30,
)
styles["rotated_detail_vehicle_ov"] = ParagraphStyle(
    "detail",
    parent=styles["detail-utc"],
    textColor="white",
    backColor="black",
    alignment=TA_CENTER,
    fontSize=8,
    leading=11,
    leftIndent=-25,
    rightIndent=10,
    borderColor="#FF0000",
    borderWidth=1,
)
styles["rotated_detail_use_ov"] = ParagraphStyle(
    "detail",
    parent=styles["detail-utc"],
    textColor="white",
    backColor="black",
    alignment=TA_CENTER,
    fontSize=8,
    leading=11,
    leftIndent=-10,
    rightIndent=-10,
    borderColor="#FF0000",
    borderWidth=1,
)
styles["rotated_detail_violation"] = ParagraphStyle(
    "detail",
    parent=styles["detail-utc"],
    textColor="white",
    backColor="black",
    alignment=TA_CENTER,
    fontSize=8,
    leading=11,
    leftIndent=-35,
    rightIndent=0,
)

styles["bullet"] = ListStyle(
    "list_default",
    leftIndent=20,
    rightIndent=0,
    spaceBefore=0,
    spaceAfter=5,
    bulletAlign="right",
    bulletType="bullet",
    bulletColor="black",
    bulletFontName="Helvetica",
    bulletFontSize=5,
    bulletOffsetY=-3,
    fontName="Times-Roman",
)

styles["rotated_detail_incident"] = ParagraphStyle(
    "detail",
    parent=styles["detail-utc"],
    textColor="white",
    backColor="black",
    alignment=TA_CENTER,
    fontSize=8,
    leading=11,
    leftIndent=-25,
    rightIndent=0,
)


styles["rotated_detail_incident_ov"] = ParagraphStyle(
    "detail",
    parent=styles["detail-utc"],
    textColor="white",
    backColor="black",
    alignment=TA_CENTER,
    fontSize=8,
    leading=11,
    leftIndent=-25,
    rightIndent=10,
    borderColor="#FF0000",
    borderWidth=1,
)

styles["rotated_detail_bond"] = ParagraphStyle(
    "detail",
    parent=styles["detail-utc"],
    textColor="white",
    backColor="black",
    alignment=TA_CENTER,
    fontSize=8,
    leading=11,
    leftIndent=-35,
    rightIndent=-5,
)

styles["rotated_detail_bond_ov"] = ParagraphStyle(
    "detail",
    parent=styles["detail-utc"],
    textColor="white",
    backColor="black",
    alignment=TA_CENTER,
    fontSize=8,
    leading=11,
    leftIndent=-25,
    rightIndent=10,
    borderColor="#FF0000",
    borderWidth=1,
)


styles["rotated_detail_courtplacedate"] = ParagraphStyle(
    "detail",
    parent=styles["detail-utc"],
    textColor="white",
    backColor="black",
    alignment=TA_CENTER,
    fontSize=8,
    leading=11,
    leftIndent=-14,
    rightIndent=-6,
)
styles["rotated_detail_courtplacedate_ov"] = ParagraphStyle(
    "detail",
    parent=styles["detail-utc"],
    textColor="white",
    backColor="black",
    alignment=TA_CENTER,
    fontSize=8,
    leading=11,
    leftIndent=-25,
    rightIndent=10,
    borderColor="#FF0000",
    borderWidth=1,
)

styles["citation_table"] = TableStyle(
    [
        ("INNERGRID", (0, 0), (-1, -1), 0, colors.blue),
        ("BOX", (0, 0), (-1, -1), 0, colors.red),
    ]
)

styles["citation_table_header"] = TableStyle(
    [
        ("BACKGROUND", (0, 0), (-1, -1), colors.red),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("ALIGNMENT", (0, 0), (-1, -1), "CENTER"),
    ]
)

styles["detail-bold-center-large"] = ParagraphStyle(
    "detail",
    parent=styles["detail"],
    fontSize=12,
    fontName="Helvetica-Bold",
    alignment=TA_CENTER,
)

styles["detail-slimfit"] = ParagraphStyle(
    "detail-compact",
    parent=styles["detail"],
    spaceAfter=0,
    leading=10,
    leftIndent=-3,
    rightIndent=0,
)

styles["detail-slimfit-right"] = ParagraphStyle(
    "detail-compact",
    parent=styles["detail"],
    spaceAfter=0,
    leading=10,
    leftIndent=-3,
    rightIndent=0,
    alignment=TA_RIGHT,
)

# new style for ivap form main tables
styles["iv-main-table"] = TableStyle([
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
])


def extend_style(style, **params):
    return ParagraphStyle("extended", parent=style, **params)


def auto_span_table(table_list, **params):
    if "style" not in params:
        params["style"] = []
    spans = []
    for i, row in enumerate(table_list):
        span_start = 0
        span_end = 0
        for j, col in enumerate(row):
            if col is None:
                span_end += 1
            else:
                if span_start < span_end:
                    spans.append(("SPAN", (span_start, i), (span_end, i)))
                span_start = j
                span_end = j
        if span_start < span_end:
            spans.append(("SPAN", (span_start, i), (span_end, i)))
    params["style"] += spans
    return Table(table_list, **params)


black_line = flowables.HRFlowable(
    width="92%",
    color="black",
    thickness=1,
    lineCap="round",
    spaceBefore=0,
    spaceAfter=1,
    hAlign="CENTER",
    vAlign="BOTTOM",
    dash=None,
)
grey_line = flowables.HRFlowable(
    width="92%",
    thickness=1,
    lineCap="round",
    spaceBefore=1,
    spaceAfter=1,
    hAlign="CENTER",
    vAlign="BOTTOM",
    dash=None,
)
black_line_ul = flowables.HRFlowable(
    width="100%",
    color="black",
    thickness=0.5,
    lineCap="round",
    spaceBefore=0,
    spaceAfter=1,
    hAlign="CENTER",
    vAlign="BOTTOM",
    dash=None,
)

black_line_short = flowables.HRFlowable(
    width="70%",
    color="black",
    thickness=0.5,
    lineCap="round",
    spaceBefore=0,
    spaceAfter=1,
    hAlign="RIGHT",
    vAlign="BOTTOM",
    dash=None,
)

# space=Spacer(1,0.2*inch)

yes_box = "<img height='10' width='12' src='%s' />&nbsp;" % os.path.join(
    os.getcwd(), "images", "crossbox.png"
)
no_box = "<img height='10' width='12' src='%s' />&nbsp;" % os.path.join(
    os.getcwd(), "images", "box.png"
)


class PageNumCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_date()
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_date(self):
        import datetime

        dt = datetime.datetime.now().strftime("%m/%d/%Y")
        self.setFont("Times-Roman", 9)
        self.drawCentredString(200 * mm, 267 * mm, dt)

    def draw_page_number(self, page_count):
        page = "Page %s of %s" % (self._pageNumber, page_count)
        self.setFont("Times-Roman", 9)
        self.drawCentredString(110 * mm, 6 * mm, page)


class OneDatePageNumCanvas(PageNumCanvas):
    def draw_date(self):
        if self._pageNumber == 1 or self._pageNumber == len(self.pages):
            PageNumCanvas.draw_date(self)


class RotatedPara(Paragraph):
    def draw(self):
        self.style = extend_style(
            self.style, spaceBefore=0, spaceAfter=-1 * self.style.fontSize
        )

        self.canv.saveState()

        textWidth = stringWidth(self.text, self.style.fontName, self.style.fontSize)
        textHeight = self.style.fontSize
        self.canv.translate(0, -textWidth + 1.5)
        self.canv.rotate(90)
        x, y = self.wrap(textWidth + 10, textHeight)
        self.canv.setStrokeColor(self.style.backColor)
        lw = 3
        self.canv.setLineWidth(lw)
        self.canv.line(
            x, y - textHeight - lw + 2, x - textWidth - 10, y - textHeight - lw + 2
        )
        Paragraph.draw(self)

        self.canv.restoreState()


# START ILLINOIS CITATION REPORT
pdfmetrics.registerFont(
    TTFont("LucidaType", os.path.join(os.getcwd(), "fonts", "LucidaSansTypewriter.ttf"))
)
pdfmetrics.registerFont(
    TTFont(
        "LucidaType-Bold",
        os.path.join(os.getcwd(), "fonts", "LucidaSansTypewriter-Bold.ttf"),
    )
)
pdfmetrics.registerFontFamily("LucidaType", normal="LucidaType", bold="LucidaType-Bold")


def extend_table_style(style, *params):
    return TableStyle(parent=style, *params)


styles["il-citation-main-table"] = TableStyle(
    [
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]
)
styles["il-citation-main-nt-table"] = TableStyle(
    [
        ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 0.5 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.5 * mm),
    ]
)
styles["il-citation-main"] = ParagraphStyle(
    "il-citation-main",
    fontSize=6,
    leading=8,
    spaceBefore=0,
    spaceAfter=0,
    leftIndent=0,
    rightIndent=0,
    wordWrap=None,
    alignment=TA_LEFT,
    fontName="Arial",
)
styles["il-citation-doc-header"] = ParagraphStyle(
    "il-citation-doc-header",
    parent=styles["il-citation-main"],
    fontSize=8,
    leading=10,
    fontName="Arial-Bold",
    alignment=TA_CENTER,
)
styles["il-citation-table-header"] = ParagraphStyle(
    "il-citation-table-header",
    parent=styles["il-citation-main"],
    spaceBefore=2,
    spaceAfter=2,
    leftIndent=1,
    rightIndent=1,
)
styles["il-citation-field-header"] = ParagraphStyle(
    "il-citation-field-header",
    fontName="Arial-Bold",
    fontSize=5.5,
    leading=6.5,
    leftIndent=0,
    rightIndent=0,
)
styles["il-citation-field-header-sm"] = ParagraphStyle(
    "il-citation-field-header-sm",
    parent=styles["il-citation-field-header"],
    fontSize=4.75,
    leading=5.75,
)
styles["il-citation-field-data"] = ParagraphStyle(
    "il-citation-field-header",
    fontName="Arial",
    fontSize=7,
    leading=8,
    leftIndent=0,
    rightIndent=0,
)
styles["il-citation-rotated"] = ParagraphStyle(
    "il-citation-rotated",
    parent=styles["il-citation-main"],
    textColor="white",
    alignment=TA_CENTER,
    fontName="Arial-Bold",
    fontSize=7.5,
    leading=0,
    leftIndent=0,
    rightIndent=0,
)
styles["il-citation-instructions"] = ParagraphStyle(
    "il-citation-instructions",
    parent=styles["il-citation-main"],
    alignment=TA_JUSTIFY,
    fontName="Arial",
    fontSize=6.5,
    leading=7.5,
    leftIndent=0,
    rightIndent=0,
)
styles["il-citation-instructions-header"] = ParagraphStyle(
    "il-citation-instructions-header",
    parent=styles["il-citation-instructions"],
    alignment=TA_CENTER,
    fontName="Arial-Bold",
)
styles["il-citation-main-nt"] = ParagraphStyle(
    "il-citation-main-nt",
    fontSize=6,
    leading=8,
    spaceBefore=0,
    spaceAfter=0,
    leftIndent=0,
    rightIndent=0,
    wordWrap=None,
    alignment=TA_LEFT,
    fontName="LucidaType",
)
styles["il-citation-field-header-nt"] = ParagraphStyle(
    "il-citation-field-header-nt",
    parent=styles["il-citation-main-nt"],
    fontSize=7,
    leading=9,
)
styles["il-citation-field-header-nt-tiny"] = ParagraphStyle(
    "il-citation-field-header-nt-tiny",
    parent=styles["il-citation-field-header-nt"],
    fontSize=4.5,
    leading=5,
)
styles["il-citation-field-data-nt"] = ParagraphStyle(
    "il-citation-field-data-nt",
    parent=styles["il-citation-main-nt"],
    fontName="Times-Bold",
    fontSize=8,
    leading=10,
)
styles["il-citation-instructions-nt"] = ParagraphStyle(
    "il-citation-instructions-nt",
    parent=styles["il-citation-main-nt"],
    fontName="Times-Bold",
    fontSize=9,
    leading=12,
)
# END ILLINOIS CITATION REPORT
