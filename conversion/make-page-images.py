"""
Basic script to convert pages of an arbitrary document to PNG images.

All MuPDF document types are supported: PDF, XPS, EPUB, etc.
Page images are stored in the script's folder and named "page-0001.png",
"page-0002.png".

Desired resolution can be chosen by setting the "DPI" variable.
"""
import sys
import fitz

filename = sys.argv[1]
doc = fitz.open(filename)
DPI = 300  # the desired image resolution
ZOOM = DPI / 72  # zoom factor, standard dpi is 72
magnify = fitz.Matrix(ZOOM, ZOOM)  # takes care of zooming
for page in doc:
    pix = page.get_pixmap(matrix=magnify)  # make page image
    pix.set_dpi(DPI, DPI)  # store dpi info in image
    pix.save("page-%04i.png" % (page.number + 1))

# generates images named page-0001.png, page-0002.png, ...
