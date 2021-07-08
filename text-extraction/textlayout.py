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
  the original


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

"""
import sys

import fitz

if not tuple(map(int, fitz.VersionBind.split("."))) >= (1, 18, 14):
    raise ValueError("Need PyMuPDF v1.18.14 or higher.")

GRID = 1  # join lines with distances less than this


def process_page(page, textout):
    left = page.rect.width  # left most used coordinate
    right = 0  # rightmost coordinate
    rowheight = page.rect.height  # the minimum row height in use

    def find_line_index(values, item):
        """Find the right row coordinate.

        Args:
            values: (list) y-coordinates of rows.
        Returns:
            index (int) for the appropriate line.
        """
        diffs = [abs(item - v) for v in values]
        i = diffs.index(min(diffs))
        return i

    def get_textline(left, slot, chars):
        """Produce the text of one line.

        Args:
            left: (float) left most coordinate used
            slot: (float) minimum width of one character in any font in use.
            chars: (list[dict]) characters of this line
        Returns:
            text: (str) text string for this line
        """
        chars.sort(
            key=lambda c: (c["bbox"][2], c["bbox"][0])
        )  # sort chars by horizontal coordinates
        text = ""  # we output this
        old_x1 = 0  # end coordinate of last char written
        for c in chars:  # walk through characters
            bbox = fitz.Rect(c["bbox"])  # char bbox
            x0 = bbox.x0 - left  # its (relative) start coordinate
            x1 = bbox.x1 - left  # ending coordinate
            char = c["c"]  # the character
            if x0 < old_x1 + slot / 2:  # close enough after previous?
                text += char  # append to output
                old_x1 = x1  # new end coord
                continue
            # char starts at a greater distance:
            # fill gap with appropriate spaces
            if x0 > old_x1 and x0 / slot > len(text):
                spaces = int((x0 / slot - len(text)))
                text += " " * spaces
            # now append char
            text += char
            old_x1 = x1
        return text

    # extract page text by single characters ("rawdict")
    # keep white space and ligatures, omit images
    blocks = page.get_text(
        "rawdict",
        flags=fitz.TEXT_PRESERVE_WHITESPACE,
        clip=page.rect,
    )["blocks"]
    chars = []
    for b in blocks:
        for l in b["lines"]:
            if l["dir"] != (1, 0):  # ignore non-horizontal text
                continue
            for s in l["spans"]:
                for c in s["chars"]:
                    chars.append(c)  # list of all chars on page
                    bbox = fitz.Rect(c["bbox"])
                    left = min(left, bbox.x0)  # update left coordinate
                    right = max(right, bbox.x1)  # update right coordinate
                    rowheight = min(rowheight, bbox.height)  # upd row height

    # compute list of line coordinates - ignore minute differences
    rows = [c["bbox"][3] for c in chars]
    rows = list(set(rows))  # omit duplicates
    rows.sort()  # sort ascending
    nrows = [rows[0]]
    for h in rows[1:]:
        if h >= nrows[-1] + GRID:  # only keep significant differences
            nrows.append(h)
    rows = nrows

    # assign char dicts to the lines on page
    lines = {}  # key: y1-ccordinate, value: char list
    for c in chars:
        i = find_line_index(rows, c["bbox"][3])
        y = rows[i]  # coord of appropriate line
        lchars = lines.get(y, [])
        if c not in lchars:
            lchars.append(c)
        lines[y] = lchars

    # ensure line coordinates are ascending
    keys = list(lines.keys())
    keys.sort()

    # compute char count per line and minimum char width
    chars_per_line = 0  # max chars in any line
    for k in keys:
        lchars = lines[k]
        widths = 0
        for c in lchars:
            bbox = fitz.Rect(c["bbox"])
            widths += bbox.width
        char_count = round(len(lchars) / widths * (right - left))
        chars_per_line = max(chars_per_line, char_count)

    # smallest char width
    slot = (right - left) / chars_per_line

    # compute line advance in text output
    rowheight = rowheight * page.rect.height / (rowheight * len(rows))
    rowpos = rowheight  # first line positioned after this
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
        process_page(page, textout)
    textout.close()


if __name__ == "__main__":
    main()
