"""
Created on Thu Jan  3 07:05:17 2019

@author: Jorj
@copyright: (c) 2019 Jorj X. McKie
@license: GNU AFFERO GPL V3

Purpose
--------
Demonstrate the effect of morphing a text box. The morphing parameters are the
box's top-left edge and a shearing matrix in x-axis direction.

For demonstration purposes, text box creation is placed in a function, which
accepts the desired parameter as an integer value. This value, divided by 100,
is used as the shearing value.
It then creates a dummy temporary PDF with one page containing stuff we want
to show. It returns a PNG image of this page.

The function is called by the main program in an "endless" loop, passing in
angles in range 0 to 360 degrees. The image is displayed using PySimpleGUI.

Notes
------
* We are using Tkinter's capability to directly accept PNG image streams, which
  is supported since version Tk 8.6.

* Significant speed improvements at creating Tkinter PhotoImage objects can be
  achieved be using Pillow / PIL instead of Tkinter's own support.

* We are not slowing down the speed of showing new images (i.a.w. "frames per
  second"). The statistics displayed at end of program can hence be used as a
  performance indicator.
"""
import os
import time

import fitz
import PySimpleGUI as sg

mytime = time.perf_counter
print(fitz.__doc__)

if not list(map(int, fitz.VersionBind.split("."))) >= [1, 14, 5]:
    raise SystemExit(
        "need PyMuPDF v1.14.5 for this script"
    )  # define some global constants
gold = (1, 1, 0)
blue = (0, 0, 1)
pagerect = fitz.Rect(0, 0, 400, 400)  # dimension of our image

mp = fitz.Point(pagerect.width / 2.0, pagerect.height / 2.0)  # center of the page
pwidth = pagerect.width
pheight = pagerect.height
r = fitz.Rect(mp, mp + (80, 80))  # rext for text box
tl = r.tl
text = "Just some demo text, to be filled in a rect."

textpoint = fitz.Point(40, 50)  # start position of this text:
itext = "X-Shear Morphing:\nfitz.Matrix(%g, 0, 1)"

# ------------------------------------------------------------------------------
# make one page
# ------------------------------------------------------------------------------
def make_page(beta):
    """Create a dummy PDF with a page, put in a box filled with above text,
    and also insert some explanation. Then x-shear the text box around
    its top-left corner by given value beta. The resulting page's image
    is returned as a PNG stream, and the PDF discarded again.
    This functions execution time determines the overall "frames" per
    second ration.
    """
    doc = fitz.open()
    page = doc.new_page(width=pwidth, height=pheight)
    mat = fitz.Matrix(beta * 0.01, 0, 1)
    img = page.new_shape()
    img.draw_rect(r)
    img.finish(fill=gold, color=blue, width=0.3, morph=(tl, mat))
    img.insert_text(textpoint, itext % (beta * 0.01), fontname="cobo", fontsize=20)
    img.insert_textbox(
        r, text, fontsize=15, rotate=90, morph=(r.tl, mat), lineheight=1.2
    )
    img.commit()
    return page.get_pixmap().tobytes("pgm")


# ------------------------------------------------------------------------------
# main program
# ------------------------------------------------------------------------------

png = make_page(0)  # create first picture
img = sg.Image(data=png)  # define form image element
layout = [[img]]  # minimal layout
form = sg.Window(
    "Demo: X-Shear-Morphing of a Text Box", layout, finalize=True
)  # define form

loop_count = 1  # count the number of loops
t0 = mytime()  # start a timer
i = 0
add = 1

while True:  # loop forever
    event, values = form.Read(timeout=0)
    if event is None:
        break
    png = make_page(i)  # make next picture
    try:  # guard against form closure
        img.update(data=png)  # put in new picture
    except:
        break  # user is fed up seeing this
    loop_count += 1  # tally the loops
    i += add
    if i >= 150:
        add = -1
        continue
    if i <= -150:
        add = 1

t1 = mytime()
fps = round(loop_count / (t1 - t0), 1)
script = os.path.basename(__file__)
print("'%s' was shown with %g frames per second." % (script, fps))
