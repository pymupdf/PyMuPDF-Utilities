"""
Export the table of contents (ToC) of a document to a CSV file
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

parser = argparse.ArgumentParser(description="Enter CSV delimiter [;] and documment filename")
parser.add_argument('-d', help='CSV delimiter [;]', default = ';')
parser.add_argument('doc', help='document filename')
args = parser.parse_args()
delim = args.d # requested CSV delimiter character
fname = args.doc # input document filename

doc = fitz.open(fname)
toc = doc.get_toc(simple = False)
ext = fname[-3:].lower()
outf = open("output.csv", "w")
for t in toc:
    t4 = t[3]
    if ext == "pdf":
        if t4["kind"] == 1:
            p4 = str(t4["to"].y)
        else:
            p4 = "0"
    else:
        p4 = "0"
    rec = delim.join([str(t[0]), t[1].strip(), str(t[2]), p4])
    outf.writelines([rec, "\n"])
outf.close()
