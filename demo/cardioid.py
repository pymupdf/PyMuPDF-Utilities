"""
PyMuPDF demo script to generate tangent constructors of mathematical curves
like Cardioid, Nephroid and similar.
This works by putting the points of a regular polygon on a circle's
perimeter and then draw - in clockwise fashion - a line from each point to
a point following 'curve' places after it.
The number 'curve' determines the type of the constructed curve. For a
cardioid ('curve' = 2) we therefore would be doing this:
Draw lines p0 to p2, p1 to p3, p2 to p4, ..., p[n-1] to p1.

Just change the 'curve' value to create a different curve.
"""
import fitz

doc = fitz.open()
page = doc.new_page(width=500, height=500)
center = (page.rect.tl + page.rect.br) / 2.0  # center of the page
radius = 200  # we will draw a circle with this radius
n = 523  # number of points on circle perimeter
curve = 5  # type of curve, 2 = cardioid, 3 = nephroid, etc.

p0 = center - (radius, 0)  # leftmost point of circle perimeter
theta = -360 / n  # the angle corresponding to number of points

# define the colors we will use
stroke = fitz.pdfcolor["red"]  # color of the lines
fill = fitz.pdfcolor["wheat"]  # fill color of circle
border = fitz.pdfcolor["black"]  # border color of circle

shape = page.new_shape()  # make a drawing canvas for the page

# draw the circle
shape.draw_circle(center, radius)
shape.finish(color=border, fill=fill, width=1)

"""
------------------------------------------------------------------------------
Compute the points on the perimeter. We do this by "abusing" the
'drawSector' method: it does this for us, but we discard its drawings.
------------------------------------------------------------------------------
"""
points = [p0]  # first point
point = p0
for i in range(1, n):
    point = shape.draw_sector(center, point, theta)  # computes next point
    points.append(point)
shape.draw_cont = ""  # we only need the points: discard draw commands

for i in range(n):
    # connect each point with the right successor
    tar = curve * i % n  # target point of this line
    shape.draw_line(points[i], points[tar])

shape.finish(color=stroke, width=0.2)  # finsh the line draws
shape.commit()
doc.save(__file__.replace(".py", ".pdf"), deflate=True)
