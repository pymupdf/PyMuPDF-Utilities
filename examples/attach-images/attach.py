"""
Attach all images found in a directory
-------------------------------------------------------------------------------
License: GNU GPL V3
(c) 2018 Jorj X. McKie

Usage
-----
python attach.py

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
        "Make a PDF from Attached Files", "Enter file directory:"
    )

if not imgdir:
    raise SystemExit()

t0 = mytime()  # set start timer

width, height = fitz.paper_size("a6-l")  # get paper format

doc = fitz.open()  # open empty PDF
page = doc.new_page(width=width, height=height)  # make new page

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
page.insert_text(rect.tl, text)
page.insert_text(rect.bl, "Page %i of %i" % (pno, pages))

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
    page.add_file_annot(point, img, filename=f)  # add as attachment

    point += (25, 0)  # position of next symbol
    if point.x >= rect.width:  # beyond right limit?
        point = fitz.Point(rect.x0, point.y + 35)  # start next line
    if point.y >= rect.height and i < imgcount - 1:  # beyond bottom limit?
        # prepare another page
        page = doc.new_page(width=width, height=height)
        pno += 1
        page.insert_text(rect.tl, text)
        page.insert_text(rect.bl, "Page %i of %i" % (pno, pages))
        point = rect.tl + (0, 20)

doc.save("output.pdf")
t1 = mytime()
print("%g" % round(t1 - t0, 3), "sec processing time")
