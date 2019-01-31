"""
Created on Wed Jan 30 07:00:00 2019

@author: Jorj
@copyright: (c) 2019 Jorj X. McKie
@license: GNU GPL 3.0

Purpose
--------
Demonstrate the use of PyMuPDF Pixmaps by creating Sierpinski's carpet.
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
import fitz, time
if not list(map(int, fitz.VersionBind.split("."))) >= [1, 14, 8]:
    raise SystemExit("need PyMuPDF v1.14.8 for this script")
n = 6
d = 3**n                          # edge length

t0 = time.perf_counter()
ir = (0, 0, d, d)                 # the pixmap rectangle

pm = fitz.Pixmap(fitz.csRGB, ir, False)
pm.setRect(pm.irect, (255,255,0)) # fill it with some background color

color = (0, 0, 255)               # color to fill the punch holes

# define 'fill' pixmap for the punch holes
fill = fitz.Pixmap(pm, pm.alpha)  # copy pm
fill.invertIRect()                # inverted colors of pm

def punch(x, y, step):
    """Recursively "punch a hole" in the central square of a d x d pixmap.
    """
    s = step // 3                 # the new step
    # iterate through the 9 sub-squares
    # the central one will be filled with the color
    for i in range(3):
        for j in range(3):
            if i != j or i != 1:
                if s >= 3:        # else prevent going down another level
                    punch(x+i*s, y+j*s, s)
            else:
                pm.setRect((x+s, y+s, x+2*s, y+2*s), color)
                #pm.copyPixmap(fill, (x+s, y+s, x+2*s, y+2*s))
                #pm.invertIRect((x+s, y+s, x+2*s, y+2*s))

    return

#==============================================================================
# main program
#==============================================================================
# now start punching holes into the pixmap
punch(0, 0, d)
t1 = time.perf_counter()
pm.writeImage("sierpinski-punch.png")
t2 = time.perf_counter()
print ("%g sec to create / fill the pixmap" % round(t1-t0,3))
print ("%g sec to save the image" % round(t2-t1,3))
