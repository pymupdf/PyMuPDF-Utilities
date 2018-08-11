from __future__ import print_function
import os, sys, time
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
if not tuple(map(int, fitz.version[0].split("."))) >= (1, 13, 17):
    raise SystemExit("require PyMuPDF v1.13.17+")

dimlimit = 100      # each image side must be greater than this
relsize  = 0.05     # image : pixmap size ratio must be larger than this (5%)
abssize  = 2048     # absolute image size limit 2 KB: ignore if smaller
imgdir   = "images" # found images are stored here

if not os.path.exists(imgdir):
    os.mkdir(imgdir)

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
imglist = []
for pno in range(len(doc)):
    il = doc.getPageImageList(pno)
    imglist.extend([x[0] for x in il])
    for img in il:
        xref = img[0]
        if xref in xreflist:
            continue
        width  = img[2]
        height = img[3]
        if min(width, height) <= dimlimit:
            continue
        pix = recoverpix(doc, img)
        if type(pix) is dict:     # we got a raw image
            ext = pix["ext"]
            imgdata = pix["image"]
            n = pix["colorspace"]
            imgfile = os.path.join(imgdir, "img-%i.%s" % (xref, ext))
        else:                     # we got a pixmap
            imgfile = os.path.join(imgdir, "img-%i.png" % xref)
            n = pix.n
            imgdata = pix.getPNGData()
    
        if len(imgdata) <= abssize:
            continue

        if len(imgdata) / (width * height * n) <= relsize:
            continue

        fout = open(imgfile, "wb")
        fout.write(imgdata)
        fout.close()
        xreflist.append(xref)

t1 = time.time()
imglist = list(set(imglist))
print(len(set(imglist)), "images in total")
print(len(xreflist), "images extracted")
print ("total time %g sec" % (t1-t0))