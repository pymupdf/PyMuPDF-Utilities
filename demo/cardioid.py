"""
PyMuPDF demo script to generate tangent constructors of curves
like cardioid, nephroid and the like
"""
import fitz
import os

outpdf = os.path.abspath(__file__).replace(".py", ".pdf")
doc = fitz.open()
page = doc.newPage(width=500, height=500)
center = (page.rect.tl + page.rect.br) / 2.0
radius = 200
n = 523  # number of lines to draw
curve = 4  # type of curve, 2 = cardioid, 3 = nephroid, etc.
p0 = center - (radius, 0)
theta = -360 / n
shape = page.newShape()

# draw a blue circle filled with yellow
shape.drawCircle(center, radius)
shape.finish(color=(0, 0, 1), fill=(1, 1, 0), width=3)

# calculate points on the perimeter
points = [p0]
point = p0
for i in range(1, n):
    point = shape.drawSector(center, point, theta)
    points.append(point)
shape.draw_cont = ""  # we only need the points

for i in range(n):  # do the line drawing
    tar = curve * i % n  # target point of this line
    shape.drawLine(points[i], points[tar])

shape.finish(color=(1, 0, 0), width=0.2)  # draw the lines
shape.commit()
doc.save(outpdf, deflate=True)
