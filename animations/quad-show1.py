"""
Created on Thu Jan  3 07:05:17 2019

@author: Jorj
@copyright: (c) 2019 Jorj X. McKie
@license: GNU AFFERO GPL V3

Purpose
--------
Visualize function "drawOval" by using a quadrilateral (tetrapod) as parameter.

For demonstration purposes, text box creation is placed in a function, which
accepts the desired parameter as float value. This value controls positioning
some egdes of the quad.
It then creates a dummy temporary PDF with one page, containing stuff we want
to show and returns an image of it.

The function is called by the main program in an "endless" loop, passing in
float values. The image is displayed using PySimpleGUI.

Notes
------
* Changed generated page image format to "PPM", which is very much faster than
  "PNG" both, in terms of creation and reading by tkinter. It also makes us
  independent from the tkinter version used.
* We are not slowing down the speed of showing new images (= "frames per
  second"). The statistics displayed at end of program can hence be used as a
  performance indicator.
"""
import os
import time

import fitz
import PySimpleGUI as sg

mytime = time.perf_counter

if not list(map(int, fitz.VersionBind.split("."))) >= [1, 14, 5]:
    raise SystemExit("need PyMuPDF v1.14.5 for this script")
print(fitz.__doc__)

# ------------------------------------------------------------------------------
# make one page
# ------------------------------------------------------------------------------
def make_oval(f):
    """Make a PDF page and draw an oval inside a Quad.
    The upper left and the lower right quad points and the fill color are
    subject to a passed-in parameter. Effectively, they exchange their position,
    thus causing changes to the drawn shape.
    The resulting page picture is passed back as a PNG image and the PDF is
    discarded again. The execution speed of this function mainly determines
    the number of "frames" shown per second.
    """
    doc = fitz.open()  # dummy PDF
    page = doc.new_page(width=400, height=400)  # page dimensions as you like
    r = page.rect + (4, 4, -4, -4)
    q = r.quad  # full page rect as a quad
    q1 = fitz.Quad(
        q.lr + (q.ul - q.lr) * f, q.ur, q.ll, q.ul + (q.lr - q.ul) * f  # upper left
    )  # lower right
    # make an entertaining fill color - simulating rotation around
    # a diagonal
    c1 = min(1, f)
    c3 = min(1, max(1 - f, 0))
    fill = (c1, 0, c3)
    page.draw_oval(
        q1, color=(0, 0, 1), fill=fill, width=0.3  # blue border  # variable fill color
    )  # border width
    return page.get_pixmap().tobytes("ppm")  # return a data stream


# ------------------------------------------------------------------------------
# main program
# ------------------------------------------------------------------------------
png = make_oval(0.0)  # create first picture
img = sg.Image(data=png)  # define form image element
layout = [[img]]  # minimal layout
form = sg.Window(
    "drawOval: diagonal points exchange position", layout, finalize=True
)  # define form

loop_count = 1  # count the number of loops
t0 = mytime()  # start a timer
i = 0
add = 1

while True:  # loop forever
    event, values = form.Read(timeout=0)
    if event is None:
        break
    png = make_oval(i / 100.0)  # make next picture
    try:  # guard against form closure
        img.update(data=png)  # put in new picture
    except:
        form.close()
        break  # user is fed up seeing this

    loop_count += 1  # tally the loops
    i += add  # update the parameter
    if i >= 100:  # loop backwards from here
        add = -1
        continue
    if i <= 0:  # loop forward again
        add = +1
        i = 0

t1 = mytime()
fps = round(loop_count / (t1 - t0), 1)
script = os.path.basename(__file__)
print("'%s' was shown with %g frames per second." % (script, fps))
