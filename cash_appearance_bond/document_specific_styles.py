from common.reportlab_styles import *


x = 0
y = 0
usable_width = width
usable_height = height

def extend_list_style(**params):
    return ListStyle("extended", **params)
