import cStringIO

from common.signatures import *
from document_specific_styles import *


def generate_fpc_c_and_d_order():
    buff = cStringIO.StringIO()
    doc = SignatureDocTemplate(buff, pagesize=letter)
    f = Frame(gutters[0], gutters[2], usable_width, usable_height, showBoundary=0)

    story = []

    main_template = PageTemplate(id="main_template", frames=[f])
    doc.addPageTemplates([main_template])
    doc.build(story, canvasmaker=PageNumCanvas)
    del doc

    buff.seek(0)
    return buff
