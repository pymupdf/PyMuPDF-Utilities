"""
Utility script
--------------
If a PDF has pages with more than one /Contents object, combine them into one.
This either done with the 'clean' option of 'save' (which invokes an MuPDF 
function), or just concatenate the streams.
The latter option is used, if no contents streams are in use by more than one
page. The MuPDF function does additional syntax checking of the content stream
and also of all content streams of all annotations.
"""
from __future__ import print_function
import sys, time
import fitz
t0 = time.time()
doc = fitz.open(sys.argv[1])
if not doc.isPDF:
    raise SystemExit("Only works for PDF.")
clist = []                             # all contents xref numbers
print("\nChecking file '%s' (%i pages) for multiple /Contents.\n" % (doc.name, len(doc)))
for page in doc:
    clist.extend(page._getContents())

if len(clist) > len(doc):              # some pages have more than one!
    print("There exist pages with multiple /Contents (%i : %i)." % (len(clist), len(doc)))
    if len(clist) != len(set(clist)):  # there are duplicate xrefs!
        print("Re-used /Contents exist -> using MuPDF 'clean'.")
        doc.save("cleaned-" + doc.name,
                 garbage = 2,
                 clean = True,         # use the standard clean function
                 deflate = True,       # recompress contents objects
                 )
    else:                              # each page has its own contents
        print("All /Contents are used only once - combining multiples.")
        pcount = 0
        for page in doc:
            xrefl = page._getContents()
            if len(xrefl) < 2:         # page has only one contents
                continue
            pcount += 1
            print("cleaning page %i with %i objects" % (page.number, len(xrefl)))
            c = b""                    # the combined contents area
            for xref in xrefl:
                c += doc._getXrefStream(xref)    # concat all contents and ...
            doc._updateStream(xrefl[0], c)       # ... put result in first one
            page._setContents(xrefl[0])          # reflect this in page defin.
        print("Content of %i pages cleaned." % pcount)
        doc.save("cleaned-" + doc.name,
                 garbage = 2,          # remove unused & compact XREF
                 deflate = True,
                )
else:
    print("Nothing to do: all pages have only one /Contents object.")

t1 = time.time()
print("Elapsed time %g seconds" % (t1-t0))
