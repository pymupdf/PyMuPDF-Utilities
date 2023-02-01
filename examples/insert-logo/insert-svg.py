"""
Insert the MuPDF logo in SVG format in all pages of a PDF document
--------------------------------------------------------------------------------
License: GNU GPL V3
(c) 2018-2019 Jorj X. McKie

Usage
-----
python insert-svg.py input.pdf logo.svg

Dependencies
------------
PyMuPDF, svglib
"""

import sys
import fitz
from svglib.svglib import svg2rlg

drawing = svg2rlg(sys.argv[2])
pdfbytes = drawing.asString("pdf")

src = fitz.open("pdf", pdfbytes)

rect = src[0].rect
factor = 25 / rect.height
rect *= factor

doc = fitz.open(sys.argv[1])
for page in doc:
    xref = page.show_pdf_page(rect, src, 0, overlay=True)
doc.save("output_svg.pdf", garbage=4)
