"""
Tile an image into 3 x 4 tiles
--------------------------------------------------------------------------------
License: GNU GPL V3
(c) 2022 Jorj X. McKie

Usage
-----
python tile.py input.jpg

Description
-----------
This script demonstrates some of MuPDF's non-PDF graphic capabilities.
"""

import sys
import fitz

print(fitz.__doc__)
assert len(sys.argv) == 2, "Usage: %s <input file>" % sys.argv[0]

pix0 = fitz.Pixmap(sys.argv[1])
tar_cs = pix0.colorspace
tar_width = pix0.width * 3
tar_height = pix0.height * 4
tar_irect = fitz.IRect(0, 0, tar_width, tar_height)
tar_pix = fitz.Pixmap(tar_cs, tar_irect, pix0.alpha)
tar_pix.clear_with(90)

for i in list(range(4)):
    y = i * pix0.height
    for j in list(range(3)):
        x = j * pix0.width
        pix0.set_origin(x, y)
        tar_pix.copy(pix0, pix0.irect)
        fn = "./output/target-" + str(i) + str(j) + ".png"
        tar_pix.save(fn)
