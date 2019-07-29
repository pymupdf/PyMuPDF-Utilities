"""
@created: 2018-09-02 18:00:00
@author: (c) 2018 Jorj X. McKie
Create a PDF with images as its pages
-------------------------------------------------------------------------------
Dependencies:
-------------
PyMuPDF
PySimpleGUI, optional: requires Python 3 if used

License:
--------
GNU GPL V3+

Description
------------
Take all images in a file directory and make a PDF page from each image.
Pages retain the dimension of the image shown.
"""
from __future__ import print_function
import os, time, sys, fitz

print(fitz.__doc__)

# do some adjustments whether Python v2 or v3
if str is not bytes:
    import PySimpleGUI as psg

    mytime = time.perf_counter
else:
    mytime = time.clock

rc = False
if str is bytes:
    imgdir = sys.argv[1]  # where my files are
else:
    imgdir = psg.PopupGetFolder(
        "Make a PDF from Embedded Files", "Enter file directory:"
    )

if not imgdir:
    raise SystemExit()

t0 = mytime()  # set start timer

doc = fitz.open()  # PDF with the pictures

imglist = os.listdir(imgdir)  # list of them
imgcount = len(imglist)  # pic count

for i, f in enumerate(imglist):
    path = os.path.join(imgdir, f)
    if not os.path.isfile(path):
        print("skipping non-file '%s'!" % f)
        continue

    if str is not bytes:
        psg.OneLineProgressMeter(
            "Inserting Images",  # show our progress
            i + 1,
            imgcount,
            "dir: " + imgdir,
            "file: " + f,
        )
    else:
        print("inserting file '%s', (%i / %i)" % (f, i + 1, imgcount))

    try:
        img = fitz.open(os.path.join(imgdir, f))  # open pic as document
        rect = img[0].rect  # pic dimension
        pdfbytes = img.convertToPDF()  # make a PDF stream
        img.close()  # no longer needed
        imgPDF = fitz.open("pdf", pdfbytes)  # open stream as PDF
        page = doc.newPage(
            width=rect.width, height=rect.height  # new page with ...
        )  # pic dimension
        page.showPDFpage(rect, imgPDF, 0)  # image fills the page
    except:
        print("unsupported document '%s'!" % f)

doc.save("all-my-inserted-pics.pdf")
t1 = mytime()
print("%g" % (t1 - t0), "sec processing time")

