"""
Demo skript: Turn Drawings into PNGs
------------------------------------
Walk through the drawings of a page and join path rectangles, which "touch"
each other.
This potentially results in a smaller set of rectangles, which each cover
a vector graphics figure.
for each of these rectangles create a high resolution PNG image.

License & Copyright
-------------------
License AGPL 3.0
Copyright (c) 2021, Jorj McKie
"""
import sys

import fitz


def detect_rects(page):
    """Detect and join rectangles of connected vector graphics."""
    # make a list of vector graphics rectangles (IRects are sufficient)
    prects = sorted(
        [p["rect"].irect for p in page.get_drawings()], key=lambda r: (r.y1, r.x0)
    )
    new_rects = []  # the final list of the joined records

    # -------------------------------------------------------------------------
    # The strategy is to identify and join all rects having at least one
    # point in common. We'll extend each rectangle somewhat by converting
    # it into an IRect and adding a 1 point border around it.
    # This allows using the ".intersects()" method for better performance.
    # -------------------------------------------------------------------------
    while prects:  # the original list will shrink in the process
        r = prects[0]  # start with first (top-left) rectangle
        rx = r + (-1, -1, 1, 1)  # little larger so we can use intersections
        for i in range(len(prects)):
            if i == 0:  # ignore first rectangle
                continue
            nr = prects[i]
            if rx.intersects(nr):  # intersecting first rectangle:
                prects[i] |= r
                prects[0] |= +prects[i]
                r = +prects[0]
                rx = r + (-1, -1, 1, 1)
        new_rects.append(prects.pop(0))  # shorten the list
        # remove duplicates: will dramatically improve performance!
        prects = sorted(list(set(prects)), key=lambda r: (r.y1, r.x0))

    new_rects = list(set(new_rects))
    new_rects.sort(key=lambda r: (r.y1, r.x0))  # sort by location
    return [r for r in new_rects if r.width > 5 and r.height > 5]


doc = fitz.open(sys.argv[1])
for page in doc:
    new_rects = detect_rects(page)
    mat = fitz.Matrix(3, 3)  # high resolution matrix
    for i, r in enumerate(new_rects):
        pix = page.get_pixmap(matrix=mat, clip=r)
        pix.save("drawing-%03i-%02i.png" % (page.number, i))
