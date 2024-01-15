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
    # we need to exclude meaningless graphics that e.g. paint a white
    # rectangle on the full page.
    delta = (-1, -1, 1, 1)  # enlarge every path rect by this
    parea = abs(page.rect) * 0.8  # area of the full page (80%)

    # exclude graphics that are too large
    paths = [p for p in page.get_drawings() if abs(p["rect"]) < parea]

    # make a list of vector graphics rectangles (IRects are sufficient)
    prects = sorted(
        [(p["rect"] + delta).irect for p in paths], key=lambda r: (r.y1, r.x0)
    )

    new_rects = []  # the final list of the joined rectangles

    # -------------------------------------------------------------------------
    # The strategy is to identify and join all rects that have at least one
    # point in common.
    # -------------------------------------------------------------------------
    while prects:  # the algorithm will empty this list
        prects_len = len(prects)  # current list length
        r = prects[0]  # first rectangle
        repeat = True
        while repeat:
            for i in range(prects_len - 1, -1, -1):  # back to front
                if i == 0:  # don't touch first rectangle
                    continue
                if r.intersects(prects[i]):
                    r |= prects[i]  # join in to first rect
                    prects[0] = +r  # copy to list item
                    del prects[i]  # delete this rect
            prects_len = len(prects)  # length may have changed

            # This is true if remainings touch the updated first one.
            # Otherwise the while ends.
            repeat = any([r.intersects(prects[i]) for i in range(1, prects_len)])

        # move first item over to result list
        new_rects.append(prects.pop(0))
        prects={f'{prect.x0}_{prect.y0}_{prect.x1}_{prect.y1}':prect for prect in prects}
        prects = sorted(list(prects.values()), key=lambda r: (r.y1, r.x0))

    new_rects={f'{new_rect.x0}_{new_rect.y0}_{new_rect.x1}_{new_rect.y1}':new_rect for new_rect in new_rects}
    new_rects = sorted(list(new_rects.values()), key=lambda r: (r.y1, r.x0))
    return [r for r in new_rects if r.width > 5 and r.height > 5]


doc = fitz.open(sys.argv[1])
for page in doc:
    new_rects = detect_rects(page)
    mat = fitz.Matrix(3, 3)  # high resolution matrix
    for i, r in enumerate(new_rects):
        pix = page.get_pixmap(matrix=mat, clip=r)
        pix.save("drawing-%03i-%02i.png" % (page.number, i))
