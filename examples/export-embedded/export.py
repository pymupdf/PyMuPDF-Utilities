"""
Export an embedded file from the input document to the output document
--------------------------------------------------------------------------------
License: GNU AGPL V3
(c) 2021 Jorj X. McKie

Usage
-----
python export.py input.pdf joe-caione-qO-PIF84Vxg-unsplash.jpg output.pdf

Description
-----------
The output.pdf file generated in examples/embed-images is renamed as input.pdf
to be used as the input file in this example.
"""

from __future__ import print_function
import sys
import fitz

pdffn = sys.argv[1]  # PDF file name
name = sys.argv[2]  # embedded file identifier
expfn = sys.argv[3]  # filename of exported file

doc = fitz.open(pdffn)  # open PDF
outfile = open(expfn, "wb")  # to be on the safe side always open binary

# extract file content. Will get exception on any error.
content = doc.embfile_get(name)

outfile.write(content)
outfile.close()
