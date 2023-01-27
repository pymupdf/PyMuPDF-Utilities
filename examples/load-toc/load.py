"""
Load a table of contents (ToC) from a CSV file
-------------------------------------------------------------------------------
License: GNU GPL V3
(c) 2023 Jorj X. McKie

Usage
-----
python load.py -d ";" -csv input.csv -pdf input.pdf

Description
-----------
The output.csv file generated in examples/export-toc is renamed as input.csv
to be used as an input file in this example. The input.pdf file behaves as both
an input and an output file.

Please note that all existing outline entries (bookmarks) in the PDF will be
replaced if running this script. The document is updated.

Each CSV line must contain 3 or 4 entries:

lvl     A positive integer indicating the hierarchy level of the entry. The
        first line must contain an lvl value of 1. It can be increased by 1 and
        decrease by any number.

title   A non-empty string containing the entry's title.

page    An integer representing the page number which value must be in the
        document's page range.

height  An optional, positive float value representing the entry position on the
        page and counting from the bottom. If omitted, 36 points (half an inch)
        below the top of the page are taken.

Dependencies
------------
PyMuPDF
"""

import csv
import fitz
import argparse

parser = argparse.ArgumentParser(description="Enter CSV delimiter [;], CSV filename and PDF filename")
parser.add_argument('-d', help='CSV delimiter [;]', default = ';')
parser.add_argument('-csv', help='CSV filename')
parser.add_argument('-pdf', help='PDF filename')

args = parser.parse_args()

assert args.csv, "missing CSV filename"
assert args.pdf, "missing PDF filename"

doc = fitz.open(args.pdf)
toc = []
with open(args.csv) as tocfile:
    tocreader = csv.reader(tocfile, delimiter = args.d)
    for row in tocreader:
        assert len(row) <= 4, "cannot handle more than 4 entries:\n %s" % (str(row),)
        try:
            p4 = float(row[3])
            toc.append([int(row[0]), row[1], int(row[2]), p4])
        except:
            toc.append([int(row[0]), row[1], int(row[2])])
doc.set_toc(toc)
doc.saveIncr()
