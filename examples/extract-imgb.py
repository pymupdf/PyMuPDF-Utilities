from __future__ import print_function
import fitz
import os, sys, time
import PySimpleGUI as sg  # show a pogress  meter with this

"""
This demo extracts all images of a PDF as PNG files, whether they are
referenced by pages or not.
It scans through all objects and selects /Type/XObject with /Subtype/Image.
So runtime is determined by number of objects and image volume.

Technically, images with a specified /SMask are correctly recovered and
should appear as originally stored.

Usage:
-------
python extract_img.py input.pdf img-prefix

The focus of this script is to be as fault-tolerant as possible:
-----------------------------------------------------------------
* It can cope with invalid PDF page trees, invalid PDF objects and more
* It ignores images with very small dimensions (<= 100 pixels side length)
* It ignores very small image file sizes (< 2 KB)
* It ignores too well-compressible images, assuming these are insignificant,
  like unicolor images: image size : pixmap size <= 5%

Adjust / omit these limits as required.

Found images are stored in a directory one level below the input PDF, called
"images" (created if not existing). Adjust this as appropriate.

Dependencies
------------
PyMuPDF v1.13.17+
"""

print(fitz.__doc__)
if not tuple(map(int, fitz.version[0].split("."))) >= (1, 13, 17):
    raise SystemExit("require PyMuPDF v1.13.17+")

dimlimit = 100  # each image side must be greater than this
relsize = 0.05  # image : pixmap size ratio must be larger than this (5%)
abssize = 2048  # absolute image size limit 2 KB: ignore if smaller
imgdir = "images"  # found images are stored here

if not os.path.exists(imgdir):
    os.mkdir(imgdir)


def recoverpix(doc, xref, item):
    """Return pixmap for item, if an /SMask exists.
    """

    def getimage(pix):
        if pix.colorspace.n != 4:
            return pix
        tpix = fitz.Pixmap(fitz.csRGB, pix)
        return tpix

    s = item["smask"]  # xref of its /SMask

    try:
        pix1 = fitz.Pixmap(doc, xref)  # make pixmap from image
    except:
        return None  # skip if error

    try:
        pix2 = fitz.Pixmap(doc, s)  # create pixmap of /SMask entry
    except:
        print("cannot create mask %i for image %i" % (s, xref))
        return getimage(pix1)  # return w/ failed transparency

    # check that we are safe
    if not (pix1.irect == pix2.irect and pix1.alpha == pix2.alpha == 0 and pix2.n == 1):
        return getimage(pix1)
    pix = fitz.Pixmap(pix1)  # copy of pix1, alpha channel added
    pix.setAlpha(pix2.samples)  # treat pix2.samples as alpha values
    pix1 = pix2 = None  # free temp pixmaps
    return getimage(pix)


# ------------------------------------------------------------------------------
# Main Program
# ------------------------------------------------------------------------------

fname = sys.argv[1] if len(sys.argv) == 2 else None
if not fname:
    fname = sg.PopupGetFile("Select file:", title="PyMuPDF PDF Image Extraction")
if not fname:
    raise SystemExit()

fpref = "img"
doc = fitz.open(fname)
img_ocnt = 0
img_icnt = 0
lenXREF = doc._getXrefLength()  # PDF object count - do not use entry 0!

# display some file info
print("")
print(__file__, "PDF: %s, pages: %i, objects: %i" % (fname, len(doc), lenXREF - 1))

t0 = time.time()  # start the timer

smasks = []  # stores xrefs of /SMask objects
# ------------------------------------------------------------------------------
# loop through PDF images
# ------------------------------------------------------------------------------
for xref in range(1, lenXREF):  # scan through all PDF objects
    sg.QuickMeter(
        "Extract Images",  # show our progress
        xref,
        lenXREF,
        "*** Scanning Cross Reference ***",
    )

    if xref in smasks:  # ignore smasks
        continue

    imgdict = doc.extractImage(xref)

    if not imgdict:  # not an image
        continue

    img_icnt += 1  # increase read images counter

    smask = imgdict["smask"]
    if smask > 0:  # store /SMask xref
        smasks.append(smask)

    width = imgdict["width"]
    height = imgdict["height"]
    ext = imgdict["ext"]

    if min(width, height) <= dimlimit:  # rectangle edges too small
        continue

    imgdata = imgdict["image"]  # image data
    l_imgdata = len(imgdata)  # length of data
    if l_imgdata <= abssize:  # image too small to be relevant
        continue

    if smask > 0:  # has smask: need use pixmaps
        pix = recoverpix(doc, xref, imgdict)  # create pix with mask applied
        if not pix:  # something went wrong
            continue
        ext = "png"
        imgdata = pix.getPNGData()
        l_samples = len(pix.samples)
        l_imgdata = len(imgdata)
    else:
        c_space = max(1, imgdict["colorspace"])  # get the colorspace n
        l_samples = width * height * c_space  # simulated samples size

    if l_imgdata / l_samples <= relsize:  # seems to be unicolor image
        continue

    # now we have an image worthwhile dealing with
    img_ocnt += 1

    imgn1 = fpref + "-%i.%s" % (xref, ext)
    imgname = os.path.join(imgdir, imgn1)
    ofile = open(imgname, "wb")
    ofile.write(imgdata)
    ofile.close()

# now delete any /SMask files not filtered out before
removed = 0
if len(smasks) > 0:
    imgdir_ls = os.listdir(imgdir)
    for smask in smasks:
        imgn1 = fpref + "-%i" % smask
        for f in imgdir_ls:
            if f.startswith(imgn1):
                imgname = os.path.join(imgdir, f)
                os.remove(imgname)
                removed += 1

t1 = time.time()

print(img_icnt, "found images")
print((img_ocnt - removed), "extracted images")
print(len(smasks), "skipped smasks")
print(removed, "removed smasks")
print("total time %g sec" % (t1 - t0))
