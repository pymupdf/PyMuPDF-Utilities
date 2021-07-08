#!/usr/bin/env python
"""
Created on Sun Jul 12 07:00:00 2015

@author: Jorj McKie
Copyright (c) 2015-2021 Jorj X. McKie

The license of this program is governed by GNU AGPL 3.0.
See the "COPYING" file of this repository.

This is an example for using the Python binding PyMuPDF of MuPDF.

This program extracts the text of any supported input document and writes it
to a text file named input-filename + ".txt".

Changes
-------
2021-06-21: add formfeed after each page of text.
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
        fout.write(page.get_text().encode("utf-8") + bytes((12,)))

    fout.close()


if __name__ == "__main__":
    main()