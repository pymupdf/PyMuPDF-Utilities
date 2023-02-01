"""
Return a Python list of lists from the words found in a fitz.Document page
-------------------------------------------------------------------------------
License: GNU GPL V3
(c) 2018 Jorj X. McKie

Usage
-----
Used by extract.py and wx-extract.py

Notes
-----
(1) Works correctly for simple, non-nested tables only.

(2) Line recognition depends on the coordinates of the detected words in the
    rectangle. These will be round to integer (pixel) values. However, use of
    different fonts, scan inaccuracies, and so on, may lead to artefacts line
    differences, which must be handled by the caller.

Dependencies
-------------
PyMuPDF v1.12.0 or later
"""

from operator import itemgetter
from itertools import groupby
import fitz


# ==============================================================================
# Function ParseTab - parse a document table into a Python list of lists
# ==============================================================================
def ParseTab(page, bbox, columns=None):
    """Returns the parsed table of a page in a PDF / (open) XPS / EPUB document.
    Parameters:
    page: fitz.Page object
    bbox: containing rectangle, list of numbers [xmin, ymin, xmax, ymax]
    columns: optional list of column coordinates. If None, columns are generated
    Returns the parsed table as a list of lists of strings.
    The number of rows is determined automatically
    from parsing the specified rectangle.
    """
    tab_rect = fitz.Rect(bbox).irect
    xmin, ymin, xmax, ymax = tuple(tab_rect)

    if tab_rect.is_empty or tab_rect.is_infinite:
        print("Warning: incorrect rectangle coordinates!")
        return []

    if type(columns) is not list or columns == []:
        coltab = [tab_rect.x0, tab_rect.x1]
    else:
        coltab = sorted(columns)

    if xmin < min(coltab):
        coltab.insert(0, xmin)
    if xmax > coltab[-1]:
        coltab.append(xmax)

    words = page.get_text("words")

    if words == []:
        print("Warning: page contains no text")
        return []

    alltxt = []

    # get words contained in table rectangle and distribute them into columns
    for w in words:
        ir = fitz.Rect(w[:4]).irect  # word rectangle
        if ir in tab_rect:
            cnr = 0  # column index
            for i in range(1, len(coltab)):  # loop over column coordinates
                if ir.x0 < coltab[i]:  # word start left of column border
                    cnr = i - 1
                    break
            alltxt.append([ir.x0, ir.y0, ir.x1, cnr, w[4]])

    if alltxt == []:
        print("Warning: no text found in rectangle!")
        return []

    alltxt.sort(key=itemgetter(1))  # sort words vertically

    # create the table / matrix
    spantab = []  # the output matrix

    for y, zeile in groupby(alltxt, itemgetter(1)):
        schema = [""] * (len(coltab) - 1)
        for c, words in groupby(zeile, itemgetter(3)):
            entry = " ".join([w[4] for w in words])
            schema[c] = entry
        spantab.append(schema)

    return spantab
