"""
Created on Thu Jan  3 07:05:17 2019

@author: Jorj
@copyright: (c) 2019 Jorj X. McKie
@license: GNU GPL 3.0

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

# define some global constants
gold = (1,1,0)
blue = (0,0,1)
pagerect = fitz.Rect(0, 0, 400, 400)   # dimension of our image

mp = fitz.Point(pagerect.width/2.,     # center of the page
                pagerect.height/2.)

r = fitz.Rect(mp, mp + (80, 80))       # rext for text box

text = "Just some demo text, to be filled in a rect."

textpoint = fitz.Point(40, 50)         # start position of this text:
itext = "X-Shear Morphing:\nfitz.Matrix(%g, 0, 1)"

#------------------------------------------------------------------------------
# make one page
#------------------------------------------------------------------------------
def make_page(beta):
    """Create a dummy PDF with a page, put in a box filled with above text,
    and also insert some explanation. Then x-shear the text box around
    its top-left corner by given value beta. The resulting page's image
    is returned as a PNG stream, and the PDF discarded again.
    This functions execution time determines the overall "frames" per
    second ration.
    """
    doc = fitz.open()
    page = doc.newPage(width=pagerect.width, height=pagerect.height)
    mat = fitz.Matrix(beta * 0.01, 0, 1)
    img = page.newShape()
    img.drawRect(r)
    img.finish(fill=gold, color=blue, width=0.3, morph = (r.tl, mat))
    img.insertText(textpoint, itext % (beta*0.01), fontname="cobo", fontsize=20)
    img.insertTextbox(r, text, fontsize=15, rotate=90, morph = (r.tl, mat))
    img.commit()
    pix = page.getPixmap(alpha=False)
    return pix.getImageData("pgm")

#------------------------------------------------------------------------------
# main program
#------------------------------------------------------------------------------
form = sg.FlexForm("Demo: X-Shear-Morphing of a Text Box") # define form
png = make_page(0)                     # create first picture
img = sg.Image(data = png)             # define form image element
layout = [[img]]                       # minimal layout
form.Layout(layout)                    # layout the form

loop_count = 1                         # count the number of loops
t0 = mytime()               # start a timer
form.Show(non_blocking=True)           # and start showing it
i = 0
add = 1

while True:                            # loop forever
    png = make_page(i)                 # make next picture
    try:                               # guard against form closure
        img.Update(data=png)           # put in new picture
    except:
        break                          # user is fed up seeing this
    form.Refresh()                     # show updated
    loop_count += 1                    # tally the loops
    i += add
    if i >= 150:
        add = -1
        continue
    if i <= -150:
        add = 1

t1 = mytime()
fps = round(loop_count / (t1 - t0), 1)
sg.Popup("This was shown with %g frames per second." % fps,
         title="Statistics",
         auto_close=True,
         auto_close_duration=5)