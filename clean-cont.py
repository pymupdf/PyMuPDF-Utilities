import sys, time
import fitz
t0 = time.process_time()
doc = fitz.open(sys.argv[1])
if not doc.isPDF:
    raise SystemExit("Only works for PDF.")
clist = []
print("\nProcessing file '%s' with %i pages.\n" % (doc.name, len(doc)))
for page in doc:
    for xref in page._getContents():
        clist.append(xref)

if len(clist) > len(doc):
    print("There exist pages with multiple /Contents.")
    if len(clist) == len(set(clist)):
        print("No re-used /Contents - going to combine.")
    else:
        raise SystemExit("Abborting: 'mutool clean -cs' required.")
    for page in doc:
        xrefl = page._getContents()
        if len(xrefl) < 2:
            continue
        c = b""
        for xref in xrefl:
            c += doc._getXrefStream(xref)
        doc._updateStream(xrefl[0], c)
        page._setContents(xrefl[0])
    doc.save("cleaned-" + doc.name, garbage = 4, deflate=True)
else:
    print("All pages only have one /Contens.")

t1 = time.process_time()
print("Elapsed time %g seconds" % (t1-t0))