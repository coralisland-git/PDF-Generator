# -*- coding: utf-8 -*-
from reportlab_styles import styles, extend_style, extend_table_style, SignatureDocTemplate, SignatureRect
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Table, PageTemplate, Frame, Spacer
from reportlab.platypus.flowables import HRFlowable, PageBreak
import datetime
import io

try:
    import cStringIO
except ModuleNotFoundError:
    pass


def generate_bench_warrant(pdf_dict, title=None, author=None):
    report = BenchWarrantReport(title, author)
    try:
        buff = cStringIO.StringIO()
    except NameError:
        buff = None
    return report.create_report(pdf_dict, buff)


class BenchWarrantReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (6.35 * mm, 6.35 * mm)
        self.title = title
        self.author = author
        self.data = None

    def create_report(self, data_dict, buff=None):
        self.data = data_dict
        if not buff:
            buff = io.BytesIO()
        pages = [x for x in dir(self) if x.startswith("_page_")]
        story = []
        for page in pages:
            elems = getattr(self, page)()
            story.extend(elems)
            story.append(PageBreak())
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
        doc_t = SignatureDocTemplate(
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
        metadata = doc_t.build(story)
        buff.seek(0)
        return {
            "metadata": metadata,
            "document": buff
        }

    @staticmethod
    def _create_border_table(elems, width=None, border_outer=None, border_inner=None, padding=(0, 0)):
        border_outer = border_outer if border_outer else 0.5 * mm
        border_inner = border_inner if border_inner else 1.05 * mm
        border_spacing = border_inner / 2 + border_outer / 2 + border_outer
        border_spacer = Spacer(0, border_outer / 2)
        new_elems = [border_spacer]
        table_data = [[x] for x in elems]
        new_elems.append(
            Table(
                [
                    [None],
                    [
                        None,
                        Table(
                            [
                                [None],
                                [
                                    None,
                                    Table(
                                        [
                                            [
                                                Table(
                                                    table_data,
                                                    style=styles["rc-main-table"]
                                                )
                                            ]
                                        ],
                                        style=extend_table_style(styles["rc-main-table"], [
                                            ("OUTLINE", (0, 0), (-1, -1), border_outer, "black", "projecting"),
                                            ("TOPPADDING", (0, 0), (-1, -1), padding[1]),
                                            ("BOTTOMPADDING", (0, 0), (-1, -1), padding[1]),
                                            ("LEFTPADDING", (0, 0), (-1, -1), padding[0]),
                                            ("RIGHTPADDING", (0, 0), (-1, -1), padding[0]),
                                        ]),
                                    ),
                                    None
                                ],
                                [None]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("OUTLINE", (0, 0), (-1, -1), border_inner, "black", "projecting"),
                            ]),
                            colWidths=(border_spacing, None, border_spacing),
                            rowHeights=[border_spacing, None, border_spacing],
                        ),
                        None
                    ],
                    [None]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("OUTLINE", (0, 0), (-1, -1), border_outer, "black", "projecting"),
                ]),
                colWidths=(border_spacing, width, border_spacing),
                rowHeights=[border_spacing, None, border_spacing],
            )
        )
        new_elems.append(border_spacer)
        return new_elems

    def _page_1(self):
        table_width = 188 * mm
        border_outer = 0.5 * mm
        border_inner = 1.05 * mm
        trial_date_parts = self.data["trial_call_date"].split("/")
        trial_date_parts[0] = datetime.date(1900, int(trial_date_parts[0]), 1).strftime('%B')
        trial_date_parts[1] = int(trial_date_parts[1])
        order_date_parts = self.data["order_date"].split("/")
        order_date_parts[0] = datetime.date(1900, int(order_date_parts[0]), 1).strftime('%B')
        order_date_parts[1] = int(order_date_parts[1])
        date_suff = ["th", "st", "nd", "rd"]
        try:
            order_date_parts[1] = "%s%s" % (order_date_parts[1], date_suff[order_date_parts[1]])
        except IndexError:
            order_date_parts[1] = "%s%s" % (order_date_parts[1], date_suff[1])
        violation_tense = "" if len(self.data["violations"]) < 2 else "s"
        violation_text = ", ".join(
            ["%s %s" % (v["violation_section"], v["violation_description"]) for v in self.data["violations"]]
        )
        ps = extend_style(
            styles["rc-bw-main"],
            rightIndent=3.3 * mm,
            leading=styles["rc-bw-main"].fontSize * 2.3,
            splitLongWords=True
        )
        elems = [
            Paragraph("BENCH WARRANT", styles["rc-bw-doc-header"]),
            HRFlowable(width="98%", thickness=0.2 * mm, lineCap="butt", color="black"),
            Spacer(0, 4 * mm),
            Paragraph("<b>State of Georgia, Rockdale County</b>", styles["rc-bw-title"]),
            Spacer(0, 6.5 * mm),
            Paragraph("<b>%s</b>" % self.data["case_number"], extend_style(
                styles["rc-bw-title"],
                fontSize=styles["rc-bw-title"].fontSize - 3,
                alignment=TA_RIGHT,
                rightIndent=24 * mm
            )),
            Spacer(0, 5.5 * mm),
            Paragraph("To all and Singular the Sheriffs, Constables, and Coroners of said State – Greeting:", ps),
            Paragraph(
                "Whereas, <u>%s %s, %s</u> during the <u>%s</u> Term of the Magistrate Court of Rockdale County, the Court did call for trial, the case against <b><u>%s</u></b>, of <b><u>%s</u></b> for the offense%s of <b><u>%s</u></b>" % (
                    trial_date_parts[0], trial_date_parts[1], trial_date_parts[2], trial_date_parts[0],
                    self.data["defendant_name"],
                    self.data["defendant_address"], violation_tense, violation_text
                ),
                extend_style(ps, firstLineIndent=13 * mm, alignment=TA_JUSTIFY)
            ),
            Paragraph(
                "The said <b>ACCUSED</b>, having failed to appear and no excuse having been offered, pursuant to O.C.G.A. 15-10- 62(b), you and each of you are therefore commanded in the name of the State to apprehend the said Defendant, and in default of his giving bond and surety in the sum ordered on the back of this Warrant, to commit him/her to the common jail of said County, so as to secure his/her appearance in Rockdale Magistrate Court.",
                extend_style(
                    ps,
                    leading=styles["rc-bw-main"].fontSize * 1.72,
                    rightIndent=2 * mm,
                )
            ),
            Paragraph(
                "Given under my hand and seal this <u>%s</u> day of <u>%s</u>, <u>%s</u>." % (
                    order_date_parts[1], order_date_parts[0], order_date_parts[2]
                ),
                extend_style(ps, firstLineIndent=13 * mm)
            ),
            SignatureRect(59 * mm, 9 * mm, label="Magistrate Judge", leftIndent=85 * mm),
            HRFlowable(thickness=0.15 * mm, lineCap="butt", color="black", dash=[0, 84.75 * mm, 61 * mm]),
            Spacer(0, 2 * mm),
            Paragraph(
                "Chief Magistrate Judge Phinia Aten.",
                extend_style(ps, firstLineIndent=84 * mm)
            ),
            Spacer(0, 0.4 * mm),
        ]
        return self._create_border_table(elems, table_width, border_inner=border_inner, border_outer=border_outer,
                                         padding=(2.2 * mm, 0.5 * mm))

    def _page_2(self):
        table_width = 68.75 * mm
        border_outer = 0.25 * mm
        border_inner = 1.05 * mm
        addr_parts = self.data["defendant_address"].split(",")
        ps = extend_style(styles["rc-bw-main"], fontSize=12, leading=12, alignment=TA_CENTER)
        elems = [
            Spacer(0, 0.75 * mm),
            Paragraph("<b>BENCH WARRANT</b>", extend_style(styles["rc-bw-title"], fontSize=14, leading=14)),
            Spacer(0, 18.5 * mm),
            HRFlowable(width="100%", thickness=0.1 * mm, lineCap="butt", color="black"),
            Spacer(0, 1.6 * mm),
            Paragraph("<b>MAGISTRATE COURT</b>", extend_style(ps, fontSize=11, leading=11)),
            Spacer(0, 19 * mm),
            HRFlowable(width="100%", thickness=0.75 * mm, lineCap="butt", color="black"),
            Spacer(0, 1.6 * mm),
            Paragraph("<b>ROCKDALE COUNTY</b>", ps),
            Spacer(0, 6 * mm),
            Paragraph("<b>VS.</b>", ps),
            Spacer(0, 0.75 * mm),
            Paragraph("<b><u>%s</u></b>" % self.data["defendant_name"], ps),
            Spacer(0, 8.25 * mm),
            HRFlowable(width="100%", thickness=0.1 * mm, lineCap="butt", color="black"),
            Spacer(0, 6.6 * mm),
            Paragraph(
                "<b><u>%s<br />%s, %s</u></b>" % (addr_parts[0], addr_parts[1], addr_parts[2]),
                extend_style(ps, fontSize=12, leading=14.5)
            ),
            Spacer(0, 21 * mm),
            HRFlowable(width="100%", thickness=0.1 * mm, lineCap="butt", color="black"),
            Spacer(0, 4 * mm),
            HRFlowable(width="100%", thickness=0.1 * mm, lineCap="butt", color="black"),
            Spacer(0, 4.75 * mm),
            HRFlowable(width="100%", thickness=0.75 * mm, lineCap="butt", color="black"),
            Spacer(0, 1.9 * mm),
            Paragraph("<b>Sheriff take good bond in the sum of</b>", extend_style(ps, fontSize=11, leading=11)),
            Spacer(0, 5.5 * mm),
            Paragraph("<b>${:,.2f}</b>".format(self.data["bond_amount"]), extend_style(ps, fontSize=12, leading=12)),
            Spacer(0, 4 * mm),
            HRFlowable(width="100%", thickness=0.1 * mm, lineCap="butt", color="black"),
            Spacer(0, 28 * mm),
        ]
        return self._create_border_table(elems, table_width, border_inner=border_inner, border_outer=border_outer)

    def _page_3(self):
        table_width = 45.25 * mm
        ps_title = extend_style(styles["rc-bw-title"], fontSize=11, leading=12.65)
        ps_text = extend_style(styles["rc-bw-title"], fontSize=12, leading=13.8)
        sections = list()
        sections.append([
            Paragraph("<b>State Personal I.D.</b>", ps_title),
            Paragraph("<b>%s</b>" % self.data["defendant_state_id_number"], ps_text),
            Spacer(0, 3.5 * mm)
        ])
        sections.append([
            Paragraph("<b>Date of Birth</b>", ps_title),
            Paragraph("<b>%s</b>" % self.data["defendant_dob"], ps_text),
            Spacer(0, 0.75 * mm)
        ])
        sections.append([
            Spacer(0, 6.75 * mm),
        ])
        sections.append([
            Paragraph("<b>State Driver’s License</b>", ps_title),
            Paragraph("<b>%s</b>" % self.data["defendant_driver_license_number"], ps_text),
            Spacer(0, 6.75 * mm),
        ])
        sections.append([
            Paragraph("<b>Social Security No.</b>", ps_title),
            Paragraph("<b>%s</b>" % self.data["defendant_ssn"], ps_text),
            Spacer(0, 16.5 * mm),
        ])
        table_data = list()
        for section in sections:
            table_data.append([
                Table(
                    [[elem] for elem in section],
                    style=styles["rc-main-table"]
                )
            ])
        t1 = Table(
            table_data,
            style=extend_table_style(styles["rc-main-table"], [
                ("GRID", (0, 0), (-1, -1), 0.1 * mm, "black"),
                ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4 * mm),
                ("LEFTPADDING", (0, 0), (-1, -1), 0.1 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0.1 * mm),
            ]),
            colWidths=table_width
        )
        return [t1]
