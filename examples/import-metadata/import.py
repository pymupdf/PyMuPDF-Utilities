"""
Import a metadata dictionary from a CSV file into a PDF document
-------------------------------------------------------------------------------
License: GNU GPL V3
(c) 2023 Jorj X. McKie

Usage
-----
python import.py -d ";" -x "n" -csv input.csv -pdf input.pdf

Description
-----------
The output.csv file generated in examples/export-metadata is renamed as input.csv
to be used as an input file in this example. The input.pdf file behaves as both
an input and an output file.

Dependencies
------------
PyMuPDF
"""

import csv
import fitz
import argparse

parser = argparse.ArgumentParser(description="Enter CSV delimiter [;], CSV filename and documment filename")
parser.add_argument('-d', help='CSV delimiter [;]', default = ';')
parser.add_argument('-x', help='delete XML info [n]', default = 'n')
parser.add_argument('-csv', help='CSV filename')
parser.add_argument('-pdf', help='PDF filename')

args = parser.parse_args()

assert args.csv, "missing CSV filename"
assert args.pdf, "missing PDF filename"

print("delimiter", args.d)
print("xml delete", args.x)
print("csv file", args.csv)
print("pdf file", args.pdf)
print("----------------------------------------")

doc = fitz.open(args.pdf)
oldmeta = doc.metadata
print("old metadata:")
for k,v in oldmeta.items():
    print(k, ":", v)

with open(args.csv) as tocfile:
    tocreader = csv.reader(tocfile, delimiter = args.d)
    for row in tocreader:
        oldmeta[row[0]] = row[1]

print("----------------------------------------")
print("\nnew metadata:")
for k,v in oldmeta.items():
    print(k, ":", v)

doc.set_metadata(oldmeta)
doc.saveIncr()
