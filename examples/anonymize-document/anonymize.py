"""
Remove all text from a document.
-------------------------------------------------------------------------------
License: GNU GPL V3
(c) 2022 Jorj X. McKie

Usage
-----
python anonymize.py input.pdf

Description
-----------
Scan through all pages of a PDF and remove all text. The metadata dictionary
will also be cleared with "none" values. Any XML-based metadata will also be
deleted.
"""

from __future__ import print_function
import fitz, sys


def remove_txt(cont):
    """
    Remove everything enclosed in a pair of "BT" / "ET" strings, including both.
    Assuming "cont" is the string of a PDF "/Contents" stream, this will make
    all text of the owning page disappear (permanent delete).
    "cont" is a bytes object in Python 3, so we will turn it into a string
    first in that case.
    """
    if type(cont) is bytes and str is not bytes:
        cont1 = (cont.decode()).replace("\n", " ")
    else:
        cont1 = cont.replace("\n", " ")
    ct = cont1.split(" ")
    nct = []
    intext = False
    for word in ct:
        if word == "ET":
            intext = False
            continue
        if word == "BT":
            intext = True
            continue
        if intext:
            continue
        nct.append(word)

    ncont = " ".join(nct)
    if str is not bytes:  # caller expects bytes if Python 3
        ncont = bytes(ncont, "utf-8")
    return ncont


assert len(sys.argv) == 2, "need input PDF file name"
fn = sys.argv[1]
assert fn.endswith(".pdf"), "expect a PDF file"
doc = fitz.open(fn)
doc.set_metadata({})  # set metadata values to "none"
doc.del_xml_metadata()  # delete any XML metadata
for page in doc:
    xref_lst = page.get_contents()
    for xref in xref_lst:
        cont = doc.xref_stream(xref)
        ncont = remove_txt(cont)
        doc.update_stream(xref, ncont)

doc.save("output.pdf", clean=True, garbage=4)
