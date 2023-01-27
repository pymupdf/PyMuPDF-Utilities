"""
Scan a document and store the embedded XObjects as pages in a new document
-------------------------------------------------------------------------------
License: GNU AGPL V3
(c) 2023 Jorj X. McKie

Usage
-----
python extract.py input.pdf

Description
-----------
The new pages can subsequently be used to generate conventional raster images of
the original XObjects or as sources to be embedded in other documents.

Dependencies
------------
PyMuPDF
"""

import sys
import time
import fitz

if fitz.VersionBind.split(".") < ["1", "16", "13"]:
    sys.exit("Need at least PyMuPDF v1.16.13")

start_time = time.perf_counter()
infile = sys.argv[1]  # input filename
src = fitz.open(infile)  # open input
print("Processing '%s' with %i pages." % (infile, len(src)))
outfile = "output.pdf"
doc = fitz.open()  # output file
xobj_total = 0  # counts total number of extracted xobjects
xrefs_encountered = []  # stores already extracted XObjects
for pno in range(len(src)):
    xobj_count = 0  # counts extracted objects per page
    xobj_list = src.get_page_xobjects(pno)  # get list of XObjects
    for xobj in xobj_list:  # loop through them
        if xobj[2] != 0:  # if not occurring directly on the page
            continue  # skip
        bbox = fitz.Rect(xobj[-1])  # bbox of XObject on input page
        if bbox.is_infinite:  # no associated valid bbox?
            continue  # skip
        if xobj[0] in xrefs_encountered:  # already extracted?
            continue  # skip
        xrefs_encountered.append(xobj[0])
        # ----------------------------------------------------------------------
        # We want this XObject, so:
        # (1) copy its page to the output PDF (enforcing zero rotation)
        # (2) from that page remove everything except the XObject invocation
        # (3) modify page size to match the XObject bbox
        # ----------------------------------------------------------------------
        doc.insert_pdf(src, from_page=pno, to_page=pno, rotate=0)
        ref_name = xobj[1]  # the symbolic name
        ref_cmd = ("/%s Do" % ref_name).encode()  # build invocation command
        page = doc[-1]  # page just inserted
        page.set_mediabox(bbox)  # set its page size to XObject bbox
        page.clean_contents()  # consolidate contents of copied page
        xref = page.get_contents()[0]  # and read resulting singular xref
        doc.update_stream(xref, ref_cmd)  # replace it by our one-line command
        xobj_count += 1  # increase counter
    if xobj_count > 0:
        print(  # tell number of extracted XObjects of input page
            "%i XObject%s extracted from page %i."
            % (xobj_count, "s" if xobj_count > 1 else "", pno)
        )
    xobj_total += xobj_count  # increase total xobject count

if xobj_total > 0:
    doc.save(outfile, garbage=4, deflate=True)
    print(
        "%i XObjects extracted from '%s' and saved as '%s'."
        % (xobj_total, src.name, outfile)
    )
else:
    print("No XObjects detected in '%s', no output generated." % infile)
stop_time = round(time.perf_counter() - start_time, 3)
print("Total time %g seconds." % (stop_time,))
