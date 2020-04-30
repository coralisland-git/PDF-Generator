from common.reportlab_styles import *

text_style = extend_style(
    styles['body'],
    leftIndent=5,
    rightIndent=5,
    fontSize=9,
    leading=11,
    spaceBefore=5
)

styles["subheading"] = ParagraphStyle(
    "bold",
    parent=styles["body"],
    leading=18,
    textTransform="uppercase",
    fontName="Times-Roman",
    bulletFontName="Times-Roman",
    alignment=TA_CENTER,
    fontSize=10
)


class FirstPageOnlyDatePageNumCanvas(PageNumCanvas):
    def draw_date(self):
        if self._pageNumber == 1:
            PageNumCanvas.draw_date(self)
