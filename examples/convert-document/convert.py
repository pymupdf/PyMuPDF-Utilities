"""
Convert an arbitrary document (XPS, EPUB, CBZ, etc.) to PDF
--------------------------------------------------------------------------------
License: GNU GPL V3
(c) 2018 Jorj X. McKie

Usage
-----
python convert.py input.epub

Description
-----------
The table of contents and the links of the input file are recovered. While this
works well for bookmarks (outlines, table of contents) links will only work as
expected as long as they are not of type "LINK_NAMED". This link type is skipped
by the script.

For XPS and EPUB though, internal links are of type "LINK_NAMED". MuPDF does not
resolve them to page numbers. So, anyone knowledgeable enough about the internal
structure of these document types can further interpret and resolve these link
types.

Dependencies
------------
PyMuPDF
"""

import sys
import fitz

if not (list(map(int, fitz.VersionBind.split("."))) >= [1, 13, 3]):
    raise SystemExit("insufficient PyMuPDF version")

fn = sys.argv[1]
doc = fitz.open(fn)

if doc.is_pdf:
    raise SystemExit("document is PDF already")

print("Converting '%s' to 'output.pdf'" % (fn))
b = doc.convert_to_pdf()  # convert to pdf
pdf = fitz.open("pdf", b)  # open as pdf

toc = doc.get_toc()  # table of contents of input
pdf.set_toc(toc)  # simply set it for output
meta = doc.metadata  # read and set metadata
if not meta["producer"]:
    meta["producer"] = "PyMuPDF v" + fitz.VersionBind

if not meta["creator"]:
    meta["creator"] = "PyMuPDF PDF converter"

pdf.set_metadata(meta)

# now process the links
link_cnti = 0
link_skip = 0
for pinput in doc:  # iterate through input pages
    links = pinput.get_links()  # get list of links
    link_cnti += len(links)  # count how many
    pout = pdf[pinput.number]  # read corresp. output page
    for l in links:  # iterate though the links
        if l["kind"] == fitz.LINK_NAMED:  # we do not handle named links
            link_skip += 1  # count them
            continue
        pout.insert_link(l)  # simply output the others

pdf.save("output.pdf", garbage=4, deflate=True)
print("Skipped %i named links of a total of %i in input." % (link_skip, link_cnti))
