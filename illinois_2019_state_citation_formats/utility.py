import io
import copy
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import PageObject
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas


def make_margin_page(size, margin):
    buff = io.BytesIO()
    c = canvas.Canvas(buff, pagesize=size)
    c.setLineWidth(margin)
    c.setStrokeColor((1, 1, 1))
    c.rect(margin / 2, margin / 2, size[0] - margin, size[1] - margin)
    c.save()
    buff.seek(0)
    return PdfFileReader(buff).getPage(0)


def get_pages(fp):
    pdf = PdfFileReader(fp)
    input_pages = list()
    for i in range(pdf.getNumPages()):
        input_pages.append(pdf.getPage(i))
    return input_pages


# import os
# ifp = os.path.expanduser("~/Desktop/traffic.pdf")
# ofp = os.path.expanduser("~/Desktop/out.pdf")
# resize_pdf_file(ifp, ofp, page_size=letter, margin=0.5 * inch, scale=1.3, overlap=1 * mm)
def resize_pdf_file(input_fp, output_fp, page_size=letter, margin=0.5 * inch, scale=1.0, overlap=0):
    margin_page = make_margin_page(page_size, margin)
    input_pages = get_pages(input_fp)
    usable_height = (page_size[1] - margin * 2)
    pdf = PdfFileWriter()
    for i in range(len(input_pages)):
        input_pages[i].scaleBy(scale)
        page = copy.copy(input_pages[i])
        coords = [(float(c[0]), float(c[1])) for c in [page.mediaBox.lowerLeft, page.mediaBox.upperRight]]
        p_height = coords[1][1] - coords[0][1]
        num_pages = int(p_height / usable_height + 1)
        num_pages = int((p_height + overlap * num_pages) / usable_height + 1)
        y_offset = margin + usable_height - p_height
        for j in range(num_pages):
            x_offset = margin
            if j:
                y_offset += usable_height - overlap
            p = PageObject.createBlankPage(width=page_size[0], height=page_size[1])
            p.mergeTranslatedPage(page, x_offset, y_offset)
            p.mergePage(margin_page)
            pdf.addPage(p)
    with open(output_fp, 'wb') as fh:
        pdf.write(fh)
