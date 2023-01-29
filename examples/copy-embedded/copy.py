"""
Copy the embedded files in the input document to the output document
--------------------------------------------------------------------------------
License: GNU AGPL V3
(c) 2021 Jorj X. McKie

Usage
-----
python copy.py input.pdf output.pdf

Description
-----------
The output.pdf file generated in examples/embed-images is renamed as input.pdf
to be used as the input file in this example.
"""

from __future__ import print_function
import sys
import fitz

ifn = sys.argv[1]  # input PDF
ofn = sys.argv[2]  # output PDF
docin = fitz.open(ifn)
docout = fitz.open(ofn)
print("Copying embedded files from '%s' to '%s'" % (ifn, ofn))
for i in range(docin.embfile_count()):
    d = docin.embfile_info(i)  # file metadata
    b = docin.embfile_get(i)  # file content
    try:  # safeguarding against duplicate entries
        print("copying entry:", d["name"])
        docout.embfile_add(b, d["name"], d["file"], d["desc"])
    except:
        pass

# save output (incrementally or to new PDF)
docout.saveIncr()
