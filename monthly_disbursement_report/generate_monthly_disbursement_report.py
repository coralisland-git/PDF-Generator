import cStringIO

from common.signatures import *
from document_specific_styles import *
from sample_data import sample_data


def generate_monthly_disbursement_report():
    buff = cStringIO.StringIO()
    doc = SignatureDocTemplate(buff, pagesize=letter)
    f = Frame(gutters[0], gutters[2], usable_width, usable_height, showBoundary=0)

    story = [
        Spacer(0 * mm, 5 * mm),
        Paragraph('''<b>MONTHLY DISBURSEMENT REPORT</b>''', style=styles["rc-mdr-header"]),
        Spacer(0 * mm, 4 * mm),
        Table(
            [
                [
                    Paragraph("Report Year/Month: " + str(sample_data["report_year"]) + " / " + process_month(sample_data["report_month"])
                              , style=styles["rc-mdr-main-content"]),
                    Paragraph("Report Date: " + sample_data["report_date"], style=styles["rc-mdr-main-content"]),
                    Paragraph("County: DEKALB", style=styles["rc-mdr-main-content"])
                ],

            ],
            style=extend_table_style(
                styles["rc-main-table"], [("VALIGN", (0, 0), (-1, -1), "TOP")]
            ),
            colWidths=(60 * mm, 70 * mm, 70 * mm),
        ),
        Table(
            [
                [
                    Paragraph("City: BROOKHAVEN", style=styles["rc-mdr-main-content"]),
                    Paragraph("Phone: 404-637-0660", style=styles["rc-mdr-main-content"]),
                    Paragraph("ORI: 044201J", style=styles["rc-mdr-main-content"])
                ],

            ],
            style=extend_table_style(
                styles["rc-main-table"], [("VALIGN", (0, 0), (-1, -1), "TOP")]
            ),
            colWidths=(60 * mm, 70 * mm, 70 * mm),
        ),
        Spacer(0 * mm, 3 * mm),
        Table(
            [
                [
                    Paragraph("", style=styles["rc-mdr-main-content"]),
                    Paragraph("Fund",  style=styles["rc-mdr-main-content"]),
                    Paragraph("Total Disbursements",  style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("1. ADR-", style=styles["rc-mdr-main-content"]),
                    Paragraph("Alternative Dispute Resolution (O.C.G.A 15-23-7)", style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["adr"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("2. CITY-", style=styles["rc-mdr-main-content"]),
                    Paragraph("City General Fund", style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["city"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("3. COUNTY-", style=styles["rc-mdr-main-content"]),
                    Paragraph("County General Fund (O.C.G.A 15-21-2)", style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["county"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("4. CRF-", style=styles["rc-mdr-main-content"]),
                    Paragraph("Clerk Retirement Fund (O.C.G.A 47-14-50 and 47-14-51)", style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["crf"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("5. DATE-", style=styles["rc-mdr-main-content"]),
                    Paragraph("Drug Abuse Treatment & Educ. (OCGA 15-21-500)",
                              style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["date"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("6. JAIL-", style=styles["rc-mdr-main-content"]),
                    Paragraph("County Jail Fund (OCGA 15-21-100)",
                              style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["jail"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("7. LL-", style=styles["rc-mdr-main-content"]),
                    Paragraph("Law Library (OCGA 36-15-9 and 15-6-7)",
                              style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["ll"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("8. POABF", style=styles["rc-mdr-main-content"]),
                    Paragraph("Peace Officers' Annuity and Benefit Fund (O.C.G.A 47-16-60)",
                              style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["poabf"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("9. PRF-", style=styles["rc-mdr-main-content"]),
                    Paragraph("Probate Retirement Fund(O.C.G.A. 47-11-50 and 47-11-51)",
                              style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["prf"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("10. PUB-", style=styles["rc-mdr-main-content"]),
                    Paragraph("Publication Fee (O.C.G.A 16-5-26, 16-5-96, 40-6-391 and 16-6-13)",
                              style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["pub"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("11. REST-", style=styles["rc-mdr-main-content"]),
                    Paragraph("Restitution (O.C.G.A 17-14-1 AND 17-14-14)",
                              style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["rest"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("12. SRF-", style=styles["rc-mdr-main-content"]),
                    Paragraph("Sheriffs' Retirement Fund (O.C.G.A 47-16-60 and 47-16-61)",
                              style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["srf"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("13. IDAF-", style=styles["rc-mdr-main-content"]),
                    Paragraph("Indigent Defense Application Fee - kept LOCAL (O.C.G.A 15-21A-6(e))",
                              style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["idaf"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("14.PROB-", style=styles["rc-mdr-main-content"]),
                    Paragraph("Probation Fees Collected & Remitted Directory by Probation Office (state, local & private) State Treasury ($23 supervsion fee)",
                              style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["prob_fee"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("", style=styles["rc-mdr-main-content"]),
                    Paragraph("Crime Victims Emergency Fund ($9 fee)",
                              style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["prob_crime_victims"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("", style=styles["rc-mdr-main-content"]),
                    Paragraph("Restitution", style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["prob_restitution"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("15. LVAP-", style=styles["rc-mdr-main-content"]),
                    Paragraph("Local Crime Victims Assistance Fund (O.C.G.A 15-21-131 and 15-21-132)",
                              style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["lvap"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("16. MRF-", style=styles["rc-mdr-main-content"]),
                    Paragraph("Magistrate Retirement Fund (O.C.G.A 47-25-60)",
                              style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["mrf"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("17. POPIDF-A", style=styles["rc-mdr-main-content"]),
                    Paragraph("Peace Officer, Prosecutor and Training Fund - Bond forfeitures",
                              style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["popidf_a"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("18. POPIDF-B", style=styles["rc-mdr-main-content"]),
                    Paragraph("Peace Officer, Prosecutor and Indigent Defense Fund - Bond forfeitures",
                              style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["popidf_b"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("19. JOF-", style=styles["rc-mdr-main-content"]),
                    Paragraph("Judicial Operation fund Fee - kept LOCAL(O.C.G.A 15-21A-6.2)",
                              style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["jof"]), style=styles["rc-mdr-main-content"])
                ],
                [
                    Paragraph("GRAND TOTAL COLLECTED", style=styles["rc-mdr-main-content"]),
                    Paragraph("",
                              style=styles["rc-mdr-main-content"]),
                    Paragraph("$ " + str(sample_data["grand_total_collected"]), style=styles["rc-mdr-main-content"])
                ]
            ],
            style=extend_table_style(
                styles["rc-main-table"],
                [
                    ("VALIGN", (0, 0), (-1, -1), "CENTER"),
                    ('BOX', (0, 0), (-1, -1), 1, colors.black),
                    ('BOX', (0, 0), (1, -1), 1, colors.black),
                    ('BOX', (0, 0), (0, -1), 1, colors.black),
                    ('LINEABOVE', (0, 0), (-1, -1), 1, colors.black),
                    ('LINEBELOW', (0, 0), (-1, -1), 1, colors.black),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 3),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                    ("SPAN", (0, 14), (0, 16)),
                    ("SPAN", (0, 22), (1, 22))
                ]
            ),
            colWidths=(27 * mm, 120 * mm, 47 * mm),
        ),
        Spacer(0 * mm, 2 * mm),
        Paragraph("I, the Undersigned clerk/court officer of the above named court, hereby certify that, to the best of my knowledge, the above and foregoing is a true and correct account of all above-referenced funds collected for the month specified",
                  style=styles["footer"]),
        Spacer(0 * mm, 4 * mm),
        Table(
            [
                [
                    Paragraph(
                        '''
                        <b>INSTRUCTIONS: Complete and return to Georgia Superior Court Clerk's Coop.</b>
                        ''', style=styles["signature"]
                    ),
                    "",
                    Paragraph("<u>{}</u>".format("&nbsp;" * 75), style=styles["signature"]),
                ],
                [
                    Paragraph(
                        '''
                        <b>Authority (GSCCCA) by last day of month following the month of disbursement.</b>
                        ''', style=styles["signature"]
                    ),
                    "",
                    Paragraph("Clerk of Court / Judge", style=styles["signature"]),
                ],
            ],
            colWidths=(140 * mm, 0 * mm, 80 * mm),
            rowHeights=(8 * mm, 4 * mm)
        ),
        Spacer(0 * mm, 8 * mm),
        Table(
            [
                [
                    Paragraph("Direct Inquiries to FINES AND FEES DIVISION", style=styles["signature"]),
                    None,
                    Paragraph("<u>{}</u>".format(sample_data["phone"] + get_remain_space(sample_data["phone"])), style=styles["signature"]),
                ],
                [
                    Paragraph("WEB: http://www.courtrax.org", style=styles["signature"]),
                    None,
                    Paragraph("Phone Number", style=styles["signature"]),
                ],

                [
                    Paragraph("EMAIL: FinesAndFees@gscca.org", style=styles["signature"]),
                    None,
                    Paragraph("<u>{}</u>".format(sample_data["email"] + get_remain_space(sample_data["email"])), style=styles["signature"]),
                ],
                [
                    Paragraph("PHONE: (886)847-4058", style=styles["signature"]),
                    None,
                    Paragraph("Email Address", style=styles["signature"]),
                ],
            ],
            colWidths=(140 * mm, 0 * mm, 80 * mm),
            rowHeights=(4 * mm, 4 * mm, 8 * mm, 4 * mm)
        )
    ]

    main_template = PageTemplate(id="main_template", frames=[f])
    doc.addPageTemplates([main_template])
    doc.build(story, canvasmaker=PageNumCanvas)
    del doc

    buff.seek(0)
    return buff


def process_month(month):
    if month < 10:
        return "0" + str(month)
    else:
        return str(month)


def get_remain_space(str):
        return "&nbsp;" * (75 - len(str) * 2)

