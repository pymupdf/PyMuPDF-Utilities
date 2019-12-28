from __future__ import print_function
import fitz, sys
"""
PyMuPDF utility
----------------
Scan through all pages of a PDF and remove all text. The metadata dictionary
will also be cleared with "none" values. Any XML-based metadata will also be
deleted. The resulting PDF will be save under the name "anonymous.pdf" in the
same directory.
"""
def remove_txt(cont):
    """Remove everything enclosed in a pair of "BT" / "ET" strings, including both. Assuming "cont" is the string of a PDF "/Contents" stream, this will make all text of the owning page disappear (permanent delete). "cont" is a bytes object in Python 3, so we will turn it into a string first in that case.
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
    if str is not bytes:          # caller expects bytes if Python 3
        ncont = bytes(ncont, "utf-8")
    return ncont

assert len(sys.argv) == 2, "need input PDF file name"
fn = sys.argv[1]
assert fn.endswith(".pdf"), "expect a PDF file"
doc = fitz.open(fn)
doc.setMetadata({})               # set metadata values to "none"
doc._delXmlMetadata()             # delete any XML metadata
for page in doc:
    xref_lst = page._getContents()
    for xref in xref_lst:
        cont = doc._getXrefStream(xref)
        ncont = remove_txt(cont)
        doc._updateStream(xref, ncont)

doc.save("anonymous.pdf", clean = True, garbage = 4)
