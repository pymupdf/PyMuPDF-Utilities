"""
Decrypt a PDF document with the password provided and save it as a new document
--------------------------------------------------------------------------------
License: GNU GPL V3+
(c) 2022 Jorj X. McKie

Usage
-----
python decrypt.py input.pdf password output.pdf
"""

import sys
import fitz

print(fitz.__doc__)
assert len(sys.argv) == 4, (
    "Usage: %s <input file> <password> <output file>" % sys.argv[0]
)

doc = fitz.Document(sys.argv[1])
assert doc.needs_pass, sys.argv[0] + " not password protected"

assert doc.authenticate(sys.argv[2]), 'cannot decrypt %s with password "%s"' % (
    sys.argv[1],
    sys.argv[2],
)

doc.save(sys.argv[3])
