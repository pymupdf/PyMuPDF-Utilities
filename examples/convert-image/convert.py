"""
Convert an arbitrary image to a PNG pixmap using Pillow
--------------------------------------------------------------------------------
License: GNU GPL V3
(c) 2022 Jorj X. McKie

Usage
-----
python convert.py input.jpg

Dependencies
------------
Pillow
"""

import sys
import fitz
from PIL import Image

print(fitz.__doc__)

if len(sys.argv) == 2:
    pic_fn = sys.argv[1]
else:
    pic_fn = None

if pic_fn:
    print("Reading %s" % pic_fn)
    pic_f = open(pic_fn, "rb")
    img = Image.open(pic_f).convert("RGB")
    samples = img.tobytes()
    pix = fitz.Pixmap(fitz.csRGB, img.size[0], img.size[1], samples, 0)
    pix.save("output.png")
    pic_f.close()
