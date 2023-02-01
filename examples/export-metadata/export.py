"""
Export a document metadata dictionary to a CSV file
-------------------------------------------------------------------------------
License: GNU GPL V3
(c) 2018 Jorj X. McKie

Usage
-----
python export.py -d ";" input.pdf
"""

from __future__ import print_function
import fitz
import argparse

parser = argparse.ArgumentParser(
    description="Enter CSV delimiter [;] and documment filename"
)
parser.add_argument("-d", help="CSV delimiter [;]", default=";")
parser.add_argument("doc", help="document filename")
args = parser.parse_args()
delim = args.d  # requested CSV delimiter character
fname = args.doc  # input document filename

doc = fitz.open(fname)
meta = doc.metadata
outf = open("output.csv", "w")
for k in meta.keys():
    v = meta.get(k)
    if not v:
        v = ""
    rec = delim.join([k, v])
    outf.writelines([rec, "\n"])
outf.close()
