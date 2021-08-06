# -*- coding: utf-8 -*-

"""
@created: 2020-08-05 13:00:00

@author: Jorj X. McKie

Let the user select a PDF file to maintain its images.

Dependencies:
PyMuPDF v1.17.5, wxPython Phoenix version

License:
 GNU AFFERO GPL 3

Copyright:
 (c) 2020 Jorj X. McKie

"""
import os
import sys

import fitz
import wx

print("Python:", sys.version)
print("wxPython:", wx.version())
print(fitz.__doc__)
try:
    from PageFormat import FindFit
except ImportError:

    def FindFit(*args):
        return "not implemented"


try:
    from icons import ico_pdf  # PDF icon in upper left screen corner

    do_icon = True
except ImportError:
    do_icon = False

app = None
app = wx.App()

if wx.VERSION[:3] < (3, 0, 3):
    raise AssertionError("need wxPython Phoenix version")
if fitz.VersionBind.split(".") < ["1", "17", "5"]:
    raise AssertionError("need PyMuPDF 1.17.5 or later")

# compute maximum PDF page display dimensions
MAX_WIDTH, MAX_HEIGHT = wx.GetDisplaySize()
MAX_WIDTH -= 400
MAX_HEIGHT -= 130
cur_hand = wx.Cursor(wx.CURSOR_HAND)
cur_cross = wx.Cursor(wx.CURSOR_CROSS)
cur_norm = wx.Cursor(wx.CURSOR_DEFAULT)
degrees = ["0", "90", "180", "270"]


def getint(v):
    """Convert any string to a non-negative integer."""
    try:
        return int(v)  # fastest
    except:
        pass
    if not type(v) is str:  # we need a string at least
        return 0
    return int("0" + "".join((d for d in v if d in "0123456789")))


def calc_matrix(fw, fh, tr, rotate=0):
    """Calculate transformation matrix for image insertion.

    Notes:
        The result is basically a multiplication of four matrices in this
        sequence: number one moves the image rectangle (always a unit rect!) to (0,0), number two rotates as desired, number three
        scales using the width-height-ratio, and number four moves to the
        target rect.
    Args:
        fw, fh: width / height ratio factors 0 < f <= 1.
                The longer one must be 1.
        tr: target rect in PDF (!) coordinates
        rotate: (degrees) rotation angle.
    Returns:
        Transformation matrix.
    """
    # compute scale matrix parameters
    small = min(fw, fh)  # factor of the smaller side

    if rotate not in (0, 180):
        fw, fh = fh, fw  # width / height exchange their roles

    if fw < 1:  # portrait
        if tr.width / fw > tr.height / fh:
            w = tr.height * small
            h = tr.height
        else:
            w = tr.width
            h = tr.width / small

    elif fw != fh:  # landscape
        if tr.width / fw > tr.height / fh:
            w = tr.height / small
            h = tr.height
        else:
            w = tr.width
            h = tr.width * small

    else:  # (treated as) equal sided
        w = tr.width
        h = tr.height

    # center point of target rectangle
    tmp = (tr.tl + tr.br) / 2.0

    # move image center to (0, 0), then rotate
    m = fitz.Matrix(1, 0, 0, 1, -0.5, -0.5) * fitz.Matrix(rotate)
    m *= fitz.Matrix(w, h)  # concat scale matrix
    m *= fitz.Matrix(1, 0, 0, 1, tmp.x, tmp.y)  # concat move to target center
    return m


def find_image(page, img):
    """Locate image reference in page contents.

    Args:
        page: the PDF page
        img: image reference name
    Returns:
        Dictionary with keys:
        xref - containing /Contents object
        start - position of 'a' in 'a b c d e f cm'
        stop - position of 'cm' + 1
        deg - one of {0, 90, 180, 270}
        bbox - image rectangle
        msg - None if successful

    Notes:
        For changing the image's position, replace bytes [start:stop]
        replaced by the new matrix command.
    """
    doc = page.parent
    img_rect = page.get_image_bbox(img)

    rc = {
        "xref": 0,
        "start": -1,
        "stop": -1,
        "begin": -1,  # begin of '/name Do' command
        "end": -1,  # position after 'Do' command
        "deg": 0,
        "bbox": img_rect,
        "msg": None,
    }
    if img_rect.is_infinite:
        rc["msg"] = "cannot find image"
        return rc

    invoker = b"/%s Do" % img.encode()
    pos1 = -1
    cont = b""
    mat_factors = []
    xref = 0
    for xref in page.get_contents():
        cont = doc.xref_stream(xref)
        pos1 = cont.find(invoker)
        if pos1 > 0:
            rc["begin"] = pos1
            rc["end"] = pos1 + len(invoker)
            break
    if pos1 <= 0:
        rc["msg"] = "cannot find image"
        return rc

    rc["xref"] = xref  # found the image here

    pos2 = cont.rfind(b"cm", 0, pos1)
    if pos2 <= 0:
        rc["msg"] = "cannot find 'cm'"  # PDF command not found
        return rc
    n = pos2 - 1

    for _ in range(6):  # find the 6 matrix coefficients
        while cont[n] in (32, 10):  # space or line break
            n -= 1
            if n <= 0:
                rc["msg"] = "cannot find matrix coeffs"
                return rc
        m = n - 1
        while cont[m] not in (32, 10):
            m -= 1
            if m <= 0:
                rc["msg"] = "cannot find matrix coeffs"
                return rc
        try:  # convert coeff from string to float
            m += 1
            mat_factors.append(round(float(cont[m : n + 1]), 5))
        except:
            rc["msg"] = "invalid matrix coeff " + cont[m : n + 1].decode()
            return rc
        n = m - 1
    start = n + 1  # matrix command starts here
    stop = pos2 + 2  # first byte after matrix command
    rc["start"] = start  # fill return dictionay
    rc["stop"] = stop
    deg = -1
    mat_factors = reversed(mat_factors)
    # -------------------------------------------------------------------------
    # This matrix must recreate the image rectangle. Only then we can be sure,
    # that future changes to this matrix will have valid results.
    # -------------------------------------------------------------------------
    a, b, c, d, _, _ = mat = fitz.Matrix(mat_factors)
    if b == c == 0:  # extract the rotation angle
        if max(a, d) < 0:
            deg = 180
        elif min(a, d) > 0:
            deg = 0
    elif a == d == 0:
        if c < 0 < b:
            deg = 90
        elif b < 0 < c:
            deg = 270
    if deg < 0:  # we only support rotations by 0, 90, 180, 270 deg
        rc["msg"] = "cannot handle image rotation"
        return rc

    rc["deg"] = deg

    mat_test = calc_matrix(1, 1, img_rect * ~page.transformation_matrix, rotate=deg)
    delta = abs(mat - mat_test)  # this must small enough
    if delta > 1e-3:
        rc["msg"] = "cannot re-compute image rect"
        return rc
    return rc


def get_images(page):
    """Loop through the page images.

    We only consider images referenced by the page itself, not those shown
    by e.g. Form XObjects.
    """
    img_list = [img[-3] for img in page.get_images(True) if img[-1] == 0]
    images = {}  # the result
    for img in img_list:
        try:
            d = find_image(page, img)
        except:
            d = {}  # image not found, or some unknown problem
        if d != {}:
            images[img] = d
    return images


# ----------------------------------------------------------------------------
# Our dialog is a subclass of wx.Dialog.
# Only special thing is, that we are being invoked with a filename ...
# ----------------------------------------------------------------------------
class PDFdisplay(wx.Dialog):
    def __init__(self, parent, filename):
        defPos = wx.DefaultPosition
        defSiz = wx.DefaultSize
        zoom = 1  # zoom factor of display
        wx.Dialog.__init__(
            self,
            parent,
            id=-1,
            title="Image Maintenance of ",
            pos=defPos,
            size=defSiz,
            style=wx.CAPTION | wx.CLOSE_BOX | wx.DEFAULT_DIALOG_STYLE,
        )

        # -------------------------------------------------------------
        # display an icon top left of dialog, append filename to title
        # -------------------------------------------------------------
        if do_icon:
            self.SetIcon(ico_pdf.img.GetIcon())  # set a screen icon
        self.SetTitle(self.Title + os.path.basename(filename))
        KHAKI = wx.Colour(240, 230, 140)
        self.SetBackgroundColour(KHAKI)

        # ---------------------------------------------------------------------
        # open document when dialog gets created
        # ---------------------------------------------------------------------
        self.doc = fitz.open(filename)  # create Document object
        if self.doc.needs_pass:  # check password protection
            self.decrypt_doc()
        if self.doc.is_encrypted:  # quit if we cannot decrypt
            self.Destroy()
            return
        self.last_pno = -1  # memorize last page displayed
        self.last_image = 0  # position to this image
        self.img_rect = wx.Rect()  # store image rectangle here
        self.img_bottom_rect = wx.Rect()  # store bottom rectangle here
        self.current_idx = -1  # store entry of found rectangle
        self.page_height = 0  # page height in pixels
        self.dragging_img = False
        self.dragstart_x = -1  # for drags: original x
        self.dragstart_y = -1  # for drags: original y
        self.resize_rect = False  # indicate resizing rect
        self.sense = 10  # cursor tolerance, e.g. min. rectangle
        # side is 2 * self.sense pixels
        self.rotation = 0
        self.page_images = {}
        self.can_change_image = True

        # forward button
        self.btn_Next = wx.Button(self, -1, "forw", defPos, defSiz, wx.BU_EXACTFIT)

        # backward button
        self.btn_Prev = wx.Button(self, -1, "back", defPos, defSiz, wx.BU_EXACTFIT)

        # -------------------------------------------------------------
        # text field for entering a target page. wx.TE_PROCESS_ENTER is
        # required to get data entry fired as events.
        # -------------------------------------------------------------
        self.TextToPage = wx.TextCtrl(
            self, -1, "1", defPos, wx.Size(40, -1), wx.TE_RIGHT | wx.TE_PROCESS_ENTER
        )
        # displays total pages and page paper format
        self.statPageMax = wx.StaticText(
            self, -1, "of " + str(len(self.doc)) + " pages.", defPos, defSiz, 0
        )
        self.paperform = wx.StaticText(self, -1, "", defPos, defSiz, 0)
        # ---------------------------------------------------------------------
        # define zooming matrix for displaying PDF page images
        # ---------------------------------------------------------------------
        self.zoom = fitz.Matrix(zoom, zoom)
        self.shrink = ~self.zoom  # corresp. shrink matrix
        self.bitmap = self.pdf_show(1)
        self.PDFimage = wx.StaticBitmap(self, -1, self.bitmap, defPos, defSiz, style=0)

        # ---------------------------------------------------------------------
        # Fields defining an image
        # ---------------------------------------------------------------------
        self.t_Update = wx.StaticText(self, -1, "")
        self.t_Save = wx.StaticText(self, -1, "")
        self.imgRotation = wx.Choice(self, wx.ID_ANY, defPos, defSiz, degrees, 0)
        self.imgName = wx.TextCtrl(self, -1, "", defPos, wx.Size(100, -1))

        self.bboxLeft = wx.SpinCtrl(
            self,
            -1,
            "",
            defPos,
            wx.Size(60, -1),
            wx.TE_RIGHT | wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER,
            0,
            9999,
            0,
        )
        self.bboxTop = wx.SpinCtrl(
            self,
            -1,
            "",
            defPos,
            wx.Size(60, -1),
            wx.TE_RIGHT | wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER,
            0,
            9999,
            0,
        )
        self.bboxWidth = wx.SpinCtrl(
            self,
            -1,
            "",
            defPos,
            wx.Size(60, -1),
            wx.TE_RIGHT | wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER,
            0,
            9999,
            0,
        )
        self.bboxHeight = wx.SpinCtrl(
            self,
            -1,
            "",
            defPos,
            wx.Size(60, -1),
            wx.TE_RIGHT | wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER,
            0,
            9999,
            0,
        )

        self.img_count = wx.StaticText(self, -1, "")
        self.btn_next_image = wx.Button(
            self, -1, "Next img", defPos, defSiz, wx.BU_EXACTFIT
        )

        self.btn_Update = wx.Button(
            self, -1, "Update img", defPos, defSiz, wx.BU_EXACTFIT
        )

        self.btn_Remove = wx.Button(
            self,
            id=wx.ID_ANY,
            label="Remove img",
            pos=defPos,
            size=self.btn_Update.Size,
            style=0,
            validator=wx.DefaultValidator,
        )

        self.btn_Refresh = wx.Button(
            self, -1, "Refresh img", defPos, self.btn_Update.Size, 0
        )

        self.btn_NewImg = wx.FilePickerCtrl(
            self,
            wx.ID_ANY,
            wx.EmptyString,
            u"Select image file",
            u"*.*",
            defPos,
            defSiz,
            wx.FLP_CHANGE_DIR | wx.FLP_FILE_MUST_EXIST | wx.FLP_SMALL,
        )

        self.btn_Save = wx.Button(
            self, -1, "Save file", defPos, self.btn_Update.Size, 0
        )

        self.btn_Quit = wx.Button(
            self, wx.ID_CANCEL, "Cancel", defPos, self.btn_Update.Size, 0
        )

        self.rectX0 = wx.StaticText(self, -1, "")
        self.rectY0 = wx.StaticText(self, -1, "")
        self.rectX1 = wx.StaticText(self, -1, "")
        self.rectY1 = wx.StaticText(self, -1, "")
        self.message = wx.StaticText(self, -1, "")
        # ---------------------------------------------------------------------
        # dialog sizers
        # ---------------------------------------------------------------------
        szr00 = wx.BoxSizer(wx.HORIZONTAL)  # overall dialog window
        szr10 = wx.BoxSizer(wx.VERTICAL)  # right: page display
        szr20 = wx.BoxSizer(wx.HORIZONTAL)  # top right: page navigation
        szr30 = wx.GridBagSizer(7, 7)  # left: image handling

        # fields for page navigation and info
        szr20.Add(self.btn_Next, 0, wx.ALL, 5)
        szr20.Add(self.btn_Prev, 0, wx.ALL, 5)
        szr20.Add(self.TextToPage, 0, wx.ALL, 5)
        szr20.Add(self.statPageMax, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        szr20.Add(self.paperform, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # use GridBagSizer for image details
        line_span = wx.GBSpan(1, 5)  # use for item taking full line

        # Image details header
        t = wx.StaticText(self, -1, "Image Details", defPos, defSiz, wx.ALIGN_CENTER)
        t.SetBackgroundColour("STEEL BLUE")
        t.SetForegroundColour("WHITE")
        szr30.Add(t, (0, 0), line_span, wx.EXPAND)  # overall header
        szr30.Add(
            wx.StaticLine(self, -1, defPos, defSiz, wx.LI_HORIZONTAL),
            (1, 0),
            line_span,
            wx.EXPAND,
        )

        # bbox header and fields
        szr30.Add(self.btn_next_image, (2, 0), (1, 1))
        szr30.Add(self.img_count, (2, 1), (1, 1), wx.ALIGN_LEFT)

        szr30.Add(wx.StaticText(self, -1, "Name:"), (3, 0), (1, 1), wx.ALIGN_RIGHT)
        szr30.Add(self.imgName, (3, 1), (1, 1), wx.ALIGN_LEFT)

        szr30.Add(wx.StaticText(self, -1, "Rotation:"), (4, 0), (1, 1), wx.ALIGN_RIGHT)
        szr30.Add(self.imgRotation, (4, 1), (1, 1), wx.ALIGN_LEFT)

        szr30.Add(
            wx.StaticText(self, -1, "[wx.Rect]    Left:"),
            (5, 0),
            (1, 1),
            wx.ALIGN_RIGHT,
        )
        szr30.Add(self.bboxLeft, (5, 1), (1, 1), wx.ALIGN_LEFT)

        szr30.Add(wx.StaticText(self, -1, "Top:"), (5, 2), (1, 1), wx.ALIGN_RIGHT)
        szr30.Add(self.bboxTop, (5, 3), (1, 1), wx.ALIGN_LEFT)

        szr30.Add(wx.StaticText(self, -1, "Width:"), (6, 0), (1, 1), wx.ALIGN_RIGHT)
        szr30.Add(self.bboxWidth, (6, 1), (1, 1), wx.ALIGN_LEFT)

        szr30.Add(wx.StaticText(self, -1, "Height:"), (6, 2), (1, 1), wx.ALIGN_RIGHT)
        szr30.Add(self.bboxHeight, (6, 3), (1, 1), wx.ALIGN_LEFT)

        szr30.Add(
            wx.StaticLine(self, -1, defPos, defSiz, wx.LI_HORIZONTAL),
            (7, 0),
            line_span,
            wx.EXPAND,
        )

        # display of fitz.Rect
        szr30.Add(
            wx.StaticText(self, -1, "[fitz.Rect]    x0:"),
            (8, 0),
            (1, 1),
            wx.ALIGN_RIGHT,
        )
        szr30.Add(self.rectX0, (8, 1), (1, 1), wx.ALIGN_LEFT)

        szr30.Add(wx.StaticText(self, -1, "y0:"), (8, 2), (1, 1), wx.ALIGN_RIGHT)
        szr30.Add(self.rectY0, (8, 3), (1, 1), wx.ALIGN_LEFT)

        szr30.Add(wx.StaticText(self, -1, "x1:"), (9, 0), (1, 1), wx.ALIGN_RIGHT)
        szr30.Add(self.rectX1, (9, 1), (1, 1), wx.ALIGN_LEFT)

        szr30.Add(wx.StaticText(self, -1, "y1:"), (9, 2), (1, 1), wx.ALIGN_RIGHT)
        szr30.Add(self.rectY1, (9, 3), (1, 1), wx.ALIGN_LEFT)

        szr30.Add(
            wx.StaticLine(self, -1, defPos, defSiz, wx.LI_HORIZONTAL),
            (10, 0),
            line_span,
            wx.EXPAND,
        )

        szr30.Add(self.message, (11, 0), line_span, wx.ALIGN_LEFT)

        # buttons
        szr30.Add(
            wx.StaticLine(self, -1, defPos, defSiz, wx.LI_HORIZONTAL),
            (14, 0),
            line_span,
            wx.EXPAND,
        )
        szr30.Add(self.btn_Update, (15, 0), (1, 1), wx.ALIGN_RIGHT)
        szr30.Add(self.t_Update, (15, 1), (1, 1))
        szr30.Add(self.btn_Refresh, (16, 0), (1, 1), wx.ALIGN_RIGHT)
        szr30.Add(
            wx.StaticText(self, -1, "Try to make modifyable"),
            (16, 1),
            line_span,
            wx.EXPAND,
        )
        szr30.Add(self.btn_NewImg, (17, 0), (1, 1), wx.ALIGN_RIGHT)
        szr30.Add(
            wx.StaticText(self, -1, "Insert image from file"),
            (17, 1),
            line_span,
            wx.EXPAND,
        )
        szr30.Add(self.btn_Remove, (18, 0), (1, 1), wx.ALIGN_RIGHT)
        szr30.Add(
            wx.StaticText(self, -1, ">> CAUTION - no undo <<"),
            (18, 1),
            line_span,
            wx.EXPAND,
        )
        szr30.Add(self.btn_Save, (19, 0), (1, 1), wx.ALIGN_RIGHT)
        szr30.Add(self.t_Save, (19, 1), (1, 4))
        szr30.Add(self.btn_Quit, (20, 0), (1, 1), wx.ALIGN_RIGHT)
        szr30.Add(
            wx.StaticLine(self, -1, defPos, defSiz, wx.LI_HORIZONTAL),
            (21, 0),
            line_span,
            wx.EXPAND,
        )

        szr10.Add(szr20, 0, wx.EXPAND, 5)
        szr10.Add(self.PDFimage, 0, wx.ALL, 5)

        szr00.Add(szr30, 0, wx.ALL, 5)
        szr00.Add(
            wx.StaticLine(self, -1, defPos, defSiz, wx.LI_VERTICAL), 0, wx.EXPAND, 5
        )
        szr00.Add(szr10, 0, wx.EXPAND, 5)

        szr00.Fit(self)
        self.SetSizer(szr00)
        self.Layout()
        self.Centre(wx.BOTH)

        # Bind dialog items to event handlers
        self.btn_Save.Bind(wx.EVT_BUTTON, self.on_save_file)
        self.btn_next_image.Bind(wx.EVT_BUTTON, self.on_next_image)
        self.btn_Update.Bind(wx.EVT_BUTTON, self.on_update_image)
        self.btn_Remove.Bind(wx.EVT_BUTTON, self.on_remove_image)
        self.btn_Refresh.Bind(wx.EVT_BUTTON, self.on_refresh_image)
        self.btn_Next.Bind(wx.EVT_BUTTON, self.on_next_page)
        self.btn_Prev.Bind(wx.EVT_BUTTON, self.on_previous_page)
        self.btn_NewImg.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_new_image)
        self.TextToPage.Bind(wx.EVT_TEXT_ENTER, self.on_goto_page)
        self.PDFimage.Bind(wx.EVT_ENTER_WINDOW, self.on_enter_window)
        self.PDFimage.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)
        self.PDFimage.Bind(wx.EVT_MOTION, self.on_move_mouse)
        self.PDFimage.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.PDFimage.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.bboxHeight.Bind(wx.EVT_SPINCTRL, self.on_image_changed)
        self.bboxLeft.Bind(wx.EVT_SPINCTRL, self.on_image_changed)
        self.bboxTop.Bind(wx.EVT_SPINCTRL, self.on_image_changed)
        self.bboxWidth.Bind(wx.EVT_SPINCTRL, self.on_image_changed)
        self.imgRotation.Bind(wx.EVT_CHOICE, self.on_rot_changed)
        self.btn_Update.Disable()
        self.btn_Remove.Disable()
        self.btn_Refresh.Disable()
        self.btn_Save.Disable()
        self.imgName.Disable()
        self.new_image(1)

    def __del__(self):
        pass

    # -------------------------------------------------------------------------
    # Button handlers and other functions
    # -------------------------------------------------------------------------

    def on_enter_window(self, evt):
        evt.Skip()
        return

    def on_move_mouse(self, evt):
        if not self.can_change_image:
            evt.Skip()
            return
        pos = evt.GetPosition()
        in_rect = self.img_rect.Contains(pos)  # cursor in image rect
        in_brect = self.img_bottom_rect.Contains(pos)  # in bottom-right corner
        self.PDFimage.SetCursor(cur_norm)  # standard cursor

        if in_brect:  # cursor if in br corner
            self.PDFimage.SetCursor(cur_cross)
        elif in_rect:  # cursor if in a rect
            self.PDFimage.SetCursor(cur_hand)

        if self.resize_rect:  # resizing bbox?
            self.PDFimage.SetCursor(cur_cross)  # adjust cursor
            if evt.LeftIsDown():  # mouse pressed? go!
                r = self.img_rect  # resizing rectangle
                w = pos.x - r.x  # new width
                h = pos.y - r.y  # new height
                nr = wx.Rect(r.x, r.y, w, h)  # new retangle

                if 2 * self.sense <= min(w, h):  # large enough?
                    self.bboxHeight.SetValue(h)
                    self.bboxWidth.SetValue(w)
                    self.redraw_bitmap()
                    self.draw_rect(nr.x, nr.y, w, h, "RED")
                    self.img_rect = nr
                    self.img_bottom_rect = self.bottom_rect_from_rect(nr)
                    self.refresh_fitz_labels(wx.Rect(nr.x, nr.y, w, h))

            evt.Skip()
            return

        if in_rect:  # still here and inside a rect?
            self.PDFimage.SetCursor(cur_hand)  # adjust cursor
            if evt.LeftIsDown():
                r = self.img_rect  # this is the rectangle
                x = pos.x - self.dragstart_x  # new left ...
                y = pos.y - self.dragstart_y  # ... and top values
                w = r.width  # shape does ...
                h = r.height  # ... not change
                nr = wx.Rect(x, y, w, h)  # new rectangle
                self.refresh_fitz_labels(nr)  # update fitz.Rect display
                self.bboxLeft.SetValue(x)  # new screen value
                self.bboxTop.SetValue(y)  # new screen value
                self.redraw_bitmap()
                self.draw_rect(x, y, w, h, "RED")
                self.img_rect = nr
                self.img_bottom_rect = self.bottom_rect_from_rect(nr)
            evt.Skip()
            return

    def bottom_rect_from_rect(self, wxrect):
        p = wxrect.BottomRight
        br = wx.Rect(p.x - self.sense, p.y - self.sense, 2 * self.sense, 2 * self.sense)
        return br

    def refresh_fitz_labels(self, wxrect):
        """Update screen fitz.Rect with wx.Rect values."""
        nfr = self.wxRect_to_Rect(wxrect)
        self.rectX0.Label = "%g" % nfr.x0
        self.rectY0.Label = "%g" % nfr.y0
        self.rectX1.Label = "%g" % nfr.x1
        self.rectY1.Label = "%g" % nfr.y1

    def on_rot_changed(self, evt):
        idx = evt.GetInt()
        self.rotation = int(degrees[idx])
        self.btn_Update.Enable()
        evt.Skip()
        return

    def on_mouse_wheel(self, evt):
        # process wheel as paging operations
        d = evt.GetWheelRotation()  # int indicating direction
        if d < 0:
            self.on_next_page(evt)
        elif d > 0:
            self.on_previous_page(evt)
        return

    def on_next_page(self, event):  # means: page forward
        page = getint(self.TextToPage.Value) + 1  # current page + 1
        page = min(page, self.doc.page_count)  # cannot go beyond last page
        self.TextToPage.ChangeValue(str(page))  # put target page# in screen
        self.new_image(page)  # refresh the layout
        event.Skip()

    def on_previous_page(self, event):  # means: page back
        page = getint(self.TextToPage.Value) - 1  # current page - 1
        page = max(page, 1)  # cannot go before page 1
        self.TextToPage.ChangeValue(str(page))  # put target page# in screen
        self.new_image(page)
        event.Skip()

    def on_goto_page(self, event):  # means: go to page number
        page = getint(self.TextToPage.Value)  # get page# from screen
        page = min(page, len(self.doc))  # cannot go beyond last page
        page = max(page, 1)  # cannot go before page 1
        self.TextToPage.ChangeValue(str(page))  # make sure it's on the screen
        self.new_image(page)
        event.Skip()

    def on_update_image(self, evt):
        """Perform PDF update of changed image position.

        Compute new rectangle from displayed values, compute new matrix,
        update resp. /Contents object with computed matrix, reload
        page and refresh image.
        """
        pno = getint(self.TextToPage.Value) - 1  # page number
        page = self.doc[pno]  # load page
        r = wx.Rect(  # get wx:Rect from screen
            self.bboxLeft.Value,
            self.bboxTop.Value,
            self.bboxWidth.Value,
            self.bboxHeight.Value,
        )
        new_rect = self.wxRect_to_Rect(r)  # compute fitz.Rect
        rot = self.rotation  # rotation value
        key = self.imgName.Value  # image reference name
        self.last_image = list(self.page_images.keys()).index(key)
        d = self.page_images[key]  # image parameters
        xref = d["xref"]
        start = d["start"]
        stop = d["stop"]
        rect = d["bbox"]  # get width / height from previous rectangle
        factor = max(rect.width, rect.height)
        fw = rect.width / factor  # calculate width / height ratio
        fh = rect.height / factor
        if d["deg"] in (90, 270):  # exchange values
            fw, fh = fh, fw
        tar_rect = new_rect * ~page.transformation_matrix
        matrix = calc_matrix(fw, fh, tar_rect, rot)
        # we have the matrix, now read /Contents stream
        cont = bytearray(self.doc.xref_stream(xref))  # modifyable version!

        new_mat = b"%g %g %g %g %g %g cm" % tuple(matrix)
        cont[start:stop] = new_mat  # put in new PDF matrix

        self.doc.update_stream(xref, bytes(cont))  # rewrite stream
        page = self.doc.reload_page(page)  # reload the page
        self.last_pno = -1
        self.new_image(pno + 1)  # make new bitmap from page
        self.btn_Save.Enable()
        self.t_Save.Label = "Save changed file."
        evt.Skip()
        return

    def on_refresh_image(self, evt):
        """Remove image invocation command and insert new one.

        This should make the image position changeable in corner cases.
        A valid image rectangle must however exist to be successful!
        """
        pno = getint(self.TextToPage.Value) - 1
        page = self.doc[pno]
        key = self.imgName.Value  # name of image
        d = self.page_images[key]
        xref = d["xref"]
        begin = d["begin"]
        end = d["end"]
        rect = d["bbox"]  # get width / height from previous rectangle
        factor = max(rect.width, rect.height)
        fw = rect.width / factor  # calculate width / height ratio
        fh = rect.height / factor
        tar_rect = rect * ~page.transformation_matrix
        matrix = calc_matrix(fw, fh, tar_rect, 0)
        # we have the matrix, now read /Contents stream
        cont = bytearray(self.doc.xref_stream(xref))  # modifyable version!
        cont[begin:end] = b""  # remove old display command
        self.doc.update_stream(xref, bytes(cont))
        new_cmd = b"\nq\n%g %g %g %g %g %g cm " % tuple(matrix)
        new_cmd += b"/%s Do\nQ\n" % key.encode()
        if not page.is_wrapped:
            page.wrap_contents()
        fitz.TOOLS._insert_contents(page, new_cmd, 1)
        page.clean_contents()
        page = self.doc.reload_page(page)
        self.last_pno = -1
        self.new_image(pno + 1)
        self.btn_Save.Enable()
        self.t_Save.Label = "Save changed file."
        evt.Skip()
        return

    def on_remove_image(self, evt):
        """Delete image from page completely.

        This works by removing substring '/name Do' from
        resp. /Contents object and refresh image.
        """
        pno = getint(self.TextToPage.Value) - 1
        page = self.doc[pno]
        key = self.imgName.Value  # name of image
        d = self.page_images[key]
        xref = d["xref"]
        begin = d["begin"]
        end = d["end"]
        cont = bytearray(self.doc.xref_stream(xref))  # modifyable version!
        cont[begin:end] = b""
        self.doc.update_stream(xref, bytes(cont))
        page.clean_contents()
        page = self.doc.reload_page(page)
        self.last_pno = -1
        self.last_image = None
        self.new_image(pno + 1)
        self.btn_Save.Enable()
        self.t_Save.Label = "Save changed file."
        evt.Skip()
        return

    def on_image_changed(self, evt):
        # change image rectangle
        if not self.can_change_image:
            evt.Skip()
            return
        r = wx.Rect(
            self.bboxLeft.Value,
            self.bboxTop.Value,
            self.bboxWidth.Value,
            self.bboxHeight.Value,
        )
        self.refresh_fitz_labels(r)
        self.redraw_bitmap()
        self.draw_rect(r.x, r.y, r.width, r.height, "RED")
        self.btn_Update.Enable()
        evt.Skip()
        return

    def on_save_file(self, evt):
        indir, infile = os.path.split(self.doc.name)
        odir = indir
        ofile = infile
        if self.doc.needs_pass or not self.doc.can_save_incrementally():
            ofile = ""
        sdlg = wx.FileDialog(
            self, "Specify Output", odir, ofile, "PDF files (*.pdf)|*.pdf", wx.FD_SAVE
        )
        if sdlg.ShowModal() == wx.ID_CANCEL:
            evt.Skip()
            return
        outfile = sdlg.GetPath()
        if self.doc.needs_pass or not self.doc.can_save_incrementally():
            title = "Repaired / decrypted PDF requires new output file"
            while outfile == self.doc.name:
                sdlg = wx.FileDialog(
                    self, title, odir, "", "PDF files (*.pdf)|*.pdf", wx.FD_SAVE
                )
                if sdlg.ShowModal() == wx.ID_CANCEL:
                    evt.Skip()
                    return
                outfile = sdlg.GetPath()
        if outfile == self.doc.name:
            self.doc.saveIncr()  # equal: update input file
        else:
            self.doc.save(outfile, garbage=3, deflate=True)

        sdlg.Destroy()
        self.btn_Save.Disable()
        self.t_Save.Label = ""
        self.btn_Update.Disable()
        evt.Skip()
        return

    def on_new_image(self, evt):
        path = evt.GetPath()
        pno = getint(self.TextToPage.Value) - 1
        page = self.doc[pno]
        w = min(page.rect.width / 2, 200)
        h = min(page.rect.height / 2, 200)
        r = fitz.Rect(0, 0, w, h)
        try:
            page.insert_image(r, filename=path)
        except Exception as exc:
            self.message.Label = "Unsupported image file"
            print(str(exc), r)
            evt.Skip()
            return

        page = self.doc.reload_page(page)
        self.last_image = -1
        self.last_pno = -1
        self.btn_Save.Enable()
        self.new_image(pno + 1)
        evt.Skip()
        return

    def on_left_up(self, evt):
        self.dragging_img = False
        self.dragstart_x = -1
        self.dragstart_y = -1
        self.resize_rect = False
        self.PDFimage.SetCursor(cur_norm)
        evt.Skip()
        return

    def on_left_down(self, evt):
        if not self.can_change_image:
            evt.Skip()
            return
        pos = evt.GetPosition()
        in_rect = self.img_rect.Contains(pos)
        in_brect = self.img_bottom_rect.Contains(pos)

        if in_brect:
            self.resize_rect = True
            self.current_idx = in_brect
            self.btn_Update.Enable()
            evt.Skip()
            return

        if in_rect:
            self.dragging_img = True  # we are about to drag
            r = self.img_rect  # the wx.Rect we will be dragging
            self.dragstart_x = pos.x - r.x  # delta to left
            self.dragstart_y = pos.y - r.y  # delta to top

        if not in_rect:
            self.current_idx = False
            evt.Skip()
            return
        self.current_idx = in_rect
        r = self.img_rect
        self.bboxLeft.SetValue(r.x)
        self.bboxTop.SetValue(r.y)
        self.bboxHeight.SetValue(r.Height)
        self.bboxWidth.SetValue(r.Width)
        self.refresh_fitz_labels(r)
        self.draw_rect(r.x, r.y, r.width, r.height, "RED")
        self.btn_Update.Enable()
        evt.Skip()
        return

    def enable_update(self):
        self.can_change_image = True
        self.bboxLeft.Enable()
        self.bboxTop.Enable()
        self.bboxHeight.Enable()
        self.bboxWidth.Enable()
        self.imgRotation.Enable()
        self.t_Update.Label = ""
        self.btn_Refresh.Disable()

    def disable_update(self):
        self.can_change_image = False
        self.bboxLeft.Disable()
        self.bboxTop.Disable()
        self.bboxHeight.Disable()
        self.bboxWidth.Disable()
        self.imgRotation.Disable()
        self.btn_Update.Disable()
        self.btn_Refresh.Enable()

    def redraw_bitmap(self):
        """Refresh bitmap image."""
        w = self.bitmap.Size[0]
        h = self.bitmap.Size[1]
        x = y = 0
        rect = wx.Rect(x, y, w, h)
        bm = self.bitmap.GetSubBitmap(rect)
        dc = wx.ClientDC(self.PDFimage)  # make a device control out of img
        dc.DrawBitmap(bm, x, y)  # refresh bitmap before draw
        return

    def draw_rect(self, x, y, w, h, c):
        dc = wx.ClientDC(self.PDFimage)
        dc.SetPen(wx.Pen(c, width=1))
        dc.SetBrush(wx.Brush(c, style=wx.BRUSHSTYLE_TRANSPARENT))
        dc.DrawRectangle(x, y, w, h)
        return

    def on_next_image(self, evt):
        self.redraw_bitmap()
        img = self.imgName.Value
        keys = list(self.page_images.keys())
        idx = keys.index(img) + 1
        self.fill_img_details(idx % len(keys))
        self.btn_Update.Disable()
        evt.Skip()
        return

    def clear_img_details(self):
        self.imgName.Value = ""
        self.img_count.Label = ""
        self.btn_next_image.Disable()
        self.imgRotation.SetSelection(0)
        self.bboxLeft.SetValue("")
        self.bboxTop.SetValue("")
        self.bboxHeight.SetValue("")
        self.bboxWidth.SetValue("")
        self.btn_Update.Disable()
        self.btn_Remove.Disable()
        self.btn_Refresh.Disable()
        self.rectX0.Label = ""
        self.rectY0.Label = ""
        self.rectX1.Label = ""
        self.rectY1.Label = ""
        self.t_Update.Label = ""
        self.t_Save.Label = ""
        self.message.Label = ""
        self.resize_rect = False
        return

    def fill_img_details(self, idx):
        keys = list(self.page_images.keys())
        try:
            key = keys[idx]
        except:
            key = keys[0]
            self.last_image = 0
        imno = len(keys) if idx == -1 else idx + 1
        self.img_count.Label = "Image: %i/%i" % (imno, len(keys))
        self.btn_next_image.Enable()
        self.imgName.Value = key
        d = self.page_images[key]
        i = degrees.index(str(d["deg"]))
        self.rotation = d["deg"]
        rect = d["bbox"]
        if not rect.is_infinite:
            self.img_rect = bbox = self.Rect_to_wxRect(rect)
            br = bbox.BottomRight
            br2 = wx.Point(br.x + self.sense, br.y + self.sense)
            tl2 = wx.Point(br.x - self.sense, br.y - self.sense)
            self.img_bottom_rect = wx.Rect(tl2, br2)
            x, y, _, _ = bbox
            w = bbox.width
            h = bbox.height
            self.imgRotation.SetSelection(i)
            self.bboxTop.SetValue(y)
            self.bboxLeft.SetValue(x)
            self.bboxWidth.SetValue(w)
            self.bboxHeight.SetValue(h)
            self.rectX0.Label = "%g" % rect.x0
            self.rectY0.Label = "%g" % rect.y0
            self.rectX1.Label = "%g" % rect.x1
            self.rectY1.Label = "%g" % rect.y1
            self.draw_rect(x, y, w, h, "RED")

        if d["start"] > 0:
            self.btn_Refresh.Enable()
        else:
            self.btn_Refresh.Disable()

        if d["msg"] != None:
            self.message.Label = d["msg"]
            self.t_Update.Label = "Cannot modify"
            self.disable_update()
        else:
            self.message.Label = ""
            self.t_Update.Label = ""
            self.enable_update()

        if d["end"] > 0:
            self.btn_Remove.Enable()
        else:
            self.btn_Remove.Disable()

        return

    def Rect_to_wxRect(self, fr):
        """ Return a zoomed wx.Rect for given fitz.Rect."""
        r = (fr * self.zoom).irect  # zoomed IRect
        return wx.Rect(r.x0, r.y0, r.width, r.height)  # wx.Rect version

    def wxRect_to_Rect(self, wr):
        """ Return a shrunk fitz.Rect for given wx.Rect."""
        r = fitz.Rect(wr.x, wr.y, wr.x + wr.width, wr.y + wr.height)
        return r * self.shrink  # shrunk fitz.Rect version

    # -------------------------------------------------------------------------
    # Read and render a page
    # -------------------------------------------------------------------------
    def new_image(self, pno):
        if pno == self.last_pno:
            return
        self.last_pno = pno
        self.img_rect = wx.Rect()
        self.img_bottom_rect = wx.Rect()
        self.bitmap = self.pdf_show(pno)  # get page bitmap

        # following takes care of changed page sizes
        bm = wx.Bitmap(self.bitmap.Size[0], self.bitmap.Size[1], self.bitmap.Depth)
        self.PDFimage.SetBitmap(bm)  # empty bitmap for adjustment
        self.Fit()  # tell dialog to fit its kids
        self.Layout()  # probably not needed
        # end of page adjustments

        self.PDFimage.SetBitmap(self.bitmap)  # put it in screen
        self.btn_Update.Disable()

        if len(self.page_images.keys()) == 0:
            self.clear_img_details()
        else:
            i = 0 if self.last_image == None else self.last_image
            self.fill_img_details(i)
        return

    def pdf_show(self, pno):
        page = self.doc[getint(pno) - 1]  # load page & get Pixmap
        width = page.rect.width
        height = page.rect.height
        if width / height < MAX_WIDTH / MAX_HEIGHT:
            zoom = MAX_HEIGHT / height
        else:
            zoom = MAX_WIDTH / width
        self.zoom = fitz.Matrix(zoom, zoom)
        self.shrink = ~self.zoom
        pix = page.get_pixmap(matrix=self.zoom, alpha=False)
        bmp = wx.Bitmap.FromBuffer(pix.w, pix.h, pix.samples)
        paper = FindFit(page.rect.width, page.rect.height)
        self.paperform.Label = "Page format: " + paper
        self.page_images = get_images(page)
        self.page_height = page.rect.height
        return bmp

    def decrypt_doc(self):
        # let user enter document password
        pw = None
        dlg = wx.TextEntryDialog(
            self,
            "Please Enter Password",
            "Document needs password to open",
            "",
            style=wx.TextEntryDialogStyle | wx.TE_PASSWORD,
        )
        while pw is None:
            rc = dlg.ShowModal()
            if rc == wx.ID_OK:
                pw = str(dlg.GetValue().encode("utf-8"))
                self.doc.authenticate(pw)
            else:
                return
            if self.doc.is_encrypted:
                pw = None
                dlg.SetTitle("Wrong password. Enter correct one or cancel.")
        return


# ----------------------------------------------------------------------------
# main program
# ----------------------------------------------------------------------------
# Show a standard FileSelect dialog to choose a file
# ----------------------------------------------------------------------------
# Wildcard: only offer PDF files
wild = "*.pdf"

# ----------------------------------------------------------------------------
# define file selection dialog
# ----------------------------------------------------------------------------
dlg = wx.FileDialog(
    None,
    message="Choose a file to display",
    wildcard=wild,
    style=wx.FD_OPEN | wx.FD_CHANGE_DIR,
)

# We got a file only when one was selected and OK pressed
if dlg.ShowModal() == wx.ID_OK:
    filename = dlg.GetPath()
else:
    filename = None

# destroy this dialog
dlg.Destroy()

# only continue if we have a filename
if filename:
    # create the dialog
    dlg = PDFdisplay(None, filename)
    # show it - this will only return for final housekeeping
    rc = dlg.ShowModal()
app = None
