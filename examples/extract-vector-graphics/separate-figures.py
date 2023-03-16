"""
Demo skript: Turn Drawings into PNGs
------------------------------------
Walk through the drawings of a page and join path rectangles, which "touch"
each other.
This potentially results in a smaller set of rectangles, which each cover
a vector graphics figure.
for each of these rectanlges create high resolution PNG image.

License & Copyright
-------------------
License AGPL 3.0
Copyright (c) 2021, Jorj McKie
"""
import sys

import fitz

doc = fitz.open(sys.argv[1])
for page in doc:
    new_rects = []  # resulting rectangles

    for p in page.get_drawings():
        w = p["width"]  # thickness of the border line
        r = p["rect"] + (-w, -w, w, w)  # enlarge each rectangle by width value
        for i in range(len(new_rects)):
            if abs(r & new_rects[i]) > 0:  # touching one of the new rects?
                new_rects[i] |= r  # enlarge it
                break
        # now look if contained in one of the new rects
        remainder = [s for s in new_rects if r in s]
        if remainder == []:  # no ==> add this rect to new rects
            new_rects.append(r)

    new_rects = list(set(new_rects))  # remove any duplicates
    new_rects.sort(key=lambda r: abs(r), reverse=True)
    remove = []
    for j in range(len(new_rects)):
        for i in range(len(new_rects)):
            if new_rects[j] in new_rects[i] and i != j:
                remove.append(j)
    remove = list(set(remove))
    for i in reversed(remove):
        del new_rects[i]
    new_rects.sort(key=lambda r: (r.tl.y, r.tl.x))  # sort by location
    mat = fitz.Matrix(3, 3)  # high resolution matrix
    for i, r in enumerate(new_rects):
        if r.height <= 5 or r.width <= 5:
            continue  # skip lines and empty rects
        pix = page.get_pixmap(matrix=mat, clip=r)
        pix.save("drawing-%03i-%02i.png" % (page.number, i))
