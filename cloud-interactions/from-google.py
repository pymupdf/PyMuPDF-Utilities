import os
import fitz  # pymupdf
import gcsfs  # google cloud storage file system

# Access the google filesystem.
# You will need to supply credentials - which is omitted here
fs = gcsfs.GCSFileSystem(project="my-google-project")

filename = fs.ls("my-bucket")[0]  # first filename in bucket
ext = os.path.splitext(filename)[1]  # determine file extension
f = fs.open(filename, "rb")  # open with that filesystem

# now open with PyMuPDF using the bytes object of "f"
doc = fitz.open(ext[1:], f.read())
