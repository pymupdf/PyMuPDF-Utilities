"""
Draw the Sierpinski carpet fractal
-------------------------------------------------------------------------------
License: GNU AFFERO GPL V3
(c) 2019 Jorj X. McKie

Usage
-----
python punch.py

Purpose
-------
Demonstrate the use of PyMuPDF Pixmaps by drawing the Sierpinski carpet.
The final picture will be a square with each edge having a length of 3**n.

This is one of several alternative versions, which uses a recursive function,
'punch', to fill the central sub-square.

Comments in the punch function indicate, which methods can be used to recolor
the central sub-square:

1. setRect:     fill the square with some predefined color
2. copyPixmap:  copy the corresponding sub-rectangle from some other pixmap.
                Here you could use the pixmap of some arbitrary image, for
                example some photo.
3. invertIrect: re-color the square with the original's inverted colors.

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
d = 3 ** n  # edge length

t0 = mytime()
ir = (0, 0, d, d)  # the pixmap rectangle

pm = fitz.Pixmap(fitz.csRGB, ir, False)
pm.set_rect(pm.irect, (255, 255, 0))  # fill it with some background color

color = (0, 0, 255)  # color to fill the punch holes

# define 'fill' pixmap for the punch holes
fill = fitz.Pixmap(pm, pm.alpha)  # copy pm
fill.invert_irect()  # inverted colors of pm


def punch(x, y, step):
    """Recursively "punch a hole" in the central square of a d x d pixmap."""
    s = step // 3  # the new step
    # iterate through the 9 sub-squares
    # the central one will be filled with the color
    for i in range(3):
        for j in range(3):
            if i != j or i != 1:
                if s >= 3:  # else prevent going down another level
                    punch(x + i * s, y + j * s, s)
            else:
                pm.set_rect((x + s, y + s, x + 2 * s, y + 2 * s), color)
                # pm.copy(fill, (x+s, y+s, x+2*s, y+2*s))
                # pm.invert_irect((x+s, y+s, x+2*s, y+2*s))

    return


# ==============================================================================
# main program
# ==============================================================================
# now start punching holes into the pixmap
punch(0, 0, d)
t1 = mytime()
pm.save("output_punch.png")
t2 = mytime()
print("Sierpinski carpet 'punch'")
print("-------------------------")
print("%g sec to create / fill the pixmap" % round(t1 - t0, 3))
print("%g sec to save the image" % round(t2 - t1, 3))
