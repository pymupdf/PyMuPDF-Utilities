"""
Draw an RGB pixel area with numpy and save it with fitz
--------------------------------------------------------------------------------
License: GNU GPL V3
(c) 2022 Jorj X. McKie

Usage
-----
python draw.py

Description
-----------
This is 10+ times faster than saving with pure python solutions like pypng and
almost 2 times faster than saving with PIL. However, PIL images are smaller than
those of MuPDF.

Dependencies
------------
Pillow, numpy
"""

from __future__ import print_function
import sys
import time
import fitz
import numpy as np
import PIL
from PIL import Image

print("Python:", sys.version)
print("NumPy version", np.__version__)
print(fitz.__doc__)
print("PIL version", PIL.__version__)

height = 2048
width = 2028

image = np.ndarray((height, width, 3), dtype=np.uint8)

for i in range(height):
    for j in range(width):
        image[i, j] = np.array([i % 256, j % 256, (i + j) % 256], dtype=np.uint8)

samples = image.tobytes()

ttab = [(time.perf_counter(), "")]

pix = fitz.Pixmap(fitz.csRGB, width, height, samples, 0)
pix.save("output_fitz.png")
ttab.append((time.perf_counter(), "fitz"))

pix = Image.frombuffer("RGB", [width, height], samples, "raw", "RGB", 0, 1)
pix.save("output_PIL.png")
ttab.append((time.perf_counter(), "PIL"))

for i, t in enumerate(ttab):
    if i > 0:
        print("storing with %s: %g sec." % (t[1], t[0] - ttab[i - 1][0]))
