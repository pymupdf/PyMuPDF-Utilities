import fitz

"""
Render a page with and without anootations.

Please note that starting with v1.16.0, pixmaps without annotations
can be created directly.
"""
print(fitz.__doc__)
advanced = list(fitz.VersionBind.split(".")) >= ["1", "16", "0"]


def no_annots_pix(src, page, alpha=False):
    r = page.rect
    doc = fitz.open()
    p1 = doc.newPage(width=r.width, height=r.height)
    p1.showPDFpage(r, src, page.number)
    return p1.getPixmap(alpha=alpha)


src = fitz.open("new-annots.pdf")  # a document with annotations
p1 = src[0]
pix1 = p1.getPixmap(alpha=False)
pix1.writePNG("with-annots.png")  # save page pixmap

pix2 = (
    no_annots_pix(src, p1) if not advanced else p1.getPixmap(alpha=False, annots=False)
)
pix2.writePNG("w-o-annot.png")
