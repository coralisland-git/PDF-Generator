import cStringIO

from document_specific_styles import *
from common.signatures import *


def generate_cash_bond_refund():
    cr = CBRReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class CBRReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (24.4 * mm, 14.4 * mm)
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
            Spacer(0, 12.4 * mm),
            Image('brookhaven.jpg', 72 * mm, 31.5 * mm),
            Spacer(0, 32 * mm),
            Paragraph(
                "CASH BOND REFUND",
                styles["rc-doc-header-fda"]
            ),
            Spacer(0, 9.8 * mm),
            Paragraph(
                "DATE:"+"&nbsp;"*8+"<u>March 14, 2018</u>", 
                styles["rc-aawp-main-content"]
            ),
            Paragraph(
                "Defendant's Name:"+"&nbsp;"*5+"<u>Andres Ayona</u>", 
                styles["rc-aawp-main-content"]
            ),
            Paragraph(
                "Citation#:"+"&nbsp;"*2+"<u>E39566</u>",
                extend_style(styles["rc-aawp-main-content"])
            ),
            Paragraph(
                "CHECK #:"+"&nbsp;"*2+"<u>22636</u>",
                extend_style(styles["rc-aawp-main-content"], spaceBefore=42)
            ),
            Paragraph(
                "AMOUNT:"+"&nbsp;"+"$ <u>525.00</u>", 
                extend_style(styles["rc-aawp-main-content"], spaceBefore=42)
            ),
            Paragraph(
                "RECEIVED BY: "+"_"*28, 
                extend_style(styles["rc-aawp-main-content"], spaceBefore=42)
            ),
            Paragraph(
                "Date: "+"_"*20, 
                styles["rc-aawp-main-content"]
            ),
            Paragraph(
                "<u>Merced Mendez</u>", 
                styles["rc-aawp-main-content"]
            )
        ]
        
        return elems
