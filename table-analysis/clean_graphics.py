"""
This little utility inspects the vector graphics of a page and consolidates
their rectangles whenever it finds intersections.

This should help finding disjoint drawings for creating respective images
or detecting tables.
"""


def clean_graphics(page):
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

    new_rects = []  # the final list of joined rectangles

    # -------------------------------------------------------------------------
    # Strategy: join rects that have at least one point in common.
    # -------------------------------------------------------------------------
    while prects:  # the algorithm will empty this list
        r = prects[0]  # first rectangle
        repeat = True
        while repeat:
            repeat = False
            for i in range(len(prects) - 1, -1, -1):  # run backwards
                if i == 0:  # don't touch first rectangle
                    continue
                if r.intersects(prects[i]):
                    r |= prects[i]  # join in to first rect
                    prects[0] = +r  # update first
                    del prects[i]  # delete this rect
                    repeat = True

        # move first item over to result list
        new_rects.append(prects.pop(0))
        prects = sorted(list(set(prects)), key=lambda r: (r.y1, r.x0))

    new_rects = sorted(list(set(new_rects)), key=lambda r: (r.y1, r.x0))
    return [r for r in new_rects if r.width > 5 and r.height > 5]
