from __future__ import print_function

import io
import os
import sys
import time

import fitz
import PySimpleGUI as sg
from PIL import Image

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

Dependencies
------------
PyMuPDF v1.13.17+, Pillow

"""
print(fitz.__doc__)

if not tuple(map(int, fitz.version[0].split("."))) >= (1, 13, 17):
    raise SystemExit("require PyMuPDF v1.13.17+")

dimlimit = 0  # 100  # each image side must be greater than this
relsize = 0  # 0.05  # image : pixmap size ratio must be larger than this (5%)
abssize = 0  # 2048  # absolute image size limit 2 KB: ignore if smaller
imgdir = "images"  # found images are stored in this subfolder

if not os.path.exists(imgdir):
    os.mkdir(imgdir)


def recoverpix(doc, item):
    x = item[0]  # xref of PDF image
    s = item[1]  # xref of its /SMask
    if s == 0:  # no smask: use direct image output
        return doc.extractImage(x)

    # we need to reconstruct an alpha channel with the smask
    fpx = io.BytesIO(doc.extractImage(x)["image"])
    fps = io.BytesIO(doc.extractImage(s)["image"])
    img0 = Image.open(fpx)
    mask = Image.open(fps)
    img = Image.new("RGBA", img0.size)
    img.paste(img0, None, mask)
    bf = io.BytesIO()
    img.save(bf, "png")
    return {"ext": "png", "colorspace": 3, "image": bf.getvalue()}


fname = sys.argv[1] if len(sys.argv) == 2 else None
if not fname:
    fname = sg.PopupGetFile("Select file:", title="PyMuPDF PDF Image Extraction")
if not fname:
    raise SystemExit()

t0 = time.time()
doc = fitz.open(fname)

page_count = len(doc)  # number of pages

xreflist = []
imglist = []
for pno in range(page_count):
    sg.QuickMeter(
        "Extract Images",  # show our progress
        pno + 1,
        page_count,
        "*** Scanning Pages ***",
    )

    il = doc.getPageImageList(pno)
    imglist.extend([x[0] for x in il])
    for img in il:
        xref = img[0]
        if xref in xreflist:
            continue
        width = img[2]
        height = img[3]
        if min(width, height) <= dimlimit:
            continue
        pix = recoverpix(doc, img)
        n = pix["colorspace"]
        imgdata = pix["image"]

        if len(imgdata) <= abssize:
            continue
        if len(imgdata) / (width * height * n) <= relsize:
            continue

        imgfile = os.path.join(imgdir, "img-%i.%s" % (xref, pix["ext"]))
        fout = open(imgfile, "wb")
        fout.write(imgdata)
        fout.close()
        xreflist.append(xref)

t1 = time.time()
imglist = list(set(imglist))
print(len(set(imglist)), "images in total")
print(len(xreflist), "images extracted")
print("total time %g sec" % (t1 - t0))
