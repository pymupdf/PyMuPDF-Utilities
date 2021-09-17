"""
Utility to convert a supported document to a Comic Book archive.

License: GNU AGPL 3.0
Author: (c) Harald Lieder, harald.lieder@outlook.com
Date: 2021-08-30
"""

import os
import sys
import zipfile

import fitz


def main(doc, outfile=None, pages=None, dpi=96):
    if outfile is None:
        if doc.name:
            filename, _ = os.path.splitext(doc.name)
            outfile = filename + ".cbz"
        elif __file__.endswith(".py"):
            outfile = __file__.replace(".py", ".cbz")
        else:
            outfile = "out.cbz"
    zipout = zipfile.ZipFile(
        outfile,
        "w",
        compression=zipfile.ZIP_STORED,
    )
    if pages is None:
        pages = range(doc.page_count)
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    for pno in pages:
        page = doc[pno]
        pix = page.get_pixmap(matrix=mat)
        pix.set_dpi(dpi, dpi)
        pagename = "p%05i.png" % (pno + 1)
        zipout.writestr(pagename, pix.tobytes("png"))
    zipout.close()


if __name__ == "__main__":
    filename = sys.argv[1]
    doc = fitz.open(filename)
    main(doc)
