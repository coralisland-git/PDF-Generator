import cStringIO

from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Flowable, Paragraph, Table, Spacer

from document_specific_styles import *

class XBox(Flowable):
    def __init__(self, size, checked=None):
        Flowable.__init__(self)
        self.width = size
        self.height = size
        self.size = size
        self.checked = checked

    def draw(self):
        self.canv.saveState()
        self.canv.setLineWidth(0.11 * self.size)
        self.canv.rect(0, 0, self.width, self.height)
        if self.checked is True:
            self.check()
        self.canv.restoreState()

    def check(self):
        self.canv.setFont('Times-Bold', self.size * 0.95)
        to = self.canv.beginText(self.width * 0.13, self.height * 0.155)
        to.textLine("X")
        self.canv.drawText(to)


def generate_detention_order():
    buff = cStringIO.StringIO()
    doc = BaseDocTemplate(buff, pagesize=letter)
    f = Frame(gutters[0] * 1.5, gutters[2], usable_width-gutters[0], usable_height, showBoundary=0)

    story = []
    story.append(Spacer(0, 4 * mm))
    table = bottom_table()
    story.append(table)

    main_template = PageTemplate(id="main_template", frames=[f])
    doc.addPageTemplates([main_template])
    doc.build(story)
    del doc

    buff.seek(0)
    return buff

def bottom_table():
    data = [
        [   #1
            Paragraph('79,206.22 BASE - FINES', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('97,665.86 TOTAL DISBURSEMENTS',
                      style=extend_style(text_style, alignment=TA_CENTER))
        ],
        [   #2
            Paragraph('18,459.04 STATE SURCHARGES ONLY', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('-25664.02 TOTAL DISBURSEMENTS',
                      style=extend_style(text_style, alignment=TA_CENTER))
        ],
        [   #3
            Paragraph('00.0 PROC - FEES',
                      style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('0.00 PROC - FEES',
                      style=extend_style(text_style, alignment=TA_CENTER))
        ],
        [   #4
            Paragraph('16188.73 OTHER CHARGES',
                      style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('-16188.73 OTHER CHARGES',
                      style=extend_style(text_style, alignment=TA_CENTER))
        ],
        [   #5
            Paragraph('0.00 ADM FEES',
                      style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('0.00 ADM FEES',
                      style=extend_style(text_style, alignment=TA_CENTER))
        ],
        [   #6
            Paragraph('0.00 TECH FEES',
                      style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('0.00 TECH FEES',
                      style=extend_style(text_style, alignment=TA_CENTER))
        ],
        [
            #7
            Paragraph('<b>97,665.86 TOTAL DISBURSEMENTS</b>',
                      style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>72001.84 NET DISBURSEMENTS</b>',
                      style=extend_style(text_style, alignment=TA_CENTER))
        ]
    ]
    table = Table(
        data,
        colWidths=(50 * mm, 50 * mm),
        rowHeights=10*mm
    )
    table.setStyle(styles['iv-main-table'])
    return table


def consolidated_report_data():
    data = [
        [  # 0
            Paragraph('Report Month: August&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Report Year: 2019',
                      style=text_style),
            '',
            '',

            Paragraph('Report Date: {}. {}, {}'.format('Sept', '16', '2019'), style=text_style),
            '',

            Paragraph('County: {}'.format('ROCKDALE'), style=text_style),
            ''
        ],
        [  # 1
            Paragraph('Clerk/Court Officer Filing Report: HON. PHINIA ATEN', style=text_style),
            '',
            '',
            Paragraph('Phone: 770-278-7799', style=text_style),
            '',
            Paragraph('ORI: 122033J', style=text_style)
        ],
        [  # 2
            '', '',
            Paragraph('<b>(1)</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>(2)</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>(3)</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>(4)</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>(5)</b>', style=extend_style(text_style, alignment=TA_CENTER))
        ],
        [  # 3
            '', '',
            Paragraph('<b>No. of Cases</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>Amount of Original Fine and/or Bond Forfeiture</b>',
                      style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>Total Amount of Fines and/or Bond Forfeitures</b>',
                      style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>Computation of Amount Collected</b>',
                      style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>Amount Collected</b>', style=extend_style(text_style, alignment=TA_CENTER))
        ],
        [  # 4
            Paragraph('SECTION 1 - CRIMINAL', style=extend_style(text_style, textColor=colors.white)),
            '', '', '', '', '', ''
        ],
        [  # 5
            Paragraph('1', style=text_style),
            Paragraph('<b>POPIDF-A (f/k/a POPTF)</b> (OCGA 15-21-73(a)(1)(A))', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$1 - $499.99', style=text_style),
            Paragraph('$0.00', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style)
        ],
        [  # 6
            '', '',
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$50 x column (1)', style=text_style),
            Paragraph('', style=text_style)
        ],
        [  # 7
            '', '',
            Paragraph('20', style=text_style),
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$357.50', style=text_style)
        ],
        [  # 8
            '',
            Paragraph('<b>POPIDF-A (f/k/a POPTF)</b> (OCGA 15-21-73(a)(2)(A) ) - <b>Bond Forfeitures</b>',
                      style=text_style),
            Paragraph('', style=text_style),
            Paragraph('Less than $1000', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('10% x Column (3)', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],
        [  # 9
            '', '',
            Paragraph('', style=text_style),
            Paragraph('Greater than $1000', style=text_style),
            Paragraph('$0.00', style=text_style),
            Paragraph('$100', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],
        [  # 10
            Paragraph('2', style=text_style),
            Paragraph(
                '<b>Georgia Crime Victims Emergency Fund</b> (OCGA 15-21-112 for conviction of OCGA 40-6-391 (DUI of alcohol/drugs))',
                style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$26', style=text_style),
            Paragraph('$0.00', style=text_style),
            Paragraph('Column (1) x $26 for July 1, 2004 or later offenses', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],
        [  # 11
            '', '',
            Paragraph('', style=text_style),
            Paragraph('$25', style=text_style),
            Paragraph('$0.00', style=text_style),
            Paragraph('Column (1) x $25 for pre July 1, 2004 offenses', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],
        [  # 12
            '', '',
            Paragraph('', style=text_style),
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [  # 13
            Paragraph('3', style=text_style),
            Paragraph('<b>Brain and Spinal Injury Trust Fund</b> (OCGA 15-21-149 and 15-21-151)', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('Full Payments', style=text_style),
            Paragraph('$0.00', style=text_style),
            Paragraph('10% x Column (3)', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [  # 14
            '', '',
            Paragraph('', style=text_style),
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [  # 15
            Paragraph('4', style=text_style),
            Paragraph('<b>Crime Lab Fee</b> (OCGA 42-8-34)', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('Felony', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$50 x column (1)', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [  # 16
            '', '',
            Paragraph('', style=text_style),
            Paragraph('Misdemeanor', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$25 x column (1)', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [  # 17
            '', '',
            Paragraph('', style=text_style),
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [  # 18
            Paragraph('5', style=text_style),
            Paragraph('<b>Driver Education and Training Fund</b> (OCGA 15-21-179)', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('Full Payments', style=text_style),
            Paragraph('$0.00', style=text_style),
            Paragraph('1.5% of column (3) for May 6, 2013 or later offenses', style=text_style),
            Paragraph('$0.00', style=text_style),
        ],

        [  # 19
            '', '',
            Paragraph('', style=text_style),
            Paragraph('Full Payments', style=text_style),
            Paragraph('$0.00', style=text_style),
            Paragraph('5% of column (3) for pre May 6, 2013 offenses', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [  # 20
            '', '',
            Paragraph('', style=text_style),
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$0.00', style=text_style),
        ],

        [  # 21
            Paragraph('SECTION 2 - INDIGENT DEFENSE', style=extend_style(text_style, textColor=colors.white)),
            '', '', '', '', '', ''
        ],

        [  # 22
            Paragraph('6', style=text_style),
            Paragraph('<b>Civil Action Surcharges</b> (OCGA 15-21A-6)', style=text_style),
            Paragraph('277', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$15 x column (1)', style=text_style),
            Paragraph('$4155.00', style=text_style)
        ],

        [  # 23
            Paragraph('7', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('Full Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('10% x column (3)', style=text_style),
            Paragraph('', style=text_style)
        ],

        [  # 24
            '',
            Paragraph('', style=text_style),
            Paragraph('21', style=text_style),
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('365.20', style=text_style)
        ],

        [  # 25
            '',
            Paragraph('<b>POPIDF-B</b> (OCGA 15-21-73 (a)(2)(B)) - <b>Bond Forfeitures</b>', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('Less than $1000', style=text_style),
            Paragraph('$0.00', style=text_style),
            Paragraph('10% x Column (3)', style=text_style),
            Paragraph('$0', style=text_style)
        ],

        [  # 26
            '',
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('Greater than $1000', style=text_style),
            Paragraph('$0.00', style=text_style),
            Paragraph('$100', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [  # 27
            Paragraph('8', style=text_style),
            Paragraph('<b>Safe Harbor Fund</b> (OCGA 15-21-208)', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$2500 x column (1)', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [  # 28
            Paragraph('9', style=text_style),
            Paragraph('<b>State Indemnification Fund</b> (OCGA 16-5-21(c), 16-5-24(c), 16-10-24)',
                      style=text_style),
            Paragraph('', style=text_style),
            Paragraph('Full Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$300 or $2000 x column (1)', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [  # 29
            '', '',
            Paragraph('', style=text_style),
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [  # 30
            Paragraph('GRAND TOTAL OF ALL COLLECTIONS', style=extend_style(text_style, textColor=colors.white)),
            '', '', '', '', '',
            Paragraph('$4877.70', style=text_style)
        ]
    ]
    table = Table(
        data,
        colWidths=(10 * mm, 55 * mm, None, 30 * mm, 25 * mm, 45 * mm, None),
        rowHeights=_get_row_heights()
    )
    table.setStyle(extend_table_style(
        styles['iv-main-table'],
        [
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
    )
    )
    return table

def _get_row_heights():
    ROW_HEIGHT = 6 * mm
    row_heights = [ROW_HEIGHT] * 31
    row_heights[3] = 15 * mm
    row_heights[4] = 4 * mm
    row_heights[10] = 9 * mm
    row_heights[11] = 9 * mm
    row_heights[18] = 9 * mm
    row_heights[19] = 9 * mm
    row_heights[21] = 4 * mm
    row_heights[22] = 9 * mm
    row_heights[27] = 9 * mm
    row_heights[30] = 4 * mm
    return row_heights
