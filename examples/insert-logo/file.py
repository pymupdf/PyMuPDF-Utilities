"""
Insert the MuPDF logo in PNG format in all pages of a PDF document
--------------------------------------------------------------------------------
License: GNU GPL V3
(c) 2018-2019 Jorj X. McKie

Usage
-----
python file.py input.pdf logo.png

Description
-----------
Any PyMuPDF-supported document can be used as the logo/watermark including PDF,
XPS, EPUB, CBZ, FB2 as well as any image type. SVG-based logos are not always
shown correctly. Use a different PDF converter like svglib if that occurs.

Logos/watermarks are transparent for all document types except for images. If a
transparency is required then the file must be manually converted to PDF first
as described next:

    pix = fitz.Pixmap(logo_filename)
    src = fitz.open()
    src_page = src.new_page(-1, width = pix.width, height = pix.height)
    src_page.insert_image(src_page.rect, pixmap = pix)

Dependencies
------------
PyMuPDF
"""

from __future__ import print_function
import sys
import fitz

src = fitz.open(sys.argv[2])

if not src.is_pdf:
    pdfbytes = src.convert_to_pdf()
    src.close()
    src = fitz.open("pdf", pdfbytes)

rect = src[0].rect
factor = 25 / rect.height
rect *= factor

doc = fitz.open(sys.argv[1])
xref = 0
for page in doc:
    xref = page.show_pdf_page(rect, src, 0, reuse_xref=xref, overlay=False)
doc.save("output_file.pdf", garbage=4)
