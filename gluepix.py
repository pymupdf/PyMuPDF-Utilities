from __future__ import print_function
import sys, time
import fitz
"""
PyMuPDF utility
----------------
For a given entry in a page's getImagleList() list, function "recoverpix"
returns either the raw image data, or a modified pixmap if an /SMask entry
exists.
The item's first two entries are PDF xref numbers. The first one is the image in
question, the second one may be 0 or the object id of a soft-image mask. In this
case, we assume it being a sequence of alpha bytes belonging to our image.
We then create a new Pixmap giving it these alpha values, and return it.
If the result pixmap is CMYK, it will be converted to RGB first.

"""

def recoverpix(doc, item):
    x = item[0]                   # xref of PDF image
    s = item[1]                   # xref of its /SMask
    if s == 0:                    # no smask: use direct image output
        return doc.extractImage(x)

    # we need to reconstruct the alpha channel with the smask
    pix1 = fitz.Pixmap(doc, x)
    pix2 = fitz.Pixmap(doc, s)    # create pixmap of /SMask entry

    # sanity check
    if not (pix1.irect == pix2.irect and \
            pix1.alpha == pix2.alpha == 0 and \
            pix2.n == 1):
        pix2 = None
        return pix1

    pix = fitz.Pixmap(pix1)       # copy of pix1, alpha channel added
    pix.setAlpha(pix2.samples)    # treat pix2.samples as alpha value
    pix1 = pix2 = None            # free temp pixmaps

    # we may need to adjust something for CMYK pixmaps here:
    if pix.colorspace.n > 3:
        pixc = fitz.Pixmap(fitz.csRGB, pix, 1) # create converted copy
        pix = None
        pix = pixc
    return pix

t0 = time.time()
fname = sys.argv[1]
doc = fitz.open(fname)
xreflist = []
for pno in range(len(doc)):
    il = doc.getPageImageList(pno)
    for img in il:
        xref = img[0]
        if xref in xreflist:
            continue
        xreflist.append(xref)
        pix = recoverpix(doc, img)
        if type(pix) is dict:     # we got a raw image
            ext = pix["ext"]
            imgdata = pix["image"]
            fout = open("img-%i-%i.%s" % (pno, xref, ext), "wb")
            fout.write(imgdata)
            fout.close()
        else:                     # we got a pixmap
            pix.writePNG("img-%i-%i.png" % (pno, xref)) # save pixmap

t1 = time.time()
print(len(xreflist), "images extracted")
print ("total time %g sec" % (t1-t0))