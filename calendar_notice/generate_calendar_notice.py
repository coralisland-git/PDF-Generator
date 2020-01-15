# -*- coding: utf-8 -*-
import cStringIO
import datetime
from reportlab.platypus.flowables import HRFlowable, PageBreak
from document_specific_styles import *


def generate_calendar_notice(title=None, author=None):
    cr = CNReport(title, author)
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class CNReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (23.5 * mm, 12.4 * mm)
        self.sections = ["header", "section_1"]
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

    def _section_header(self):
        elems = list()
        elems.append(Spacer(0, 9.8 * mm))
        elems.append(
            Paragraph(
                "MAGISTRATE COURT OF ROCKDALE COUNTY",
                styles["rc-doc-header"]
            )
        )
        elems.append(
            Paragraph(
                """
                945 Court Street, Conyers, Georgia 30012 (Offices)<br />
                948 Bank Street, Conyers, Georgia 30012 (Courtroom)<br />
                PO Box 289, Conyers, Georgia 30012 (Mailing Address)<br />
                (770) 278-7800 (Telephone)
                """, 
                styles['note']
            )
        )        
        elems = elems + [
            Paragraph(
                "<u>ORDINANCE TRIAL CALENDAR NOTICE</u>",
                extend_style(styles["rc-header"], spaceBefore=10)
            )
        ]
        elems.append(Spacer(0, 5 * mm))
        elems.append(
            Table(
                [
                    [
                        Paragraph("<b>To:</b>", extend_style(styles["rc-main-rmt-addr"], alignment=TA_RIGHT)),
                        Paragraph(
                            """
                            <b>Daizah Vigay<br />
                            2524 Lake Capri Drive<br />
                            Conyers GA 30012</b>
                            """,
                            extend_style(styles["rc-main-rmt-addr"])
                        )
                    ]
                ],
                colWidths=(25 * mm, 173 * mm),
                style=(
                    ('VALIGN', (0, 0), (0, 0), 'TOP'),
                )
            )
        )
        return elems

    def _section_section_1(self):        
        elems = [
            Paragraph(
                "Rockdale County vs.Daizah Vigay Case No. 2019-ORD-0142",
                extend_style(styles["rc-aawp-main-content"],  spaceBefore=10)
            ),
        ]
        elems.append(Spacer(0, 3 * mm))
        elems += [
            Paragraph(
                """
                The Defendant is commanded to appear on December 03, 2019 at 8:30 AM, before the
                Honorable Phinia Aten, in the Magistrate Courtroom, 948 Bank Street, Conyers, Georgia 30012,
                to announce your readiness for trial. It is mandatory for all defendants and their attorneys to be
                present for calendar call on this date. If the Defendant wishes, an opportunity to discuss
                resolution of the case with the County Attorney will be afforded to the Defendant and/or the
                Defendant’s attorney on the court date. If you are the Defendant’s bond surety, this Notice has
                been sent to you to advise that: (1) it is your responsibility to secure the Defendant’s court
                attendance as commanded; and (2) the Defendant may seek to enter a cash bond forfeiture as a
                resolution of the case during the Defendant’s discussion of possible resolutions with the County
                Attorney. If you have an objection to a cash bond forfeiture, you must state your objection
                during the calendar call. You may contact the Magistrate Court Clerk’s Office for further
                information at (770) 278-7800. FAILURE OF THE DEFENDANT TO APPEAR WILL
                RESULT IN THE ISSUANCE OF A BENCH WARRANT.
                <br />SIGNED and MAILED on this the 4th day of December, 2019.""",
                styles["rc-aawp-main-content"]
            ),
        ]
        elems.append(Spacer(0, 10 * mm))        
        elems.append(
            HRFlowable(thickness=0.15 * mm, lineCap="butt", color="black", dash=[0, 61 * mm, 94 * mm])
        )
        elems.append(
            Paragraph(
                "Clerk or Judicial Assistant",
                extend_style(styles["body"], firstLineIndent=72 * mm, leading=10)
            )
        )
        elems.append(
            Paragraph(
                "-" * 102,
                extend_style(styles["rc-aawp-main-content"], leading=15)
            )
        )
        elems.append(
            Paragraph(
                "<u>NOTICE TO ALL PARTIES REGARDING PROPER COURTROOM CONDUCT</u>",
                extend_style(styles["rc-header"], fontSize=10)
            )
        )
        elems.append(
            Paragraph(
                """
                -<b> &nbsp;PROPER ATTIRE  </b><br />
                -<b> &nbsp;CHILDREN MUST BEHAVE </b><br />
                -<b> &nbsp;NO TALKING, PROFANITY OR OTHER DISRUPTIVE BEHAVIOR </b><br />
                -<b> &nbsp;NO ELECTRONIC DEVICES ARE PERMITTED </b>(INCLUDING BUT NOT LIMITED TO <br />
                - &nbsp;CELL PHONES, TABLETS, LAPTOP COMPUTERS, CAMERAS AND AUDIO/VISUAL <br />                   
                """,
                extend_style(styles["rc-footer"], spaceBefore=10)
            ),
        )
        elems.append(
          Paragraph(
                "RECORDERS) WITHOUT EXPRESS PERMISSION OF THE COURT <br />",
                extend_style(styles["rc-footer"], leftIndent=17 * mm)
            ),
        )
        elems.append(
          Paragraph(
                "-<b> &nbsp;WILLFUL VIOLATIONS MAY RESULT IN A CONTEMPT OF COURT CITATION </b><br />",
                styles["rc-footer"]
            ),
        )

        return elems