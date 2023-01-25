"""
Embed all images found in a directory
-------------------------------------------------------------------------------
License: GNU GPL V3+
(c) 2018 Jorj X. McKie

Usage
-----
python embed.py

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

doc = fitz.open()

width, height = fitz.paper_size("a4")
rect = fitz.Rect(0, 0, width, height) + (36, 36, -36, -36)
imglist = os.listdir(imgdir)
imgcount = len(imglist)

for i, f in enumerate(imglist):
    path = os.path.join(imgdir, f)
    if not os.path.isfile(path):
        print("skipping non-file '%s'!" % f)
        continue

    if str is not bytes:
        psg.OneLineProgressMeter(
            "Embedding Files", i + 1, imgcount, "dir: " + imgdir, "file: " + f
        )
    else:
        print("embedding file '%s', (%i / %i)" % (f, i + 1, imgcount))

    img = open(path, "rb").read()
    doc.embfile_add(f, img, filename=f, ufilename=f, desc=f)

page = doc.new_page()  # every doc needs at least one page

doc.save("output.pdf")
t1 = mytime()
print("%g" % round(t1 - t0, 3), "sec processing time")
