"""
Utility to convert a supported document to an image-only PDF.

License: GNU AGPL 3.0
Author: (c) Harald Lieder, harald.lieder@outlook.com
Date: 2021-08-30
"""
import os
import sys

import fitz


def main(doc, outfile=None, pages=None, dpi=96):
    if outfile is None:
        if doc.name:
            filename, _ = os.path.splitext(doc.name)
            outfile = filename + ".pdf"
        elif __file__.endswith(".py"):
            outfile = __file__.replace(".py", ".pdf")
        else:
            outfile = "out.pdf"
    if outfile == doc.name:
        outfile += ".pdf"
    if pages is None:
        pages = range(doc.page_count)
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    pdfout = fitz.open()
    for pno in pages:
        page = doc[pno]
        pix = page.get_pixmap(matrix=mat)
        pix.set_dpi(dpi, dpi)
        opage = pdfout.new_page(width=page.rect.width, height=page.rect.height)
        opage.insert_image(opage.rect, pixmap=pix)
    pdfout.ez_save(outfile)
    pdfout.close()


if __name__ == "__main__":
    filename = sys.argv[1]
    doc = fitz.open(filename)
    main(doc)
