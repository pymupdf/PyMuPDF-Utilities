"""
Draw the Sierpinski carpet fractal
-------------------------------------------------------------------------------
License: GNU AFFERO GPL V3
(c) 2019 Jorj X. McKie

Usage
-----
python carpet.py

Purpose
-------
Demonstrate the use of PyMuPDF Pixmaps by drawing the Sierpinski carpet.
The final picture will be a square with each edge having a length of 3**n.

This is one of several alternative versions, which directly fills the
image's areas, which correspond to "holes" in the carpet.
There is another script available (sierpinski-punch.py), which uses a recursive
approach, which may appear more intuitive.

Comments in the loop indicate different ways to fill the "holes":

1. setRect:     fill with some predefined color
2. copyPixmap:  copy the corresponding part from some other pixmap.
                Here you could use the pixmap of some arbitrary image, for
                example some photo.

Whichever method you use, the punch function should show a similar performance.
The time required to save the resulting PNG image very much depends on image
"complexity": it will be longer if you used some photo image in method 2
(copyPixmap) above.
"""

from __future__ import print_function
import fitz, time

print(fitz.__doc__)

if not list(map(int, fitz.VersionBind.split("."))) >= [1, 14, 8]:
    raise SystemExit("need PyMuPDF v1.14.8 for this script")

mytime = time.clock if str is bytes else time.perf_counter

n = 6
d = 3**n  # edge length

t0 = mytime()
ir = (0, 0, d, d)  # the pixmap rectangle

pm = fitz.Pixmap(fitz.csRGB, ir, False)
fillcolor = fitz.utils.getColorInfoDict()["papayawhip"]
pm.set_rect(ir, fillcolor)  # fill it with some background color

color = (0, 0, 255)  # color to fill the punch holes

# define 'fill' pixmap for the punch holes
fill = fitz.Pixmap(pm, 0)  # copy pm
fill.invert_irect(fill.irect)  # inverted colors of pm

for lvl in range(0, n + 1):
    step = 3 ** (n - lvl)
    for x in range(0, 3**lvl):
        x0 = x * step
        if x % 3 == 1:
            for y in range(0, 3**lvl):
                y0 = y * step
                if y % 3 == 1:
                    pm.set_rect((y0, x0, y0 + step, x0 + step), color)
                    # pm.copy(fill, (y0, x0, y0 + step, x0 + step))

t1 = mytime()
pm.save("output_carpet.png")
t2 = mytime()
print("Sierpinski carpet fitz")
print("----------------------")
print("%g sec filling the pixmap" % round(t1 - t0, 3))
print("%g sec saving the picture" % round(t2 - t1, 3))
