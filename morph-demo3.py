import os
import fitz
scriptdir = os.path.abspath(os.curdir)
gold = (1,1,0)
blue = (0,0,1)
pagerect = fitz.Rect(0,0,400,400)
mp = fitz.Point(pagerect.width/2., pagerect.height/2.)
r = fitz.Rect(mp, mp + (80,80))
textpoint = fitz.Point(40, 200)
text = "Just some demo text, to be filled in a rect."
itext = "y-Shearing:\nfitz.Matrix(0, %g, 1)"

doc = fitz.open()
for beta in range(-10, 11):
    page = doc.newPage(width=pagerect.width, height=pagerect.height)
    mat = fitz.Matrix(0, beta*0.1, 1)
    img = page.newShape()
    img.drawRect(r)
    img.finish(fill=gold, color=blue, width=0.3, morph = (r.tl, mat))
    img.insertText(textpoint, itext % (beta*0.1), fontname="cobo")
    img.insertTextbox(r, text, fontsize=15, rotate=90, morph = (r.tl, mat))
    img.commit()

doc = doc.save(os.path.join(scriptdir, __file__ + ".pdf"))
