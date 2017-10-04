from __future__ import print_function
import fitz
"""
PyMuPDF utility
----------------
For a given entry in a page's getImagleList() list, function "recoverpix"
returns the PNG image. This can then e.g. be saved to disk.
The item's first two entries are PDF xref numbers. The first one is the image in
question, the second one may be 0 or the object id of a soft-image mask. In this
case, we assume it being a sequence of alpha bytes belonging to our image.
We then create a new Pixmap giving it these alpha values, and return the PNG
image of it.
This an intermediate solution while PyMuPDF is developing a better one.
So currently, we only support RGB images. A final PyMuPDF solution should look
like this:
(1) A new Pixmap creation method, which takes a zero-alpha input and
    creates a copy of it with an alpha channel (filled with 0xff).
(2) A new Pixmap method allowing to fill the alpha channel with the contents
    of a given sequence of bytes.
"""

def recoverpix(doc, item):
    x = item[0]  # xref of PDF image
    s = item[1]  # xref of its /SMask
    pix1 = fitz.Pixmap(doc, x)
    if s == 0:
        return pix1 # no special handling
    pix2 = fitz.Pixmap(doc, s)  # create pixmap of /SMask entry
    pix = fitz.Pixmap(pix1)  # copy of pix1 plus alpha channel
    pix.setAlpha(pix2.samples)  # treat pix2.samples as alpha value
    pix1 = pix2 = None  # free temp pixmaps
    return pix

doc = fitz.open("test.pdf")
il = doc.getPageImageList(0)  # just process page 0
for img in il:
    pix = recoverpix(doc, img)
    pix.writePNG(img[7] + ".png") # save pixmap
