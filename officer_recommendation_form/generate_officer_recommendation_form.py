import cStringIO

from document_specific_styles import *
from common.signatures import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT


def generate_officer_recommendation_form():
    cr = ORFReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class ORFReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (24.4 * mm, 9.4 * mm)
        self.sections = ["content"]
        self.title = title
        self.author = author
        self.data = None

    def create_report(self, buff=None):
        def get_method(section):
            try:
                method = getattr(self, "_section_" + section)
            except AttributeError:
                raise Exception("Section method not found: " + section)
            return method     

        if not buff:
            buff = io.BytesIO()

        story = []
        for section in self.sections:
            elems = get_method(section)()
            for elem in elems:
                story.append(elem)

        page_t = PageTemplate('normal', [
            Frame(
                self.page_margin[0],
                self.page_margin[1],
                self.page_size[0] - self.page_margin[0] * 2,
                self.page_size[1] - self.page_margin[1] * 2,
                leftPadding=0,
                bottomPadding=0,
                rightPadding=0,
                topPadding=0,
            )
        ])
        doc_t = BaseDocTemplate(
            buff,
            pagesize=letter,
            title=self.title,
            author=self.author,
            leftMargin=self.page_margin[0],
            rightMargin=self.page_margin[0],
            topMargin=self.page_margin[1],
            bottomMargin=self.page_margin[1],
        )
        doc_t.addPageTemplates(page_t)
        doc_t.build(story)
        buff.seek(0)
        return buff

    def _section_content(self):
        elems = list()
        elems += [
            Table(
                [
                    [
                        None,
                        Paragraph(
                            "BROOKHAVEN MUNICIPAL COURT",
                            extend_style(styles["rc-doc-header-orf"],leading=9),
                        ),
                        Image('brookhaven.jpg', 51 * mm, 22 * mm)
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("OUTLINE", (2, 0), (-1, -1), 0.1, "black"),
                    ("LEFTPADDING", (2, 0), ( 2, 0), 2.6 * mm ),
                    ("RIGHTPADDING", (2, 0), ( 2, 0), 1.6 * mm ),
                    ("TOPPADDING", (2, 0), ( 2, 0), 1.2 * mm ),
                    ("BOTTOMPADDING", (2, 0), ( 2, 0), 7.8 * mm )                    
                ]),
                colWidths=(57*mm, 82*mm, 56 * mm)
            ),
            Paragraph(
                "ISSUING OFFICER'S RECOMMENDATION FORM",
                extend_style(styles["rc-doc-header-orf"], spaceBefore=15),
            ),
            Paragraph("<b>ALLEGED OFFENSE:</b>", styles["rc-aawp-main-content"]),
            Paragraph("_"*6+" PARKING TICKET (OFFENSE CITED) "+"_"*37, styles["rc-aawp-main-content"]),
            Paragraph("_"*6+" INTERSECTION SAFETY VIOLATIONS (PHOTO-ENFORCED)", styles["rc-aawp-main-content"]),
            Paragraph("_"*6+" UNIFORM TRAFFIC CITATION (OFFENSE CITED) "+"_"*27, styles["rc-aawp-main-content"]),
            Paragraph("_"*6+" CODE ENFORCEMENT OFFICER (OFFENSE CITED) "+"_"*25, styles["rc-aawp-main-content"]),
            Paragraph("OFFENSE DATE: "+"_"*24+" TIME: "+"_"*31, styles["rc-aawp-main-content"]),
            Paragraph("TICKET NUMBER: "+"_"*60, styles["rc-aawp-main-content"]),
            Paragraph("TAG NUMBER: "+"_"*28+" STATE: "+"_"*10+" YEAR "+"_"*12, styles["rc-aawp-main-content"]),
            Paragraph("VIN NUMBER: "+"_"*64, styles["rc-aawp-main-content"]),
            Paragraph("VEHICLE MAKE: "+"_"*38+" COLOR: "+"_"*16, styles["rc-aawp-main-content"]),
            Paragraph("LOCATION: "+"_"*66, extend_style(styles["rc-aawp-main-content"], leading=6)),
            Paragraph("<b>_</b>"*94, extend_style(styles["rc-aawp-main-content"], spaceBefore=0, leading=12)),
            Paragraph("I, "+"_"*50+" , as the citing Officer, recommend that the<br /> above Citation be:", styles["rc-aawp-main-content"]),
            Table(
                [
                    [
                        Paragraph("Considered for:", styles["rc-aawp-main-content"]),
                        Paragraph("_"*5+" Dismissal", styles["rc-aawp-main-content"]),
                    ],
                    [
                        None, Paragraph("_"*5+" Nolle Prossed", styles["rc-aawp-main-content"]),
                    ],
                    [
                        None, Paragraph("_"*5+" Reduced to a Warning", styles["rc-aawp-main-content"]),
                    ],
                    [
                        None, Paragraph("_"*5+" Reduction in normal fine to $ "+"_"*6, styles["rc-aawp-main-content"]),
                    ],
                    [
                        None, Paragraph("_"*5+" Other: "+"_"*56, styles["rc-aawp-main-content"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                ]),
                colWidths=(25 * mm, 142 * mm),
                rowHeights=8.8*mm
            ),
            Paragraph("Reason: "+"_"*85, extend_style(styles["rc-aawp-main-content"], leading=6)),
            Paragraph("<b>_</b>"*94, extend_style(styles["rc-aawp-main-content"], spaceBefore=0, leading=12)),
            Paragraph("Submitted by: (Requesting Officer) "+"_"*41+" Date "+"_"*18, styles["rc-aawp-main-content"]),
            Paragraph("Approved by: (Supervisor) "+"_"*48+" Date "+"_"*18, styles["rc-aawp-main-content"]),
            Paragraph("Approved by (Solicitor) "+"_"*50+" Date "+"_"*19, styles["rc-aawp-main-content"]),
        ]
        
        return elems

