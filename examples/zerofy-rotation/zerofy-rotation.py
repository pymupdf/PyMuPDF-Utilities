"""
This is a PyMuPDF utility script performing the following function:

It copies the input pages to the output file giving all pages a rotation
of zero - without changing page appearance.

Usage: "python zerofy-rotation.py input.pdf"

The resulting output file will be named "input-rot0.pdf".
"""

import sys
import fitz

try:
    src = fitz.open(sys.argv[1])  # source file
except:
    print("Usage: 'python zerofy-rotation.py input.pdf'\n")
    raise
doc = fitz.open()  # new output file

for src_page in src:  # iterate over input pages
    src_rect = src_page.rect  # source page rect
    w, h = src_rect.br  # save its width, height
    src_rot = src_page.rotation  # save source rotation
    src_page.set_rotation(0)  # set rotation to 0 temporarily
    page = doc.new_page(width=w, height=h)  # make output page
    page.show_pdf_page(  # insert source page
        page.rect,
        src,
        src_page.number,
        rotate=-src_rot,  # reversed original rotation
    )

src.close()
doc.ez_save(src.name.replace(".pdf", "-rot0.pdf"), clean=True)
