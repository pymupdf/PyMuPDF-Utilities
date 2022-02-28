import fitz

if tuple(map(int, fitz.VersionBind.split("."))) < (1, 19, 5):
    raise ValueError("Need v1.19.5+")

# This script variant does a pseudo-removal:
# replace image by a fully transparent pixmap
doc = fitz.open("original.pdf")

page = doc[0]
page.clean_contents()  # unify page's /Contents into one
images = page.get_images()  # we only are interested in first image here
item = images[0]
old_xref = item[0]  # old image xref

# make a small 100% transparent pixmap (of just any dimension)
pix = fitz.Pixmap(fitz.csGRAY, (0, 0, 1, 1), 1)
pix.clear_with()  # clear all samples bytes to 0x00

# insert new image just anywhere
new_xref = page.insert_image(page.rect, pixmap=pix)

# copy over definition and stream of new image
doc.xref_copy(new_xref, old_xref)

# there now is a second /Contents object, showing new image
cont_xrefs = page.get_contents()

# make sure that new /Contents is forgotten again
page.set_contents(cont_xrefs[0])
page.clean_contents()
doc.ez_save("no-image.pdf", garbage=4)
