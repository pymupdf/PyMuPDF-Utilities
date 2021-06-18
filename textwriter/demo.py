import fitz, os

thisdir = lambda f: os.path.join(os.path.dirname(__file__), f)
thisfile = os.path.abspath(__file__)
outfile = thisfile.replace(".py", ".pdf")

font1 = fitz.Font("helv")
font2 = fitz.Font("tiro")
doc = fitz.open()
page = doc.new_page()
point = fitz.Point(50, 72)
matrix = fitz.Matrix(-20)

wrt1 = fitz.TextWriter(page.rect, color=(0, 0, 1))
wrt2 = fitz.TextWriter(page.rect, color=(1, 0, 0))

_, last = wrt1.append(point, "This text changes color,", font1, 11)
_, last = wrt2.append(last, " font and fontsize", font2, 18)
_, last = wrt1.append(last, " several", font1, 11)
_, last = wrt2.append(last, " times!", font2, 24)

# output both text writers on current page in arbitrary sequence
wrt1.write_text(page, morph=(point, matrix))  # using the same morph parameter
wrt2.write_text(page, morph=(point, matrix))  # also preserves the joint text.

# make a new page
page = doc.new_page()
rect = wrt1.text_rect | wrt2.text_rect  # join rect of blue and red text
# make new rectangle from it, rotated by 90 degrees
nrect = fitz.Rect(
    rect.tl,  # same top-left, but width and height exchanged
    rect.x0 + rect.height,
    rect.y0 + rect.width,
)

# use the page method for joint rotated output
page.write_text(rect=nrect, writers=(wrt1, wrt2), rotate=90)

# one more time with rotation by 270 degrees
nrect += (
    2 * nrect.width,  # identical copy somewhat shifted to the right
    0,
    2 * nrect.width,
    0,
)
page.write_text(rect=nrect, writers=(wrt1, wrt2), rotate=-90)

# more outputs with 45 degrees
page = doc.new_page()
page.write_text(
    rect=page.rect,
    writers=(wrt1, wrt2),
    color=(0.2, 0.6, 1),
    rotate=-45,  # or recoloring
)
page.write_text(
    rect=page.rect,
    writers=(wrt1, wrt2),
    opacity=0.5,  # can be used for watermarking
    rotate=45,
)
doc.save(
    outfile,
    garbage=4,  # makes sense here to combine identical binary data
    deflate=True,
)
