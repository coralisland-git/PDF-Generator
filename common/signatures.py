from reportlab.lib import colors
from reportlab.platypus import BaseDocTemplate
from reportlab.platypus.flowables import Flowable


class SignatureDocTemplate(BaseDocTemplate):
    def __init__(self, *args, **kwargs):
        BaseDocTemplate.__init__(self, *args, **kwargs)
        self.metadata = {"locations": {"signatures": list()}}
        self.sig_counter = 0

    def add_signature(self, coords, sig_id, label=""):
        if not sig_id:
            self.sig_counter += 1
            sig_id = self.sig_counter
        sig = {
            "id": str(sig_id),
            "label": label,
            "page": self.page,
            "coordinates": coords,
        }
        self.metadata["locations"]["signatures"].append(sig)

    def add_signed_datetime(self, coords, sig_id):
        for signature in self.metadata["locations"]["signatures"]:
            if str(sig_id) == str(signature["id"]):
                signature["signed_datetime"] = {"coordinates": coords}
                return
        raise IndexError("Signature id not found: %s" % sig_id)

    def build(self, *args, **kwargs):
        BaseDocTemplate.build(self, *args, **kwargs)
        return self.metadata


class LocationRect(Flowable):
    _fixedWidth = 1
    _fixedHeight = 1

    def __init__(self, width, height, leftIndent=0, spaceBefore=0, showBoundary=False):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.leftIndent = leftIndent
        self.spaceBefore = spaceBefore
        self.showBoundary = showBoundary
        self.coords = {}

    def _get_page_coords(self):
        shift_above_signing_line = min(self.height * 0.1, 3)
        x_1 = int(self.canv._currentMatrix[4])
        y_1 = int(self.canv._currentMatrix[5])
        x_2 = int(x_1 + self.width)
        y_2 = int(y_1 + self.height)
        y_1 += int(shift_above_signing_line)
        # top_left, top_right, bottom_right, bottom_left
        # (x_1, y_2), (x_2, y_2), (x_2, y_1), (x_1, y_1)
        return {
            "bottom_left": {"x_coord": x_1, "y_coord": y_1},
            "top_left": {"x_coord": x_1, "y_coord": y_2},
            "top_right": {"x_coord": x_2, "y_coord": y_2},
            "bottom_right": {"x_coord": x_2, "y_coord": y_1},
        }

    def draw(self):
        self.canv.translate(self.leftIndent, self.spaceBefore * -1)
        self.coords = self._get_page_coords()
        if self.showBoundary:
            self.canv.saveState()
            self.canv.setLineWidth(0.5)
            self.canv.setStrokeColor(colors.red)
            self.canv.rect(0, 0, self.width, self.height)
            self.canv.restoreState()

    def __repr__(self):
        return "%s(w=%s, h=%s)" % (self.__class__.__name__, self.width, self.height)


class SignatureRect(LocationRect):
    def __init__(self, *args, **kwargs):
        self.sig_id = None
        self.label = None
        attrs = ["sig_id", "label"]
        for attr in attrs:
            if attr in kwargs:
                setattr(self, attr, kwargs[attr])
                del kwargs[attr]
        LocationRect.__init__(self, *args, **kwargs)

    def draw(self):
        LocationRect.draw(self)
        self.canv._doctemplate.add_signature(self.coords, self.sig_id, self.label)


class SignatureDatetimeRect(LocationRect):
    def __init__(self, *args, **kwargs):
        self.sig_id = None
        attrs = ["sig_id"]
        for attr in attrs:
            if attr in kwargs:
                setattr(self, attr, kwargs[attr])
                del kwargs[attr]
        LocationRect.__init__(self, *args, **kwargs)

    def draw(self):
        LocationRect.draw(self)
        self.canv._doctemplate.add_signed_datetime(self.coords, self.sig_id)
