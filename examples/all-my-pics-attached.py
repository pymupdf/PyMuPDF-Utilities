# -*- coding: utf-8 -*-
"""
@created: 2018-09-02 18:00:00
@author: (c) 2018 Jorj X. McKie

Embed all files from a directory
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
Take all files from a directory and attach them to pages in a new PDF.
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
        "Make a PDF from Attached Files", "Enter file directory:"
    )

if not imgdir:
    raise SystemExit()

t0 = mytime()  # set start timer

width, height = fitz.PaperSize("a6-l")  # get paper format

doc = fitz.open()  # open empty PDF
page = doc.newPage(width=width, height=height)  # make new page

# define sub rect to receive text and annotation symbols
rect = fitz.Rect(0, 0, width, height) + (36, 36, -36, -36)

imglist = os.listdir(imgdir)  # directory listing
imgcount = len(imglist)  # number of files

# calculate number of pages we will create
per_page = ((width - 72) // 25) * ((height - 36 - 56) // 35)
pages = int(round(imgcount / per_page + 0.5))

# header text
text = "Contains the following %i files from '%s':\n\n" % (imgcount, imgdir)
pno = 1

# insert header and footer
page.insertText(rect.tl, text)
page.insertText(rect.bl, "Page %i of %i" % (pno, pages))

point = rect.tl + (0, 20)  # insertion point of first symbol

for i, f in enumerate(imglist):
    path = os.path.join(imgdir, f)
    if not os.path.isfile(path):
        print("skipping non-file '%s'!" % f)
        continue

    if str is not bytes:  # show progress meter if Python v3
        psg.OneLineProgressMeter(
            "Attaching Files", i + 1, imgcount, "dir: " + imgdir, "file: " + f
        )
    else:
        print("attaching file '%s', (%i / %i)" % (f, i + 1, imgcount))

    img = open(path, "rb").read()  # file content
    page.addFileAnnot(point, img, filename=f)  # add as attachment

    point += (25, 0)  # position of next symbol
    if point.x >= rect.width:  # beyond right limit?
        point = fitz.Point(rect.x0, point.y + 35)  # start next line
    if point.y >= rect.height and i < imgcount - 1:  # beyond bottom limit?
        # prepare another page
        page = doc.newPage(width=width, height=height)
        pno += 1
        page.insertText(rect.tl, text)
        page.insertText(rect.bl, "Page %i of %i" % (pno, pages))
        point = rect.tl + (0, 20)

doc.save("all-my-pics-attached.pdf")
t1 = mytime()
print("%g" % round(t1 - t0, 3), "sec processing time")

