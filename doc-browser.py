"""
@created: 2018-08-19 18:00:00

@author: (c) 2018 Jorj X. McKie

Display a PyMuPDF Document using Tkinter
-------------------------------------------------------------------------------

Dependencies:
-------------
PyMuPDF, PySimpleGUI > v2.9.0, Tkinter with Tk v8.6+, Python 3


License:
--------
GNU GPL V3+

Description
------------
Read filename from command line and start display with page 1.
Pages can be directly jumped to, or buttons for paging can be used.
For experimental / demonstration purposes, we have included options to zoom
into the four page quadrants (top-left, bottom-right, etc.).

"""
import sys
import fitz
import PySimpleGUI as sg
fname = sys.argv[1]
doc = fitz.open(fname)
page_count = len(doc)

title = "PyMuPDF display of '%s', pages: %i" % (fname, page_count)

def get_page(pno, zoom = 0):
    """Return a PNG image for a document page number. If zoom is other than 0, one of the 4 page quadrants are zoomed-in instead and the corresponding clip returned.

    """
    page = doc[pno]                    # get document page
    r = page.rect                      # page rectangle
    mp = r.tl + (r.br - r.tl) * 0.5    # rect middle point
    mt = r.tl + (r.tr - r.tl) * 0.5    # middle of top edge
    ml = r.tl + (r.bl - r.tl) * 0.5    # middle of left edge
    mr = r.tr + (r.br - r.tr) * 0.5    # middle of right egde
    mb = r.bl + (r.br - r.bl) * 0.5    # middle of bottom edge
    mat = fitz.Matrix(2, 2)            # zoom matrix
    if zoom == 1:                      # top-left quadrant
        clip = fitz.Rect(r.tl, mp)
    elif zoom == 4:                    # bot-right quadrant
        clip = fitz.Rect(mp, r.br)
    elif zoom == 2:                    # top-right
        clip = fitz.Rect(mt, mr)
    elif zoom == 3:                    # bot-left
        clip = fitz.Rect(ml, mb)
    if zoom == 0:                      # total page
        pix = page.getPixmap(alpha = False)
    else:
        pix = page.getPixmap(alpha = False, matrix = mat, clip = clip)
    return pix.getPNGData()            # return the PNG image

form = sg.FlexForm(title)

cur_page = 0
data = get_page(cur_page)              # show page 1 for start
image_elem = sg.Image(data=data)
goto = sg.InputText(str(cur_page + 1), size = (5,1), do_not_clear = True)
layout = [  
            [
             sg.ReadFormButton('Goto'),
             goto,
             sg.ReadFormButton('Next'),
             sg.ReadFormButton('Prev'),
             sg.Quit(),
             sg.Text("Zoom:"),
             sg.ReadFormButton('Top-L'),
             sg.ReadFormButton('Top-R'),
             sg.ReadFormButton('Bot-L'),
             sg.ReadFormButton('Bot-R'),
            ],
            [image_elem],
         ]

form.Layout(layout)

i = 0
oldzoom = 0                            # used for zoom on/off
# the zoom buttons work in on/off mode.
while True:
    button, value = form.Read()
    zoom = 0
    if button in (None, 'Quit'):
        break
    if button == "Goto":
        try:
            i = int(value[0]) - 1
        except:
            i = 0
    elif button == "Next":
        i += 1
    elif button == "Prev":
        i -= 1
    elif button == "Top-L":
        if oldzoom == 1:
            zoom = oldzoom = 0
        else:
            zoom = oldzoom = 1
    elif button == "Top-R":
        if oldzoom == 2:
            zoom = oldzoom = 0
        else:
            zoom = oldzoom = 2
    elif button == "Bot-L":
        if oldzoom == 3:
            zoom = oldzoom = 0
        else:
            zoom = oldzoom = 3
    elif button == "Bot-R":
        if oldzoom == 4:
            zoom = oldzoom = 0
        else:
            zoom = oldzoom = 4

    if i >= page_count:                # wrap around
        i = 0
    while i < 0:
        i += page_count
    data = get_page(i, zoom)
    image_elem.Update(data=data)
    goto.TKStringVar.set(str(i+1))
