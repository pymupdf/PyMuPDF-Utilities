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
    print("There exist pages with multiple /Contents.")
    if len(clist) != len(set(clist)):  # subset of unique xrefs is smaller!
        print("Re-used /Contents exist -> using 'clean' option.")
        doc.save("cleaned-" + doc.name,
                 garbage = 4,
                 clean = True,         # use the standard clean function
                 deflate = True,
                 )
    else:                              # each page has its own contents
        print("No re-used /Contents - going to combine.")
        for page in doc:
            xrefl = page._getContents()
            if len(xrefl) < 2:         # page has only one contents
                continue
            c = b""                    # the combined contents area
            for xref in xrefl:
                c += doc._getXrefStream(xref)    # concat all contents and ...
            doc._updateStream(xrefl[0], c)       # ... overwrite first object
            page._setContents(xrefl[0])          # reflect this in page defin.
        doc.save("cleaned-" + doc.name,
                 garbage = 4,          # removes now unused contents objects
                 deflate = True,
                )
else:
    print("Nothing to do: all pages only have one /Contents object.")

t1 = time.time()
print("Elapsed time %g seconds" % (t1-t0))
