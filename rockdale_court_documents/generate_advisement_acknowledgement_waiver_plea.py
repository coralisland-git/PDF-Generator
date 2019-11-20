from reportlab_styles import (
    styles, extend_style, extend_table_style, SignatureDocTemplate, SignatureRect, SignatureDatetimeRect
)
import cStringIO
import io
import datetime
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Flowable, Paragraph, Table, Spacer


def generate_advisement_acknowledgement_waiver_plea(pdf_dict, title=None, author=None):
    cr = AAWPReport(title, author)
    buff = cStringIO.StringIO()
    return cr.create_report(pdf_dict, buff)


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


class AAWPReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (23.5 * mm, 12.4 * mm)
        self.sections = ["header", "section_1", "section_2", "section_3", "section_4"]
        self.title = title
        self.author = author
        self.data = None

    def create_report(self, data_dict, buff=None):
        def get_method(section):
            try:
                method = getattr(self, "_section_" + section)
            except AttributeError:
                raise Exception("Section method not found: " + section)
            return method

        self.data = data_dict
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

    def _section_header(self):
        elems = list()
        elems.append(
            Paragraph(
                "IN THE MAGISTRATE COURT OF ROCKDALE COUNTY<br />STATE OF GEORGIA",
                style=styles["rc-doc-header"]
            )
        )
        elems.append(Spacer(0, 9.8 * mm))
        elems.append(
            Table(
                [
                    [
                        Table(
                            [
                                [Paragraph("ROCKDALE COUNTY, GEORGIA",
                                           extend_style(styles["rc-header"], alignment=TA_LEFT))],
                                [Paragraph("vs.", styles["rc-aawp-main"])],
                                [Paragraph("%s" % self.data["defendant_name"], styles["rc-aawp-main"])],
                                [Paragraph("Defendant.", styles["rc-aawp-main"])],
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("LINEBELOW", (0, 2), (0, 2), 0.7, "black"),
                                ("TOPPADDING", (0, 2), (0, 2), 0.5 * mm),
                                ("LEFTPADDING", (0, 2), (0, 2), 2 * mm),
                                ("TOPPADDING", (0, 2), (0, 2), 1 * mm),
                                ("TOPPADDING", (0, 3), (0, 3), 4 * mm),
                                ("LEFTPADDING", (0, 3), (0, 3), 5.3 * mm),
                            ]),
                            colWidths=72.9 * mm,
                        ),
                        Table(
                            [
                                [
                                    Paragraph("Ordinance Case No.", styles["rc-aawp-main"]),
                                    None,
                                    Paragraph("%s" % self.data["case_number"], styles["rc-aawp-main"]),
                                ],
                                [
                                    Paragraph("Citation No(s).", styles["rc-aawp-main"]),
                                ],
                                [
                                    None,
                                    Paragraph("%s" % ', '.join(self.data["citation_numbers"]), styles["rc-aawp-main"]),
                                ],
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("LINEBELOW", (2, 0), (2, 0), 0.5, "black"),
                                ("LINEBELOW", (1, 2), (-1, 2), 0.7, "black"),
                                ("SPAN", (0, 0), (1, 0)),
                                ("SPAN", (0, 1), (1, 1)),
                                ("SPAN", (1, 2), (2, 2)),
                                ("TOPPADDING", (0, 2), (0, 2), 1.6 * mm),
                                ("LEFTPADDING", (2, 0), (2, 0), 2 * mm),
                                ("LEFTPADDING", (1, 2), (1, 2), 2 * mm),

                            ]),
                            colWidths=(1.6 * mm, 34 * mm, 38.9 * mm)
                        ),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEAFTER", (0, 0), (0, -1), 2.25, "black", "butt"),
                    ("LEFTPADDING", (0, 0), (0, -1), 1.8 * mm),
                    ("LEFTPADDING", (1, 0), (1, -1), 4.8 * mm),
                ]),
                colWidths=84.3 * mm,
                rowHeights=35 * mm
            )
        )
        elems.append(Spacer(0, 4 * mm))
        elems = elems + [
            Paragraph(
                "<u>ORDINANCE ADVISEMENT, ACKNOWLEDGEMENTOF RIGHTS,<br />WAIVER AND PLEA OF GUILTY OR NO CONTEST FORM</u>",
                styles["rc-header"]
            ),
            Spacer(0, 5.2 * mm),
            Table(
                [
                    [
                        Paragraph(
                            "Completion of this form is necessary if you intend to plead guilty or no contest to the county ordinance citations against you in this case. Please read the form carefully and sign the form only if you understand its terms and statements and you wish for the Judge to accept your plea, sentence you and close your ordinance case without neither a jury or bench trial. If you have any questions about your case or the information on this form, please consult your attorney before signing it and submission as the Judge, county prosecutor, citing officers, interpreter and court clerks cannot give legal advice.",
                            styles["rc-aawp-main"]
                        )
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LEFTPADDING", (0, 0), (-1, -1), 1.9 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1.9 * mm),
                ]),
            )
        ]
        return elems

    def _section_section_1(self):
        elems = list()
        elems = elems + [
            Paragraph(
                "I.&nbsp;&nbsp;&nbsp;PLEA SECTION",
                style=styles["rc-section-header"]
            ),
            Table(
                [
                    [
                        Paragraph(
                            "I am the named defendant in this case, and I understand that Rockdale County is prosecuting me for the following county ordinance violations in this case. I am pleading guilty or no contest to these violations. My plea is entered voluntarily and knowingly; without anyone making threats; without anyone using force against me; and without any promises; to induce my plea. A factual basis for this plea exists and I understand the nature of my violations. I am not under the influence of any alcohol, medication or any other substance. Below, I have provided my true date of birth, the highest level of education that I have received, and information about my ability to understand the English spoken and written language.",
                            styles["rc-aawp-main"]
                        )
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LEFTPADDING", (0, 0), (-1, -1), 1.9 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1.9 * mm),
                ]),
            )
        ]
        elems.append(Spacer(0, 5.2 * mm))
        dob_parts = self.data["defendant_DOB"].split("/")
        ps = styles["rc-aawp-main"]
        ps_center = extend_style(ps, alignment=TA_CENTER)
        elems.append(
            Table(
                [
                    [
                        Table(
                            [
                                [
                                    Paragraph("<b>Defendant's Signature</b>", style=ps),
                                    SignatureRect(66 * mm, 5 * mm, label="Defendant", sig_id="DS-01"),
                                    Paragraph("<b>Date</b>", style=ps_center),
                                    SignatureDatetimeRect(39 * mm, 5 * mm, sig_id="DS-01")
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("ALIGN", (2, 0), (2, 0), "CENTER"),
                                ("LEFTPADDING", (1, 0), (1, 0), 1.5 * mm),
                                ("LEFTPADDING", (3, 0), (3, 0), 1.5 * mm),
                                ("LINEBELOW", (1, 0), (1, -1), 0.5, "black"),
                                ("LINEBELOW", (3, 0), (3, -1), 0.5, "black"),
                            ]),
                            colWidths=(41.7 * mm, 69.9 * mm, 10.5 * mm, None),
                        )
                    ],
                    [
                        Table(
                            [
                                [
                                    Paragraph("<b>Defendant's Printed Name</b>", style=ps),
                                    Paragraph("%s" % self.data["defendant_name"], ps),
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("LEFTPADDING", (1, 0), (1, 0), 1.5 * mm),
                                ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                            ]),
                            colWidths=(49.3 * mm, None),
                        )
                    ],
                    [
                        Table(
                            [
                                [
                                    Paragraph("<b>Defendant's Education</b>", style=ps),
                                    Paragraph("%s" % self.data["defendant_education"], ps),
                                    Paragraph("<b>Date of Birth</b>", style=ps_center),
                                    Paragraph("%s" % dob_parts[0], style=ps_center),
                                    Paragraph("/", style=ps),
                                    Paragraph("%s" % dob_parts[1], style=ps_center),
                                    Paragraph("/", style=ps),
                                    Paragraph("%s" % dob_parts[2], style=ps_center),

                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("LEFTPADDING", (1, 0), (1, 0), 1.5 * mm),
                                ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                                ("LINEBELOW", (3, 0), (3, 0), 0.5, "black"),
                                ("LINEBELOW", (5, 0), (5, 0), 0.5, "black"),
                                ("LINEBELOW", (7, 0), (7, 0), 0.5, "black"),
                            ]),
                            colWidths=(
                                42.7 * mm, 40.2 * mm, 25.8 * mm, 6.3 * mm, 1.3 * mm, 6.3 * mm, 1.3 * mm, 10.4 * mm
                            ),
                        )
                    ],
                    [
                        Table(
                            [
                                [
                                    Paragraph("I can both speak and read English", style=ps),
                                    Paragraph("X" if self.data["defendant_english"] else "", style=ps_center),
                                    Paragraph(".", style=ps),
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                            ]),
                            colWidths=(58.2 * mm, 15 * mm, None),
                        )
                    ],
                    [
                        Table(
                            [
                                [
                                    Paragraph("I cannot speak or read English", style=ps),
                                    Paragraph("X" if not self.data["defendant_english"] else "", style=ps_center),
                                    Paragraph("; I need an interpreter and translator for", style=ps),
                                    Paragraph("%s" % self.data["interpreter_language"], style=ps_center),
                                    Paragraph(".", style=ps),
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                                ("LINEBELOW", (3, 0), (3, 0), 0.5, "black"),
                            ]),
                            colWidths=(52.6 * mm, 14.7 * mm, 67 * mm, 29.2 * mm, None),
                        )
                    ],
                ],
                style=styles["rc-main-table"],
                colWidths=165 * mm,
                rowHeights=4.8 * mm
            )
        )
        elems.append(Spacer(0, 4.5 * mm))
        num_citations = len(self.data["citation_table"])
        row_heights = [4.2 * mm] + [8.4 * mm] * num_citations
        ps = extend_style(ps_center, fontSize=10, leading=12.5)
        ps_left = extend_style(ps, alignment=TA_LEFT)
        table_data = [
            [
                Paragraph("<b>CITATION NO.</b>", style=ps),
                Paragraph("<b>VIOLATION</b>", style=ps),
                Paragraph("<b>PLEA (CHECK ONE)</b>", style=ps),
            ]
        ]
        for i in range(0, num_citations):
            table_data.append([
                Paragraph("%s" % self.data["citation_table"][i]["citation_number"], style=ps),
                Paragraph("%s" % self.data["citation_table"][i]["violation"], style=ps),
                Table(
                    [
                        [
                            XBox(6.7, True if self.data["citation_table"][i]["plea"] else False),
                            Paragraph("GUILTY", style=ps_left)
                        ],
                        [
                            XBox(6.7, True if not self.data["citation_table"][i]["plea"] else False),
                            Paragraph("NO CONTEST", style=ps_left)
                        ]
                    ],
                    style=extend_table_style(styles["rc-main-table"], [
                        ("LEFTPADDING", (0, 0), (0, -1), 5.5 * mm),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ]),
                    colWidths=(14.5 * mm, None)
                )
            ])
        elems.append(
            Table(
                table_data,
                style=extend_table_style(styles["rc-main-table"], [
                    ("GRID", (0, 0), (-1, -1), 0.5, "black"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]),
                colWidths=(30.4 * mm, 96.6 * mm, 41 * mm),
                rowHeights=row_heights
            )
        )
        return elems

    def _section_section_2(self):
        elems = [
            Paragraph(
                "II.&nbsp;&nbsp;ADVISEMENT AND ACKNOWLEDGEMENT OF RIGHTS SECTION",
                style=styles["rc-section-header"]
            ),
            Paragraph(
                "The following constitutional and state rights apply in this case. I acknowledge that I have carefully read and understand these rights that only I can waive (give up), and my signature below proves that I am waiving all of these rights freely, voluntarily and knowingly.",
                extend_style(styles["rc-aawp-main"], alignment=TA_JUSTIFY, leftIndent=1.9 * mm, rightIndent=1.9 * mm)
            )
        ]
        list_text = [
            "I have the right to have the violation(s) against me explained and understand them.",
            "I have the right to be presumed innocent.",
            "I have the right to remain silent and not incriminate myself. I cannot be forced to testify nor can my silence be used against me.",
            "I have the right to be represented by an attorney. I have the right be represented by a court-appointed attorney, if I cannot afford to hire an attorney of my choice.",
            "I have theright to a public trial heard and decided by a jury.",
            "I have the right to confront the witnesses against me; that is, to see, hear and question all witnesses who testify under oath.",
            "I have the right to produce evidence and use the Court's subpoena power to bring to court witnesses and evidence on my behalf.",
            "I have the right to make the County prove that I am guilty of each violation beyond a reasonable doubt.",
            "I have the right to seek appellate review of my conviction, within 30 days of my conviction, in a higher court if I am found guilty after a trial.",
            "I understand that the maximum penalty that can be imposed for each violation is a fine of up to one thousand dollars ($1,000.00) and up to 60 (sixty) days in jail; and that the maximum period of probation is up to six (6) months.",
            "I understand that, even though the county prosecutor may recommend a sentence, the Court is not bound to accept a recommendation and may impose a lesser or greater sentence than recommended. The Court may, in its discretion, sentence me to serve a sentence consecutively to another sentence.",
            "I understand that the Court does not have to accept a plea of no contest (nolo contendere)",
            "I understand that I may file a petition for habeas corpus, within one year from my conviction, to seek a review of my plea proceedings.",
            "I understand that if I am not a citizen of the United States, my plea of guilty or no contest may have an adverse impact upon my immigration status.",
            "I understand that if I am on probation or parole, a plea of guilty to the charges in this court could be used against me to revoke, that is take away, all or part of my probated or my parole sentence and could result in my serving all or part of that sentence in jail or prison.",
            "I understand that if I receive a suspended or probated sentence by the Court, I must comply with the terms of my sentence, including, but not limited to, the payment of any fine and restitution, compliance actions and other special conditions, until my sentence expires or terminates by court order.",
        ]
        list_data = [
            [Paragraph("<seq id=\"s2_l0\">.", styles["rc-aawp-main"]), Paragraph(l, styles["rc-aawp-main"])] for l in
            list_text
        ]
        elems.append(
            Table(
                list_data,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (0, -1), 1.9 * mm),
                    ("RIGHTPADDING", (1, 0), (1, -1), 1.9 * mm),
                ]),
                colWidths=(8.25 * mm, None)
            )
        )
        return elems

    def _section_section_3(self):
        elems = [
            Paragraph(
                "III.&nbsp;SPECIAL ADVISEMENT AND ACKNOWLEDGMENT OF RIGHT TO COUNSEL SECTION",
                style=styles["rc-section-header"]
            ),
            Paragraph(
                "I have the right to represent myself or to be represented by an attorney in all criminal county ordinance proceedings against me. If I am not financially able to employ an attorney of my own choice, I have a right to have a court-appointed attorney to represent me. An attorney can help me (1) understand the violation(s) against me; (2) determine whether a legally sufficient citation has been filed against me; (3) determine whether I have any defense to the violation(s) against me, possible defenses and the County's burden to prove me guilty on all elements of the violation(s) beyond a reasonable doubt; (4) prepare and conduct any trial held on the violation(s) against me; (5) determine what evidence is legally admissible; (6) file motions and make objections to exclude evidence which is not legally admissible against me; (7) determine what evidence I would be able to present in my defense; (8) file motions to obtain information from the prosecution, such as incident reports, scientific reports, witness statements, video or audio recordings, photographs, etc.; (9) make strategic decisions as to the calling of witnesses and whether or not I should testify at trial; (10) properly preserve legal issues for appeal in the event that I am convicted at trial; (11) conduct plea negotiations on my behalf if I desire to plead guilty or no contest to the violation(s) against me; (12) make sure all of my rights as a defendant in a criminal case are protected. Proceeding without the assistance of an attorney in my case may be detrimental to my best interest. If convicted after a trial, the Judge has the discretion to sentence me, for each violation conviction, to a maximum jail term of 60 (sixty) days and/or fine up to $1000 (one thousand dollars).",
                extend_style(styles["rc-aawp-main"], leftIndent=1.9 * mm, rightIndent=1.9 * mm)
            ),
            Spacer(0, 7.75 * mm)
        ]
        return elems

    def _section_section_4(self):
        elems = [
            Paragraph(
                "IV.&nbsp;&nbsp;DEFENDANT'S STATEMENT REGARDIN GWAIVER OF RIGHTS AND PLEA OF GUILTY OR NO CONTEST SECTION",
                style=styles["rc-section-header"]
            ),
            Paragraph(
                "I have carefully read, or had read to me, all of the foregoing sections of this form. I understand all of information provided in these sections. I have no questions, which need to be answered before I sign this below. My signature certifies that I have been advised of, and understand, the violation(s) against me on the citation(s); that I have been advised of, and understand, my rights, including but not limited to my right to counsel, to remain silent and plead not guilty, to be publicly tried by judge or jury, to confront witnesses against me and to make the County prove my guilt beyond a reasonable doubt; the maximum punishment provided by law applicable to my case, and the consequences of pleading guilty or no contest; that I am not under the influence of any alcohol, medication or other substance; and I have not been threatened, forced, or promised anything inducing me to plead guilty or no contest other than the terms of the plea agreement which will be stated on the record. I further certify, and agree, that a factual basis exists for the violation(s) to which I am entering a plea of guilty or no contest; that I desire to plead guilty or no contest; that I made up my own mind to plead guilty or no contest and that I freely, voluntarily and knowingly waive my aforementioned rights. I further state that I am satisfied with my attorney's services and manner of handling of my case if I exercised my right to counsel.",
                extend_style(styles["rc-aawp-main"], leftIndent=1.9 * mm, rightIndent=1.9 * mm)
            ),
        ]
        elems.append(Spacer(0, 3 * mm))
        elems.append(
            Table(
                [
                    [
                        Paragraph("<b>Defendant's Signature</b>", style=styles["rc-aawp-main"]),
                        SignatureRect(70 * mm, 4.8 * mm, label="Defendant", sig_id="DS-02"),
                        None,
                        None,
                        Paragraph("<b>Date</b>", style=extend_style(styles["rc-aawp-main"], alignment=TA_CENTER)),
                        SignatureDatetimeRect(41 * mm, 4.8 * mm, sig_id="DS-02")
                    ],
                    [
                        Paragraph("<b>Defendant's Printed Name</b>", style=styles["rc-aawp-main"]),
                        None,
                        Paragraph("%s" % self.data["defendant_name"], style=styles["rc-aawp-main"]),
                    ],
                    [
                        None
                    ],
                    [
                        Paragraph("<b>Defendant's Attorney Signature</b>", style=styles["rc-aawp-main"]),
                        None,
                        None,
                        SignatureRect(52 * mm, 4.8 * mm, label="Defendant", sig_id="DAS-01"),
                        Paragraph("<b>Date</b>", style=extend_style(styles["rc-aawp-main"], alignment=TA_CENTER)),
                        SignatureDatetimeRect(41 * mm, 4.8 * mm, sig_id="DAS-01")
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    # ("SPAN", (1, 0), (3, 0)),
                    ("SPAN", (0, 1), (1, 1)),
                    ("LINEBELOW", (1, 0), (3, 0), 0.5, "black"),
                    ("LINEBELOW", (5, 0), (6, 0), 0.5, "black"),
                    ("SPAN", (2, 1), (-1, 1)),
                    ("LINEBELOW", (2, 1), (6, 1), 0.5, "black"),
                    ("SPAN", (0, 3), (2, 3)),
                    ("LINEBELOW", (3, 3), (3, 3), 0.5, "black"),
                    ("LINEBELOW", (5, 3), (6, 3), 0.5, "black"),
                ]),
                colWidths=(41.5 * mm, 7.6 * mm, 9.9 * mm, 53 * mm, 10.5 * mm, 42 * mm),
                rowHeights=4.8 * mm
            )
        )
        elems = elems + [
            Spacer(0, 5 * mm),
            Paragraph(
                "The Court finds that the Defendant has appeared in open court and entered a plea. The Defendant freely, voluntarily and knowingly, waived the above rights.  I am satisfied that there is a factual and legal basis for the plea accepted and entered. The Defendant's waiver of rights and plea were entered freely, voluntarily and knowingly with an understanding of the nature of the violation(s) and consequences of the plea.",
                extend_style(styles["rc-aawp-main"], leftIndent=1.9 * mm, rightIndent=1.9 * mm)
            ),
            Paragraph(
                "<b>IT IS ORDERED</b> that the Defendant's plea is accepted and entered.",
                extend_style(styles["rc-aawp-main"], leftIndent=14.5 * mm, spaceBefore=5.2 * mm, spaceAfter=6 * mm)
            ),
        ]
        date_parts = self.data["ordered_date"].split("/")
        date_parts[0] = int(date_parts[0])
        if date_parts[0] == 1:
            date_parts[0] = "1st"
        elif date_parts[0] == 2:
            date_parts[0] = "2nd"
        elif date_parts[0] == 3:
            date_parts[0] = "3rd"
        else:
            date_parts[0] = "%sth" % date_parts[0]
        date_parts[1] = datetime.date(1900, int(date_parts[1]), 1).strftime('%B')
        date_parts[2] = date_parts[2][2:]
        elems.append(
            Table(
                [
                    [
                        Paragraph("<b>SO ORDERED</b> this", styles["rc-aawp-main"]),
                        Paragraph("%s" % date_parts[0], extend_style(styles["rc-aawp-main"], alignment=TA_CENTER)),
                        Paragraph("day of", extend_style(styles["rc-aawp-main"], alignment=TA_CENTER)),
                        Paragraph("%s" % date_parts[1], extend_style(styles["rc-aawp-main"], alignment=TA_CENTER)),
                        Paragraph("20", extend_style(styles["rc-aawp-main"], alignment=TA_RIGHT)),
                        Paragraph("%s" % date_parts[2], styles["rc-aawp-main"]),
                        Paragraph(".", styles["rc-aawp-main"]),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LEFTPADDING", (0, 0), (0, -1), 1.9 * mm),
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                    ("LINEBELOW", (3, 0), (3, 0), 0.5, "black"),
                    ("LINEBELOW", (5, 0), (5, 0), 0.5, "black"),
                ]),
                colWidths=(38 * mm, 10.5 * mm, 12.8 * mm, 28.5 * mm, 5.5 * mm, 7.3 * mm, 2 * mm, None)
            )
        )
        elems.append(Spacer(0, 1 * mm))
        elems.append(SignatureRect(98 * mm, 9 * mm, label="Magistrate Judge", leftIndent=66 * mm))
        elems.append(
            Table(
                [
                    [
                        None,
                        XBox(7.8, True if self.data["judge_is_phinia_aten"] else False),
                        Paragraph("Chief Magistrate Judge Phinia Aten", styles["rc-aawp-main"]),
                        None,
                        None,
                    ],
                    [
                        None,
                        XBox(7.8, True if self.data["judge_other"] else False),
                        Paragraph("Magistrate Judge:", styles["rc-aawp-main"]),
                        Paragraph("%s" % self.data["judge_other_name"], styles["rc-aawp-main"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEABOVE", (1, 0), (3, 0), 0.5, "black"),
                    ("LINEBELOW", (3, 1), (3, 1), 0.5, "black"),
                    ("LEFTPADDING", (2, 0), (2, -1), 1.5 * mm),
                    ("RIGHTPADDING", (1, 0), (1, -1), 1.5 * mm),
                    ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                    ("VALIGN", (1, 0), (1, -1), "MIDDLE"),
                    ("SPAN", (2, 0), (3, 0)),
                ]),
                colWidths=(None, 33.5 * mm, 33.3 * mm, 32.8 * mm, 3.8 * mm)
            )
        )
        return elems
