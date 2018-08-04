import fitz
def no_annots_pix(src, page, alpha = False):
    r = page.rect
    doc = fitz.open()
    p1 = doc.newPage(width = r.width, height=r.height)
    p1.showPDFpage(r, src, page.number)
    return p1.getPixmap(alpha = alpha)

src = fitz.open("new-annots.pdf")      # a document with annotations
p1 = src[0]
pix1 = p1.getPixmap(alpha = False)
pix1.writePNG("with-annots.png")       # save page pixmap

pix2 = no_annots_pix(src, p1)
pix2.writePNG("w-o-annot.png")