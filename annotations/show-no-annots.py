import os
import fitz

"""
Render a page with and without anootations.

Please note that starting with v1.16.0, pixmaps without annotations
can be created directly.
"""
print(fitz.__doc__)
thisdir = os.path.dirname(__file__)
infile = os.path.join(thisdir, "new-annots-0.pdf")
src = fitz.open(infile)  # a document with annotations
p1 = src[0]
pix1 = p1.getPixmap(annots=True)
pix1.writePNG(os.path.join(thisdir, "with-annots.png"))  # save page pixmap
pix2 = p1.getPixmap(annots=False)
pix2.writePNG(os.path.join(thisdir, "without-annots.png"))
