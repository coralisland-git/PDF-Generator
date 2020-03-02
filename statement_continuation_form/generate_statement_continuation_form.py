import cStringIO

from document_specific_styles import *
from common.signatures import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Flowable, Paragraph, Table, Spacer

def generate_officer_recommendation_form():
    cr = ORFReport()
    buff = cStringIO.StringIO()
    page_count = cr.get_page_count(buff)    
    return cr.create_report(buff, page_count)


class ORFReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (12.4 * mm, 12.4 * mm)
        self.sections = ["content"]
        self.title = title
        self.author = author
        self.data = None
        self.description = """Test Data"""

    def create_report(self, buff=None, page_count=None):
        def get_method(section):
            try:
                method = getattr(self, "_section_" + section)
            except AttributeError:
                raise Exception("Section method not found: " + section)
            return method

        def page_number(canv, doc):
            table = Table(
                [
                    [
                        Image('brookhaven.jpg', 42 * mm, 15 * mm),
                        Table(
                            [
                                [
                                    Paragraph(
                                        "BROOKHAVEN POLICE DEPARTMENT",
                                        styles["rc-doc-header-scf"],
                                    ),
                                ],
                                [
                                    Paragraph(
                                        "STATEMENT CONTINUATION FORM",
                                        extend_style(styles["rc-doc-header-scf"], fontSize=13.5, leading=14),
                                    )
                                ]
                            ],
                            style=styles["rc-main-table"]
                        )
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("ALIGN", (0, 0), (0, 0), "RIGHT"),
                    ("RIGHTPADDING", (0, 0), ( 0, 0), 7 * mm ),
                ]),
                colWidths=(48*mm, 130*mm)
            )
            table.wrapOn(canv, self.page_size[0], 0)
            table.drawOn(canv, 20*mm, self.page_size[1] - 26.2*mm)
            space = "&nbsp;"*5
            page_num = Paragraph(
                "PAGE &nbsp; <u>"+space+str(doc.page)+space+"</u> &nbsp;&nbsp; OF &nbsp;&nbsp; <u>"+space+str(page_count)+space+"</u>",
                extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER, spaceBefore=30, leftIndent=22, leading=13),
            )
            page_num.wrapOn(canv, self.page_size[0], 0)
            page_num.drawOn(canv, 0, self.page_size[1] - 39.2*mm)

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
                self.page_size[1] - self.page_margin[1] * 3.4,
                leftPadding=0,
                bottomPadding=0,
                rightPadding=0,
                topPadding=8.4*mm,
            )
        ], onPage=page_number)
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

    def get_page_count(self, buff=None):
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
        return doc_t.page

    def get_lines(self, description):
        description = description.replace('\n','').replace('\t', '')
        w_temp = description.split(' ')
        word_list = []
        for word in w_temp:
            if word != '':
                word_list.append(word)
        lines = []
        begin_idx = 0
        idx = 0        
        while idx <= len(word_list):
            line = ' '.join(word_list[begin_idx:idx])
            t_len = stringWidth(line, "Times-Roman", 10)
            if t_len > 535.0:                
                if t_len > 538.0:
                    line = ' '.join(word_list[begin_idx:idx-1])
                    begin_idx = idx-1
                else:
                    begin_idx = idx
                lines += [
                    [
                        Paragraph(line,
                            extend_style(styles["rc-aawp-main-content-tb"], leading=14),
                        )
                    ]
                ]
            idx += 1
        lines += [
            [
                Paragraph(line,
                    extend_style(styles["rc-aawp-main-content-tb"], leading=14),
                )
            ]
        ]
        l_count = len(lines)
        if l_count < 23:
            for idx in range(l_count, 23):
                lines += [
                    [
                        Paragraph('', extend_style(styles["rc-aawp-main-content-tb"], leading=14))
                    ]
                ]
        if l_count > 23 and l_count < 27:
            for idx in range(0, 27-l_count):
                lines += [
                    [
                        Paragraph('', extend_style(styles["rc-aawp-main-content-tb"], leading=14))
                    ]
                ]
        return lines

    def _section_content(self):
        elems = list()
        lines = self.get_lines(self.description)
        for line in lines:
            elems += [
                Table(                
                    [line],
                    style=extend_table_style(styles["rc-main-table"], [
                        ("LINEBELOW", (0, 0), (0, 0), 0.1, "black")
                    ]),
                    rowHeights=8.2 * mm
                )
            ]
        elems +=[
            Spacer(0, 12.4 * mm),
            Table(
                [
                    [
                        Paragraph(
                            "PERSON MAKING STATEMENT SIGNATURE",
                            styles["rc-aawp-main-content-tb"],
                        ),
                        None,
                        Paragraph(
                            "TODAY'S DATE & TIME",
                            styles["rc-aawp-main-content-tb"],
                        ),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEABOVE", (0, 0), (0, 0), 0.1, "black"),
                    ("LINEABOVE", (2, 0), (2, 0), 0.1, "black"),
                    ("LEFTPADDING", (0, 0), ( -1, -1), 1.6 * mm )
                ]),
                colWidths=(76*mm, 10*mm, 68*mm, 36*mm)
            ),
            Spacer(0, 4.4 * mm),
            Table(
                [
                    [
                        Paragraph(
                            "OFFICER'S SIGNATURE",
                            styles["rc-aawp-main-content-tb"],
                        ), None,
                        Paragraph(
                            "BADGE #",
                            styles["rc-aawp-main-content-tb"],
                        ), None,
                        Paragraph(
                            "CASE NUMBER",
                            styles["rc-aawp-main-content-tb"],
                        ), None                 
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEABOVE", (0, 0), (0 , 0), 0.1, "black"),
                    ("LINEABOVE", (2, 0), (2, 0), 0.1, "black"),
                    ("LINEABOVE", (4, 0), (4, 0), 0.1, "black"),
                    ("LEFTPADDING", (0, 0), ( -1, -1), 1.6 * mm )
                ]),
                colWidths=(55*mm, 5*mm, 48*mm, 5*mm, 60*mm, 17*mm)
            )
        ]
        
        return elems