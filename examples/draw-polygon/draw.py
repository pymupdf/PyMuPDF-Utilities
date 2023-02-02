"""
Draw a regular polygon with a curly border
--------------------------------------------------------------------------------
License: GNU GPL V3
(c) 2017 Jorj X. McKie

Usage
-----
python draw.py

Description
-----------
Draw an arbitrary regular polygon using wavy lines instead of straight lines.
Two output files are generated: a PDF and a SVG image file. The page size is
adjusted to the drawing. This script also demonstrates how the draw commands can
be used to calculate points without actually drawing them.

Dependencies
------------
PyMuPDF
"""

import fitz

print(fitz.__doc__)

outpdf = "output.pdf"
outsvg = "output.svg"
doc = fitz.open()
page = doc.new_page()
img = page.new_shape()
nedge = 5  # number of polygon edges
breadth = 2  # wave amplitude
beta = -1.0 * 360 / nedge  # our angle, drawn clockwise
center = fitz.Point(300, 300)  # center of circle
p0 = fitz.Point(300, 200)  # start here (1st edge = north)
p1 = +p0  # save as last edge to add
points = [p0]  # to store the polygon edges

# we only use this to calculate the polygon edges
# we will delete the resp. draw commands
for i in range(nedge - 1):
    p0 = img.draw_sector(center, p0, beta)
    points.append(p0)

# erase previous draw commands in contents buffer
img.draw_cont = ""

points.append(p1)  # add starting point to edges list
# now draw the lines along stored edges
for i in range(nedge):
    img.draw_squiggle(points[i], points[i + 1], breadth=breadth)

img.finish(color=(0, 0, 1), fill=(1, 1, 0), closePath=False)

# adjust visible page to dimensions of the drawing
page.set_cropbox(img.rect)
img.commit()
doc.save(outpdf)
fout = open(outsvg, "w")
fout.write(page.get_svg_image())
fout.close()
doc.close()
