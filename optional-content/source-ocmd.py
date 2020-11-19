"""
PyMuPDF Demo Program

Show how to create a PDF page that display content depending on the state
of a set of optional content groups.

Here we create a PDF page with two objects of which exactly one is shown
at any time.
"""
import fitz

# source file with at least 2 pages
src = fitz.open("source.pdf")

# new PDF with one page
doc = fitz.open()
page = doc.newPage()

# define 2 rectangles: upper and lower half page
r0 = page.rect
r0.y1 = r0.height / 2
r1 = r0 + (0, r0.height, 0, r0.height)

# make 1 OCG and 1 OCMD
ocg0 = doc.addOCG("ocg0", on=True)  # to be used for upper rect

# the following is interpreted as "not ocg0"
ocmd0 = doc.set_ocmd(  # to be used for lower rect
    ocgs=[ocg0],
    policy="alloff",
)

# alternatively, you can use visibility expressions:
# ocmd0 = doc.set_ocmd(ve=["not", ocg0])

# insert the 2 source page images, each connected to one OCG
page.showPDFpage(r0, src, 0, oc=ocg0, rotate=90)
page.showPDFpage(r1, src, 1, oc=ocmd0, rotate=-90)

doc.save(  # save the file
    __file__.replace(".py", ".pdf"),
    garbage=3,
    pretty=True,
    deflate=True,
    clean=True,
)

"""
The new PDF can now be viewed by e.g. Adobe Acrobat reader. Setting
"ocg0" ON of OFF will flip between showing page 0 and page 1.
"""
