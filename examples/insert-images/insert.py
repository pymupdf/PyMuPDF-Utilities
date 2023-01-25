"""
Create a PDF document by inserting the images found in the input directory.
-------------------------------------------------------------------------------
License: GNU GPL V3
(c) 2018 Jorj X. McKie

Usage
-----
python insert.py

Description
-----------
The pages retain the dimensions of the image being displayed.

Dependencies
------------
PyMuPDF
PySimpleGUI, tkinter, optional: requires Python 3 if used
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
        pdfbytes = img.convert_to_pdf()  # make a PDF stream
        img.close()  # no longer needed
        imgPDF = fitz.open("pdf", pdfbytes)  # open stream as PDF
        page = doc.new_page(
            width=rect.width, height=rect.height  # new page with ...
        )  # pic dimension
        page.show_pdf_page(rect, imgPDF, 0)  # image fills the page
    except:
        print("unsupported document '%s'!" % f)

doc.save("output.pdf")
t1 = mytime()
print("%g" % (t1 - t0), "sec processing time")
