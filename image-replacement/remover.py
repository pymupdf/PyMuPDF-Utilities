import fitz
from replacer import img_replace

if tuple(map(int, fitz.VersionBind.split("."))) < (1, 19, 5):
    raise ValueError("Need v1.19.5+")

# This script variant does a pseudo-removal:
# replace image by a small fully transparent pixmap
doc = fitz.open("original.pdf")

page = doc[0]

images = page.get_images()  # we only are interested in first image here
item = images[0]
old_xref = item[0]  # old image xref

# make a small 100% transparent pixmap (of just any dimension)
pix = fitz.Pixmap(fitz.csGRAY, (0, 0, 1, 1), 1)
pix.clear_with()  # clear all samples bytes to 0x00
img_replace(page, old_xref, pixmap=pix)

doc.ez_save("no-image.pdf", garbage=4)
