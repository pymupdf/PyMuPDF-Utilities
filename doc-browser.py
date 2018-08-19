import sys
import fitz
import PySimpleGUI as sg
fname = sys.argv[1]
doc = fitz.open(fname)
title = "PyMuPDF display of '%s' (%i pages)" % (fname, len(doc))

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

data = get_page(0)                     # show page 1 for start
image_elem = sg.Image(data=data)
layout = [  [image_elem],
            [sg.ReadFormButton('Next'),
             sg.ReadFormButton('Prev'),
             sg.ReadFormButton('First'),
             sg.ReadFormButton('Last'),
             sg.ReadFormButton('Zoom-1'),
             sg.ReadFormButton('Zoom-2'),
             sg.ReadFormButton('Zoom-3'),
             sg.ReadFormButton('Zoom-4'),
             sg.Quit()]  ]

form.Layout(layout)

i = 0
oldzoom = 0                            # used for zoom on/off
# the zoom buttons work in on/off mode.
while True:
    button,value = form.Read()
    zoom = 0
    if button in (None, 'Quit'):
        break
    if button == "Next":
        i += 1
    elif button == "Prev":
        i -= 1
    elif button == "First":
        i = 0
    elif button == "Last":
        i = -1
    elif button == "Zoom-1":
        if oldzoom == 1:
            zoom = oldzoom = 0
        else:
            zoom = oldzoom = 1
    elif button == "Zoom-2":
        if oldzoom == 2:
            zoom = oldzoom = 0
        else:
            zoom = oldzoom = 2
    elif button == "Zoom-3":
        if oldzoom == 3:
            zoom = oldzoom = 0
        else:
            zoom = oldzoom = 3
    elif button == "Zoom-4":
        if oldzoom == 4:
            zoom = oldzoom = 0
        else:
            zoom = oldzoom = 4
    data = get_page(i, zoom)
    image_elem.Update(data=data)

