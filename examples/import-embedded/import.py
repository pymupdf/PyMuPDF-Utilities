"""
Import a file to a document
--------------------------------------------------------------------------------
License: GNU AGPL V3
(c) 2023 Jorj X. McKie

Usage
-----
python import.py input.pdf joe-caione-qO-PIF84Vxg-unsplash.jpg -o output.pdf
"""

from __future__ import print_function
import fitz
import argparse

parser = argparse.ArgumentParser(
    description="Enter PDF, file to embed, and optional name, description and output pdf."
)
parser.add_argument("pdf", help="PDF filename")
parser.add_argument("file", help="name of embedded file")
parser.add_argument("-n", "--name", help="name for embedded file entry (default: file)")
parser.add_argument("-d", "--desc", help="description (default:  file)")
parser.add_argument("-o", "--output", help="output PDF (default: modify pdf)")

args = parser.parse_args()

if not args.name:
    name = args.file
desc = args.desc
if not args.desc:
    desc = args.file

content = open(args.file, "rb").read()
doc = fitz.open(args.pdf)
doc.embfile_add(name, content, args.file, desc)

if not args.output:
    doc.saveIncr()
else:
    doc.save(args.output, garbage=4, deflate=True)
