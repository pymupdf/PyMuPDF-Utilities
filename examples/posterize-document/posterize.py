"""
Create a PDF copy with split-up pages (posterize)
--------------------------------------------------------------------------------
License: GNU AGPL V3.0+
(c) 2018 Jorj X. McKie

Usage
------
python posterize.py input.pdf

Description
-----------
The output.pdf file contains 4 pages for every input page. The top-left,
top-right, bottom-left, bottom-right parts of the page are now separate pages.
The page dimensions are 1/4 page of the input file.

Dependencies
------------
PyMuPDF
"""

from __future__ import print_function
import fitz, sys

src = fitz.open(sys.argv[1])
doc = fitz.open()

for spage in src:
    xref = 0
    r = spage.rect
    d = fitz.Rect(spage.cropbox_position, spage.cropbox_position)

    r1 = r * 0.5  # top left
    r2 = r1 + (r1.width, 0, r1.width, 0)  # top right
    r3 = r1 + (0, r1.height, 0, r1.height)  # bottom left
    r4 = fitz.Rect(r1.br, r.br)  # bottom right
    rect_list = [r1, r2, r3, r4]

    for rx in rect_list:
        rx += d
        page = doc.new_page(-1, width=rx.width, height=rx.height)
        xref = page.show_pdf_page(
            page.rect,
            src,
            spage.number,
            clip=rx,
            reuse_xref=xref,
        )

doc.save("output.pdf", garbage=4, deflate=True)
