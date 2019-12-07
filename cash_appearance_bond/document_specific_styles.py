from common.reportlab_styles import *


pdfmetrics.registerFont(
    TTFont("Calibri", os.path.join(os.getcwd(), "fonts", "Calibri Regular.ttf"))
)

pdfmetrics.registerFont(
    TTFont("Calibri-bold", os.path.join(os.getcwd(), "fonts", "Calibri Bold.TTF"))
)

pdfmetrics.registerFont(
    TTFont("Calibri-Italic", os.path.join(os.getcwd(), "fonts", "Calibri Italic.ttf"))
)

pdfmetrics.registerFont(
    TTFont("Calibri-Bold-Italic", os.path.join(os.getcwd(), "fonts", "Calibri Bold Italic.ttf"))
)

pdfmetrics.registerFontFamily(
    "Calibri",
    normal="Calibri",
    bold="Calibri-bold",
    italic="Calibri-Italic",
    boldItalic="Calibri-Bold-Italic",
)

x = 0
y = 0
usable_width = width
usable_height = height

def extend_list_style(**params):
    return ListStyle("extended", **params)
