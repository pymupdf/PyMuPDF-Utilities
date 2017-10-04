from __future__ import print_function
import fitz
"""
PyMuPDF utility
----------------
For a given entry in a page's getImagleList() list, function "recoverpix"
returns the modified pixmap. This can then e.g. be saved to disk.
The item's first two entries are PDF xref numbers. The first one is the image in
question, the second one may be 0 or the object id of a soft-image mask. In this
case, we assume it being a sequence of alpha bytes belonging to our image.
We then create a new Pixmap giving it these alpha values, and return it.
The caller of function recoverpix should take special care of CMYK pixmaps
(which cannot be saved using writePNG directly).
"""

def recoverpix(doc, item):
    x = item[0]  # xref of PDF image
    s = item[1]  # xref of its /SMask
    pix1 = fitz.Pixmap(doc, x)
    if s == 0:
        return pix1 # no special handling
    pix2 = fitz.Pixmap(doc, s)  # create pixmap of /SMask entry
    # check that we are safe
    if not (pix1.irect == pix2.irect and \
            pix1.alpha == pix2.alpha == 0 and \
            pix2.n == 1):
        pix2 = None
        return pix1
    pix = fitz.Pixmap(pix1)  # copy of pix1, alpha channel added
    pix.setAlpha(pix2.samples)  # treat pix2.samples as alpha value
    pix1 = pix2 = None  # free temp pixmaps
    return pix

doc = fitz.open("test.pdf")
il = doc.getPageImageList(0)  # just process page 0
# put following in a page loop if total doc needs be scanned
for img in il:
    pix = recoverpix(doc, img)
    # we may need to adjust something for CMYK pixmaps here:
    if pix.colorspace.n > 3:  # this is CMYK
        pixc = fitz.Pixmap(fitz.csRGB, pix, 1) # create converted copy
        pix = None
        pix = pixc
    pix.writePNG("img-%i-%s.png" % (page.number, img[7])) # save pixmap
