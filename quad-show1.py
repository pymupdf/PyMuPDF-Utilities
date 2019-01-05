"""
Created on Thu Jan  3 07:05:17 2019

@author: Jorj
@copyright: (c) 2019 Jorj X. McKie
@license: GNU GPL 3.0

Purpose
--------
Visualize function "drawOval" by using a quadrilateral (tetrapod) as parameter.

For demonstration purposes, text box creation is placed in a function, which 
accepts the desired parameter as float value. This value controls positioning
the two lower egdes of the quad.
It then creates a dummy temporary PDF with one page containing stuff we want
to show. It returns a PNG image of this page.

The function is called by the main program in an "endless" loop, passing in
float values. The image is displayed using PySimpleGUI.

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
import time
import fitz
if not list(map(int, fitz.VersionBind.split("."))) >= [1, 14, 5]:
    raise SystemExit("need PyMuPDF v1.14.5 for this script")

py2 = str is bytes
if not py2:
    import PySimpleGUI as sg
    mytime = time.perf_counter
else:
    import PySimpleGUI27 as sg
    mytime = time.clock

#------------------------------------------------------------------------------
# make one page
#------------------------------------------------------------------------------
def make_oval(f):
    """Make a PDF page and draw an oval inside a Quad.
    The lower two quad points and the fill color are subject to a passed-in
    parameter. Effectively, they exchange their position, thus causing
    changes to the drawn shape.
    The resulting page picture is passed back as a PNG image and the PDF is
    dicarded again.
    """
    doc = fitz.open()                  # dummy PDF
    page=doc.newPage(width=400,height=400)  # page dimensions as you like
    q = page.rect.quad                 # full page rect as a quad
    q1 = fitz.Quad(q.ul, 
                   q.ur,
                   q.ll + (q.lr - q.ll) * f,
                   q.ll + (q.lr - q.ll) * (1 - f))
    # make an entertaining fill color
    c1=  min(1, f)
    c3 = min(1, max(1-f, 0))
    c2 = c1*c3
    fill = (c1, c2, c3)
    page.drawOval(q1, color=(0,0,1),   # blue border
                  fill=fill,           # variable fill color
                  width=0.3)           # border width
    pix = page.getPixmap(alpha=False)  # make pixmap, no alpha
    doc.close()                        # discard PDF again
    return pix.getImageData("pgm")     # return a data stream

#------------------------------------------------------------------------------
# main program
#------------------------------------------------------------------------------
form = sg.FlexForm("drawOval: lower points exchange position") # define form
png = make_oval(0.)                    # create first picture
img = sg.Image(data = png)             # define form image element
layout = [[img]]                       # minimal layout
form.Layout(layout)                    # layout the form

loop_count = 1                         # count the number of loops
t0 = mytime()                          # start a timer
form.Show(non_blocking=True)           # and start showing it
i = 0
add = 1

while True:                            # loop forever
    png = make_oval(i/100.)            # make next picture
    try:                               # guard against form closure
        img.Update(data=png)           # put in new picture
    except:
        break                          # user is fed up seeing this
    form.Refresh()                     # show updated
    loop_count += 1                    # tally the loops
    i += add                           # update the parameter
    if i >= 150:                       # loop backwards from here
        add = -1
        continue
    if i < 0:                          # loop forward again
        add = +1
        i = 0

t1 = mytime()
fps = round(loop_count / (t1 - t0), 1)
sg.Popup("This was shown with %g frames per second." % fps,
         title="Statistics",
         auto_close=True,
         auto_close_duration=5)
