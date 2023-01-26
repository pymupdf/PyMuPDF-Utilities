"""
Optimize a PDF document with FileOptimizer.
-------------------------------------------------------------------------------
License: GNU GPL V3
(c) 2022 Jorj X. McKie

Usage
-----
python optimize.py input.pdf

Notes
-----
Since "/Producer" and "/Creator" get affected by this, the document metadata is
first saved to be restored after the optimization is completed. This means
non-compressed object definitions are also accepted as created by FileOptimizer.

Dependencies
------------
FileOptimizer
"""

from __future__ import print_function
import fitz
import sys, os, subprocess, tempfile, time

assert len(sys.argv) == 2, "need filename parameter"
fn = sys.argv[1]
assert fn.lower().endswith(".pdf"), "must be a PDF file"

fullname = os.path.abspath(fn)  # get the full path & name
t0 = time.perf_counter()  # save current time
doc = fitz.open(fullname)  # open PDF to save metadata
meta = doc.metadata
doc.close()

t1 = time.perf_counter()  # save current time again
subprocess.call(["fileoptimizer64", fullname])  # now invoke super optimizer
t2 = time.perf_counter()  # save current time again

cdir = os.path.split(fullname)[0]  # split dir from filename
fnout = tempfile.mkstemp(suffix = ".pdf", dir = cdir)  # create temp pdf name
doc = fitz.open(fullname)  # open now optimized PDF
doc.set_metadata(meta)  # restore old metadata
doc.save(fnout[1], garbage = 4)  # save temp PDF with it, a little sub opt
doc.close()  # close it

os.remove(fn)  # remove super optimized file
os.close(fnout[0])  # close temp file
os.rename(fnout[1], fn)  # and rename it to original filename
t3 = time.perf_counter()  # save current time again

# put out runtime statistics
print("Timings:")
print(str(round(t1-t0, 4)).rjust(10), "save old metata")
print(str(round(t2-t1, 4)).rjust(10), "execute FileOptimizer")
print(str(round(t3-t2, 4)).rjust(10), "restore old metadata")
