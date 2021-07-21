"""
@created: 2021-07-08

@author: (c) Harald Lieder, harald.lieder@outlook.com, 2021

Extract document text preserving layout
---------------------------------------
This script extracts the text of a document and produces a text file.
It tries to position the text such that it resembles the original layout.

Approach
--------
Iterate through the pages and ...

* Extract the text via page.get_text("rawdict").

* Place each character in the most appropriate position to resemble
  the original.


TODOs, Missing Features, Limitations
------------------------------------
* Doubled text mimicking bold or similar effects are not yet handled.
* Can only handle text in horizontal, top-left to bottom-right mode,
  other text is ignored.


Dependencies
------------
PyMuPDF v1.18.14


License
-------
GNU AFFERO GPL 3.0

Copyright
---------
(c) 2021 Harald Lieder

Changes
-------
2021-07-10:
Use the span's origin to define the line y-coordinate, instead of the
bbox. This improves matching characters belonging to the same line.
There also is a small performance doing this on span level.

2021-07-11:
Add logic to eliminate character duplicates, i.e. multiple same characters
in (almost) the same place.
"""
import sys

import fitz

if not tuple(map(int, fitz.VersionBind.split("."))) >= (1, 18, 14):
    raise ValueError("Need PyMuPDF v1.18.14 or higher.")

GRID = 2  # join lines with distances less than this


def process_page(page, textout):
    left = page.rect.width  # left most used coordinate
    right = 0  # rightmost coordinate
    rowheight = page.rect.height  # smallest row height in use
    chars = []  # list of all char dicts here
    rows = []  # bottom coordinates of the lines

    # --------------------------------------------------------------------
    def find_line_index(values, value):
        """Find the right row coordinate.

        Args:
            values: (list) y-coordinates of rows.
            value: (float) lookup for this value
        Returns:
            Index (int) for the appropriate line of value.
        """
        diffs = [abs(value - v) for v in values]
        return diffs.index(min(diffs))

    # --------------------------------------------------------------------
    def get_textline(left, slot, chars):
        """Produce the text of one line.

        Args:
            left: (float) left most coordinate used
            slot: (float) minimum width of one character in any font in use.
            chars: (list[dict]) characters of this line
        Returns:
            text: (str) text string for this line
        """
        text = ""  # we output this
        old_x0 = 0  # start coordinate of last char
        old_x1 = 0  # end coordinate of last char
        old_orig = 0  # x-origin of last char
        for c in chars:  # loop over characters
            bbox = fitz.Rect(c["bbox"])  # char bbox
            x0 = bbox.x0 - left  # its (relative) start coordinate
            x1 = bbox.x1 - left  # ending coordinate
            ox = c["origin"][0] - left  # char origin.x
            char = c["c"]  # the character
            if (
                old_x0 <= ox < old_x1 and char == text[-1] and abs(ox - old_orig) <= 1
            ):  # eliminate overprints
                continue
            if x0 < old_x1 + slot / 2:  # close enough after previous?
                text += char  # append to output
                old_x1 = x1  # new end coord
                old_x0 = x0
                old_orig = ox
                continue
            # next char starts after some gap:
            # fill it with right number of spaces, so char is positioned
            # in the right slot of the line
            delta = x0 / slot - len(text)
            if x0 > old_x1 and delta > 0:
                text += " " * int(round(delta))
            # now append char
            text += char
            old_x1 = x1  # new end coordinate
            old_x0 = x0  # new start coordinate
            old_orig = ox  # new origin
        return text

    # extract page text by single characters ("rawdict")
    # keep white space and ligatures, omit images
    blocks = page.get_text(
        "rawdict",
        flags=fitz.TEXT_PRESERVE_WHITESPACE,
        clip=page.rect,
    )["blocks"]

    for block in blocks:
        left = min(left, block["bbox"][0])  # update left coordinate
        right = max(right, block["bbox"][2])  # update right coordinate
        for line in block["lines"]:
            if line["dir"] != (1, 0):  # ignore non-horizontal text
                continue
            # upd row height
            rowheight = min(rowheight, line["bbox"][3] - line["bbox"][1])
            for span in line["spans"]:
                rows.append(round(span["origin"][1]))
                for char in span["chars"]:
                    chars.append(char)  # list of all chars on page

    # compute list of line coordinates - ignoring 'GRID' differences
    rows = list(set(rows))  # omit duplicates
    rows.sort()  # sort ascending
    nrows = [rows[0]]
    for h in rows[1:]:
        if h >= nrows[-1] + GRID:  # only keep significant differences
            nrows.append(h)
    rows = nrows  # curated list of line bottom coordinates

    # sort char dicts by x-coordinates
    chars.sort(key=lambda c: (c["bbox"][2], c["bbox"][0]))
    # assign char dicts to the right lines on page
    lines = {}  # key: y1-ccordinate, value: char list
    for c in chars:
        i = find_line_index(rows, c["origin"][1])  # index of the right y
        y = rows[i]  # the right line
        lchars = lines.get(y, [])  # read line chars so far
        if c not in lchars:
            lchars.append(c)  # append this char
        lines[y] = lchars  # write back to line

    # ensure line coordinates are ascending
    keys = list(lines.keys())
    keys.sort()

    # Compute minimum char width ("slot"):
    # For each line compute how many of its chars would fit in between
    # left and right. Take the max of these numbers.

    chars_per_line = 0  # max chars per line
    for k in keys:
        lchars = lines[k]
        widths = sum([fitz.Rect(c["bbox"]).width for c in lchars])
        chars_this_line = len(lchars) / widths * (right - left)
        chars_per_line = max(chars_per_line, chars_this_line)

    # smallest char width
    slot = (right - left) / chars_per_line

    # compute line advance in text output
    rowheight = rowheight * (rows[-1] - rows[0]) / (rowheight * len(rows)) * 1.2
    rowpos = rows[0]  # first line positioned here
    textout.write(b"\n")
    for k in keys:  # walk through the lines
        while rowpos < k:  # honor distance between lines
            textout.write(b"\n")
            rowpos += rowheight
        text = get_textline(left, slot, lines[k])
        textout.write((text + "\n").encode("utf8"))
        rowpos = k + rowheight

    textout.write(bytes([12]))  # write formfeed


def main(*args):
    if not args:
        filename = sys.argv[1]
    else:
        filename = args[0]
    doc = fitz.open(filename)
    textout = open(filename.replace(".pdf", ".txt"), "wb")
    for page in doc:
        if page.get_text():
            process_page(page, textout)
    textout.close()


if __name__ == "__main__":
    main()
