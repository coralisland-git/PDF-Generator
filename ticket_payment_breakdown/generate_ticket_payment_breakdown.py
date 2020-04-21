import cStringIO

from common.signatures import *
from document_specific_styles import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT


def generate_ticket_payment_breakdown():
    cr = TPBReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)

class TPBReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (8.4 * mm, 6.4 * mm)
        self.sections = [            
            "section_1", 
            "section_2", 
            "section_3", 
            "section_4", 
            "section_5"
        ]
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

        def page_number(canv, doc):
            footer_table = Table(
                [
                    [
                        Paragraph("<b>07/18/2019 at 08:19 AM</b>", extend_style(styles['rc-aawp-main-content'], fontSize=8)),
                        Paragraph("<b>Page 1 of 1</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT, fontSize=8)),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEABOVE", (0, 0), (-1, -1), 0.1, "black"),
                    ("TOPPADDING", (0, 0), (-1, -1), .8 * mm),
                ]),
            )
            footer_table.wrapOn(canv, self.page_size[0] - 11.6*mm, 0)
            footer_table.drawOn(canv, 5.8*mm, 5.8*mm)

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

    def _section_section_1(self):
        receipt_table = [
            [
                Paragraph("<b>Receipt # Date</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Case #</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Name</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Charge</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Amount</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                Paragraph("<b>Pay Type</b>", styles['rc-aawp-main-content']),
            ]
        ]
        receipt_arr = [
            {
                "Receipt # Date": "70672 7/17/2019 00:00:00",
                "Case #": "E67593",
                "Name": "MOHAMED, AHMED JEMAL",
                "Charge": "VIOLATION OF TRAFFIC CONTROL DEVICE-1ST",
                "Amount": "178,00",
                "Pay Type": "Credit Card",
            },{
                "Receipt # Date": "70678 7/17/2019 00:00:00",
                "Case #": "E65114",
                "Name": "HUDES, JESSICA RACHEL",
                "Charge": "NO LICENSE ON <br /> PERSON-1ST",
                "Amount": "12,00",
                "Pay Type": "Credit Card",
            },{
                "Receipt # Date": "70679 7/17/2019 00:00:00",
                "Case #": "E65142",
                "Name": "SCHWARTZ, JACOB ERIN",
                "Charge": "EXPIRED OR NO LICENSE PLATE OR DECAL-1ST",
                "Amount": "126.00",
                "Pay Type": "Credit Card",
            },{
                "Receipt # Date": "70680 7/17/2019 00:00:00",
                "Case #": "E68159",
                "Name": "JACKSON, GARY JR",
                "Charge": "FAILURE TO STOP FOR STOP SIGN-1ST",
                "Amount": "178.00",
                "Pay Type": "Credit Card",
            },{
                "Receipt # Date": "70681 7/17/2019 00:00:00",
                "Case #": "E65299",
                "Name": "MITCHELL, JOSHUA CODY",
                "Charge": "MITCHELL, JOSHUA CODY",
                "Amount": "15.00",
                "Pay Type": "Credit Card",
            },{
                "Receipt # Date": "70682 7/17/2019 00:00:00",
                "Case #": "E67939",
                "Name": "KETA, SARAH MUTOMBO",
                "Charge": "EXPIRED OR NO LICENSE PLATE OR DECAL-1ST",
                "Amount": "126.00",
                "Pay Type": "Credit Card",
            },{
                "Receipt # Date": "70683 7/17/2019 00:00:00",
                "Case #": "E67940",
                "Name": "KETA, SARAH MUTOMBO",
                "Charge": "DRIVING WITH OBSTRUCTED LICENSE PLATE-1ST",
                "Amount": "178.00",
                "Pay Type": "Credit Card",
            }
        ]
        for idx, receipt in enumerate(receipt_arr):
            receipt_table.append(
                [
                    Paragraph(receipt["Receipt # Date"], extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                    Paragraph(receipt["Case #"], styles['rc-aawp-main-content']),
                    Paragraph(receipt["Name"], styles['rc-aawp-main-content']),
                    Paragraph(receipt["Charge"], styles['rc-aawp-main-content']),
                    Paragraph(receipt["Amount"], extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                    Paragraph(receipt["Pay Type"], styles['rc-aawp-main-content']),
                ]
            )
        elems = [
            Paragraph(
                """
                <b>ONLINE <br />
                Reporting Date From 07/17/2019 To 07/17/2019 </b>
                """,
                styles["rc-doc-header"]
            ),
            Spacer(0, .4 * mm),
            Table(
                receipt_table,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (0, 0), (-1, -1), 0.5, "black"),
                    ("TOPPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("LEFTPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), .8 * mm),
                ]),
                colWidths=(43*mm, 24*mm, 48*mm, 50*mm, 15*mm, 20*mm)
            ),
            Spacer(0, .8 * mm),
            Table(
                [
                    [   
                        Paragraph("<b>Cash</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Credit Card</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("813.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Work</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("813.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                    ],[   
                        Paragraph("<b>Check</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Cash Bond (CC)</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Jail</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ],[   
                        Paragraph("<b>Money Order</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>ECA</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Writeoff</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ],[   
                        Paragraph("<b>Cash Bond (Cash)</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Total</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("813.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Refund</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ],[   
                        Paragraph("<b>Total</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Cash Bond App/For</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Total</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),                    
                    ("TOPPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("LEFTPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), .8 * mm),
                ]),
                colWidths=(30*mm, 18*mm, 33*mm, 20*mm, 25*mm, 23*mm, 47*mm)
            ),
            PageBreak()
        ]
        return elems

    def _section_section_2(self):
        receipt_table = [
            [
                Paragraph("<b>Receipt # Date</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Case #</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Name</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Charge</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Amount</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                Paragraph("<b>Pay Type</b>", styles['rc-aawp-main-content']),
            ]
        ]
        receipt_arr = [
            {
                "Receipt # Date": "70667 7/17/2019 00:00:00",
                "Case #": "E62062",
                "Name": "YANSUNU, SAMUEL J",
                "Charge": "UNLAWFUL USE OF WIRELESS DEVICE-1ST",
                "Amount": "50.00",
                "Pay Type": "Credit Card",
            }
        ]
        for idx, receipt in enumerate(receipt_arr):
            receipt_table.append(
                [
                    Paragraph(receipt["Receipt # Date"], extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                    Paragraph(receipt["Case #"], styles['rc-aawp-main-content']),
                    Paragraph(receipt["Name"], styles['rc-aawp-main-content']),
                    Paragraph(receipt["Charge"], styles['rc-aawp-main-content']),
                    Paragraph(receipt["Amount"], extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                    Paragraph(receipt["Pay Type"], styles['rc-aawp-main-content']),
                ]
            )
        elems = [
            Paragraph(
                """
                <b>MYAP <br />
                Reporting Date From 07/17/2019 To 07/17/2019 </b>
                """,
                styles["rc-doc-header"]
            ),
            Spacer(0, .4 * mm),
            Table(
                receipt_table,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (0, 0), (-1, -1), 0.5, "black"),
                    ("TOPPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("LEFTPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), .8 * mm),
                ]),
                colWidths=(43*mm, 24*mm, 48*mm, 50*mm, 15*mm, 20*mm)
            ),
            Spacer(0, .8 * mm),
            Table(
                [
                    [   
                        Paragraph("<b>Cash</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Credit Card</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("50.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Work</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("50.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                    ],[   
                        Paragraph("<b>Check</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Cash Bond (CC)</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Jail</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ],[   
                        Paragraph("<b>Money Order</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>ECA</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Writeoff</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ],[   
                        Paragraph("<b>Cash Bond (Cash)</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Total</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("50.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Refund</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ],[   
                        Paragraph("<b>Total</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Cash Bond App/For</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Total</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),                    
                    ("TOPPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("LEFTPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), .8 * mm),
                ]),
                colWidths=(30*mm, 18*mm, 33*mm, 20*mm, 25*mm, 23*mm, 47*mm)
            ),
            PageBreak()
        ]
        return elems

    def _section_section_3(self):
        receipt_table = [
            [
                Paragraph("<b>Receipt # Date</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Case #</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Name</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Charge</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Amount</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                Paragraph("<b>Pay Type</b>", styles['rc-aawp-main-content']),
            ]
        ]
        receipt_arr = [
            {
                "Receipt # Date": "70673 7/17/2019 00:00:00",
                "Case #": "E64527",
                "Name": "LOPEZ, JOSHUA NOELITO",
                "Charge": "UNLAWFUL USE OF WIRELESS DEVICE-1ST",
                "Amount": "50.00",
                "Pay Type": "CB App/For",
            }
        ]
        for idx, receipt in enumerate(receipt_arr):
            receipt_table.append(
                [
                    Paragraph(receipt["Receipt # Date"], extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                    Paragraph(receipt["Case #"], styles['rc-aawp-main-content']),
                    Paragraph(receipt["Name"], styles['rc-aawp-main-content']),
                    Paragraph(receipt["Charge"], styles['rc-aawp-main-content']),
                    Paragraph(receipt["Amount"], extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                    Paragraph(receipt["Pay Type"], styles['rc-aawp-main-content']),
                ]
            )
        elems = [
            Paragraph(
                """
                <b>ALAU <br />
                Reporting Date From 07/17/2019 To 07/17/2019 </b>
                """,
                styles["rc-doc-header"]
            ),
            Spacer(0, .4 * mm),
            Table(
                receipt_table,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (0, 0), (-1, -1), 0.5, "black"),
                    ("TOPPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("LEFTPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), .8 * mm),
                ]),
                colWidths=(43*mm, 24*mm, 48*mm, 50*mm, 15*mm, 20*mm)
            ),
            Spacer(0, .8 * mm),
            Table(
                [
                    [   
                        Paragraph("<b>Cash</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Credit Card</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Work</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("50.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                    ],[   
                        Paragraph("<b>Check</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Cash Bond (CC)</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Jail</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ],[   
                        Paragraph("<b>Money Order</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>ECA</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Writeoff</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ],[   
                        Paragraph("<b>Cash Bond (Cash)</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Total</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Refund</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ],[   
                        Paragraph("<b>Total</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Cash Bond App/For</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("50.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Total</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),                    
                    ("TOPPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("LEFTPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), .8 * mm),
                ]),
                colWidths=(30*mm, 18*mm, 33*mm, 20*mm, 25*mm, 23*mm, 47*mm)
            ),
            PageBreak()
        ]
        return elems

    def _section_section_4(self):
        receipt_table = [
            [
                Paragraph("<b>Receipt # Date</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Case #</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Name</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Charge</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Amount</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                Paragraph("<b>Pay Type</b>", styles['rc-aawp-main-content']),
            ]
        ]
        receipt_arr = [
            {
                "Receipt # Date": "70667 7/17/2019 00:00:00",
                "Case #": "E62062",
                "Name": "YANSUNU. SAMUEL J",
                "Charge": "UNLAWFUL USE OF WIRELESS DEVICE-1ST",
                "Amount": "50.00",
                "Pay Type": "Credit Card",
            },{
                "Receipt # Date": "70672 7/17/2019 00:00:00",
                "Case #": "E67593",
                "Name": "MOHAMED, AI MED JEMAL",
                "Charge": "VIOLATION OF TRAFFIC CONTROL DEVICE-1ST",
                "Amount": "178.00",
                "Pay Type": "Credit Card",
            },{
                "Receipt # Date": "70673 7/17/2019 00:00:00",
                "Case #": "E64527",
                "Name": "LOPEZ, JOSHUA NOELITO",
                "Charge": "UNLAWFUL USE OF WIRELESS DEVICE-1ST",
                "Amount": "50.00",
                "Pay Type": "CB App/For",
            },{
                "Receipt # Date": "70674 7117/2019 00:00:00",
                "Case #": "E68163",
                "Name": "OLOSUNDE, FEMI ABIOYE",
                "Charge": "TAG LIGHT REQUIRED-1ST",
                "Amount": "20.00",
                "Pay Type": "Credit Card",
            },{
                "Receipt # Date": "70674 7117/2019 00:00:00",
                "Case #": "E68163",
                "Name": "OLOSUNDE, FEMI ABIOYE",
                "Charge": "TAG LIGHT REQUIRED-1ST",
                "Amount": "30.00",
                "Pay Type": "Cash",
            },{
                "Receipt # Date": "70678 7/17/2019 00:00:00",
                "Case #": "E65114",
                "Name": "NUDES, JESSICA RACHEL",
                "Charge": "NO LICENSE ON PERSON-1ST",
                "Amount": "12.00",
                "Pay Type": "Credit Card",
            },{
                "Receipt # Date": "70679 7/17/2019 00:00:00",
                "Case #": "E65142",
                "Name": "SCHWARTZ, JACOB ERIN",
                "Charge": "EXPIRED OR NO LICENSE PLATE OR DECAL-1ST",
                "Amount": "126.00",
                "Pay Type": "Credit Card",
            },{
                "Receipt # Date": "70680 7/17/2019 00:00:00",
                "Case #": "E68159",
                "Name": "JACKSON, GARY JR",
                "Charge": "FAILURE TO STOP FOR STOP SIGN-1ST",
                "Amount": "178.00",
                "Pay Type": "Credit Card",
            },{
                "Receipt # Date": "70681 7/17/2019 00:00:00",
                "Case #": "E65299",
                "Name": "MITCHELL, JOSHUA CODY",
                "Charge": "NO SEATBELT-1ST",
                "Amount": "15.00",
                "Pay Type": "Credit Card",
            },{
                "Receipt # Date": "70682 7/17/2019 00:00:00",
                "Case #": "E67939",
                "Name": "KETA, SARAH MUTOMBO",
                "Charge": "EXPIRED OR NO LICENSE PLATE OR DECAL-1ST",
                "Amount": "126.00",
                "Pay Type": "Credit Card",
            },{
                "Receipt # Date": "70683 7/17/2019 00:00:00",
                "Case #": "E67940",
                "Name": "KETA, SARAH MUTOMBO",
                "Charge": "DRIVING WITH OBSTRUCTED LICENSE PLATE-1ST",
                "Amount": "178.00",
                "Pay Type": "Credit Card",
            }
        ]
        for idx, receipt in enumerate(receipt_arr):
            receipt_table.append(
                [
                    Paragraph(receipt["Receipt # Date"], extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                    Paragraph(receipt["Case #"], styles['rc-aawp-main-content']),
                    Paragraph(receipt["Name"], styles['rc-aawp-main-content']),
                    Paragraph(receipt["Charge"], styles['rc-aawp-main-content']),
                    Paragraph(receipt["Amount"], extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                    Paragraph(receipt["Pay Type"], styles['rc-aawp-main-content']),
                ]
            )
        elems = [
            Paragraph(
                """
                <b>***ALL CLERKS *** <br />
                Reporting Date From 07/17/2019 To 07/17/2019 </b>
                """,
                styles["rc-doc-header"]
            ),
            Spacer(0, .4 * mm),
            Table(
                receipt_table,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (0, 0), (-1, -1), 0.5, "black"),
                    ("TOPPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("LEFTPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), .8 * mm),
                ]),
                colWidths=(43*mm, 24*mm, 48*mm, 50*mm, 15*mm, 20*mm)
            ),
            Spacer(0, .8 * mm),
            Table(
                [
                    [   
                        Paragraph("<b>Cash</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("30.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Credit Card</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("883.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Work</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("963.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                    ],[   
                        Paragraph("<b>Check</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Cash Bond (CC)</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Jail</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ],[   
                        Paragraph("<b>Money Order</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>ECA</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Writeoff</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ],[   
                        Paragraph("<b>Cash Bond (Cash)</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Total</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("883.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Refund</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ],[   
                        Paragraph("<b>Total</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("30.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Cash Bond App/For</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("50.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Total</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),                    
                    ("TOPPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("LEFTPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), .8 * mm),
                ]),
                colWidths=(30*mm, 18*mm, 33*mm, 20*mm, 25*mm, 23*mm, 47*mm)
            ),
            PageBreak()
        ]
        return elems

    def _section_section_5(self):
        receipt_table = [
            [
                Paragraph("<b>Receipt # Date</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Case #</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Name</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Charge</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Amount</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                Paragraph("<b>Pay Type</b>", styles['rc-aawp-main-content']),
            ]
        ]
        receipt_arr = [
            {
                "Receipt # Date": "70674 7/17/2019 00:00:00",
                "Case #": "E68163",
                "Name": "OLOSUNDE. FEMI ABIOYE",
                "Charge": "TAG LIGHT REQUIRED-1ST",
                "Amount": "20.00",
                "Pay Type": "Credit Card",
            },{
                "Receipt # Date": "70674 7/17/2019 00:00:00",
                "Case #": "E68163",
                "Name": "OLOSUNDE. FEMI ABIOYE",
                "Charge": "TAG LIGHT REQUIRED-1ST",
                "Amount": "30.00",
                "Pay Type": "Cash",
            }
        ]
        for idx, receipt in enumerate(receipt_arr):
            receipt_table.append(
                [
                    Paragraph(receipt["Receipt # Date"], extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                    Paragraph(receipt["Case #"], styles['rc-aawp-main-content']),
                    Paragraph(receipt["Name"], styles['rc-aawp-main-content']),
                    Paragraph(receipt["Charge"], styles['rc-aawp-main-content']),
                    Paragraph(receipt["Amount"], extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                    Paragraph(receipt["Pay Type"], styles['rc-aawp-main-content']),
                ]
            )
        elems = [
            Paragraph(
                """
                <b>STHARRISON <br />
                Reporting Date From 07/17/2019 To 07/17/2019 </b>
                """,
                styles["rc-doc-header"]
            ),
            Spacer(0, .4 * mm),
            Table(
                receipt_table,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (0, 0), (-1, -1), 0.5, "black"),
                    ("TOPPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("LEFTPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), .8 * mm),
                ]),
                colWidths=(43*mm, 24*mm, 48*mm, 50*mm, 15*mm, 20*mm)
            ),
            Spacer(0, .8 * mm),
            Table(
                [
                    [   
                        Paragraph("<b>Cash</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("30.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Credit Card</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("20.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Work</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("50.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                    ],[   
                        Paragraph("<b>Check</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Cash Bond (CC)</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Jail</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ],[   
                        Paragraph("<b>Money Order</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>ECA</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Writeoff</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ],[   
                        Paragraph("<b>Cash Bond (Cash)</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Total</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("20.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Refund</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ],[   
                        Paragraph("<b>Total</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("30.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Cash Bond App/For</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("<b>Total</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),                    
                    ("TOPPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("LEFTPADDING", (0, 0), (-1, -1), .8 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), .8 * mm),
                ]),
                colWidths=(30*mm, 18*mm, 33*mm, 20*mm, 25*mm, 23*mm, 47*mm)
            ),
            PageBreak()
        ]
        return elems