import cStringIO

from document_specific_styles import *
from common.signatures import *


def generate_entry_of_appearance():
    cr = EOAReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class EOAReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (24.4 * mm, 9.4 * mm)
        self.sections = ["content"]
        self.title = title
        self.author = author
        self.data = None
        self.month = 2
        self.day = 28

    def get_month(self, month):
        mon_arr = [
            'January', 'February',' March', 'April', 'May', 'June', 'July',
            'August', 'September', 'October', 'November', 'December'
        ]
        try:
            month = int(month)
            if month > 12 or month < 1:
                return ''
            else:
                m_t = '0' + str(month) if month < 10 else str(month)
                return mon_arr[month-1] + ' (' + m_t + ')'
        except:
            return ''

    def get_day(self, day):
        try:
            day = int(day)
            if day > 31 or day < 0:
                return ''
            if day == 1:
                day = '1st'
            elif day == 2:
                day = '2nd'
            elif day == 3:
                day = '3rd'
            else:
                day = str(day) + 'th'
            return day
        except:
            return ''

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
            Spacer(0, 4 * mm),
            Image('brookhaven.jpg', 40 * mm, 16 * mm),            
            Paragraph(
                "IN THE MUNICIPAL COURT OF BROOKHAVEN <br />STATE OF GEORGIA",
                styles["rc-doc-header"]
            ),
            Spacer(0, 8.8 * mm),
            Table(
                [
                    [
                        Paragraph("STATE OF GEORGIA", styles["rc-aawp-main-content"]),
                        Paragraph("Case Number(s):", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(101*mm, 28*mm, 38*mm),
            ),
            Spacer(0, 1.6 * mm),
            Table(
                [
                    [
                        Paragraph("VS.", extend_style(styles["rc-aawp-main-content"], leftIndent=12*mm)), 
                        None,
                        Paragraph("Test Data", styles["rc-aawp-main-content"])
                    ],
                    [
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),
                        None, 
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                    ("LINEBELOW", (0, 1), (0, 1), 0.1, "black")
                ]),
                colWidths=(52*mm, 63*mm, 52*mm),
                rowHeights=7.2*mm
            ),
            Paragraph("ENTRY OF APPEARANCE", extend_style(styles["rc-doc-header"])),
            Spacer(0, 13.2 * mm),
            Paragraph(
                "&nbsp;"*13+"I, <u>"+"&nbsp;"*28+"Test Data"+"&nbsp;"*28+"</u>, Attorney at Law, hereby request the Clerk of said Court to enter my name as attorney of record for the above named defendant.",
                extend_style(styles["rc-aawp-main-content"])
            ),
            Paragraph(
                "&nbsp;"*13+"The official address to which all notices on behalf of the Court may be provided to me is, to wit:",
                extend_style(styles["rc-aawp-main-content"], spaceBefore=10)
            ),
            Table(
                [
                    [
                        Paragraph("1 Test Dr. Apt. 123, Testcity, XX 12345", styles["rc-aawp-main-content"])
                    ],
                    [
                        Paragraph("1 Test Dr. Apt. 123, Testcity, XX 12345", styles["rc-aawp-main-content"])
                    ],
                    [
                        Paragraph("1 Test Dr. Apt. 123, Testcity, XX 12345", styles["rc-aawp-main-content"])
                    ],
                    [
                        Paragraph("1 Test Dr. Apt. 123, Testcity, XX 12345", styles["rc-aawp-main-content"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (0, 3), 0.1, "black"),
                ]),
                colWidths=(92*mm),
                rowHeights=8.4*mm
            ),
            Table(
                [
                    [
                        Paragraph("Telephone number:", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"]), 
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.1, "black")        
                ]),
                colWidths=(31*mm, 75*mm, 15*mm),
                rowHeights=8.4*mm
            ),
            Table(
                [
                    [
                        Paragraph("Email:", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"]), 
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.1, "black"),                    
                ]),
                colWidths=(11*mm, 96*mm, 15*mm),
                rowHeights=8.4*mm
            ),
            Spacer(0, 7.8 * mm),
            Table(
                [
                    [
                        None,
                        Paragraph("This", styles["rc-aawp-main-content"]),
                        Paragraph(self.get_day(self.day), styles["rc-aawp-main-content"]),
                        Paragraph("day of", styles["rc-aawp-main-content"]),
                        Paragraph(self.get_month(self.month), styles["rc-aawp-main-content"]),
                        Paragraph(", 20", styles["rc-aawp-main-content"]),
                        Paragraph("XX", styles["rc-aawp-main-content"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                    ("LINEBELOW", (4, 0), (4, 0), 0.1, "black"),
                    ("LINEBELOW", (6, 0), (6, 0), 0.1, "black")
                ]),
                colWidths=(63*mm, 8*mm, 14*mm, 12*mm, 56*mm, 6*mm, 8*mm),
                rowHeights=8.4*mm
            ),
            Spacer(0, 11.2 * mm),
            Table(
                [
                    [
                        None, Paragraph("By:", styles["rc-aawp-main-content"]), None
                    ],
                    [
                        None, None, Paragraph("Signature", extend_style(styles["rc-aawp-main-content"], leftIndent=6.4*mm))
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(88*mm, 6*mm, 73*mm),
                rowHeights=5.4*mm
            ),
            Spacer(0, 7.8 * mm),
            Table(
                [
                    [
                        None, 
                        Paragraph("State Bar of Ga. No.", styles["rc-aawp-main-content"]), 
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(88*mm, 33*mm, 46*mm),
                rowHeights=8.4*mm
            ),
            Spacer(0, 38.2 * mm),
            Paragraph("Remised Aug, 2016", extend_style(styles["rc-aawp-main-content"], fontSize=5.5))
        ]
        
        return elems