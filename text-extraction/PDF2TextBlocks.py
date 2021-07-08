"""
Created on Thu Dec 14 17:00:00 2017

@author: Jorj McKie
Copyright (c) 2017-2021 Jorj X. McKie

The license of this program is governed by GNU AGPL 3.0.
See the "COPYING" file of this repository.

This is an example for using the Python binding PyMuPDF for MuPDF.

The program extracts the text of any supported input document and writes it
to a text file.
The input file name is provided as a parameter to this script (sys.argv[1])
The output file name is input-filename + ".txt".

In an effort to ensure correct reading sequence, text blocks are sorted in
ascending vertical, then horizontal direction. Sorting happens based on the
coordinates of the blocks' top-left rectangle corner.
This should work for text in horizontal, top-left to bottom-right writing mode.
Please make adjustments to your case as appropriate.

Changes
-------
2021-06-29: simplify block sorting and make script importable.
"""

import fitz
import sys


def main(*args):
    if not args:
        filename = sys.argv[1]
    else:
        filename = args[0]
    ofile = filename + ".txt"
    doc = fitz.open(filename)
    fout = open(ofile, "wb")

    for page in doc:
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: (b[1], b[0]))
        for b in blocks:
            fout.write(b[4].encode("utf-8"))

    fout.close()


if __name__ == "__main__":
    main()
