"""
Example script: Using PyMuPDF for table analysis
-------------------------------------------------

This script extracts cell content from a table on a PDF page and outputs
a pandas DataFrame (as an Excel file).

The script should work if the following conditions are met:

1. The table is inside a wrapping rectangle (boundary box or "bbox").
2. The table has a clean (row x column) format, no joined cells.
3. Table cell are wrapped by "gridlines" (vector graphics).

The script executes the following steps:

Step 0: Open file named in the command line, read first page and determine
        the bbox of the table by reading a JSON file with the same filename.
Step 1: Extract x- and y-coordinates of vector graphic lines. They are
        used as cell borders.
Step 2: Extract page text as single words and put each word string in the
        adequate cell.
Step 3: Output Python table as a pandas DataFrame (resp. Excel file).

"""
import fitz
import pandas as pd

"""
-------------------------------------------------------------------------
Make minimal boundary boxes:
Text extraction and searches deliver rectangles with no extra room above
and below: their heights will equal the font size.
Popular fonts have higher line rectangles, e.g. Helvetica has a height
that is 37.4% larger than the font size. This may cause problems when
trying to fit strings in externally defined rectangles - as is the case
with gridlines.
-------------------------------------------------------------------------
"""
fitz.Tools().set_small_glyph_heights(True)


def main(page, table_bbox):
    """Extract table structure defined by gridlines within given table_bbox."""

    # vertical / horizontal line coordinates. Python 'sets' avoid duplicates.
    vert = set()  # vertical (x-) coordinates
    hori = set()  # horizontal (y-) coordinates

    def clean_list(values):
        """Remove items from values that are too close to predecessor."""
        for i in range(len(values) - 1, 0, -1):
            v1 = values[i]
            v0 = values[i - 1]
            if v1 - v0 <= 3:  # too close to predecessor
                del values[i]

    def getcoord(bbox, text):
        """Find ridx / cidx index for given text rectangle.

        We need the text only for error messages.
        """
        cidx = -1  # col index
        ridx = -1  # row index
        for i in range(len(vert) - 1):
            if vert[i] <= bbox.x0 < bbox.x1 <= vert[i + 1]:
                cidx = i
                break
        for j in range(len(hori) - 1):
            if hori[j] <= bbox.y0 < bbox.y1 <= hori[j + 1]:
                ridx = j
                break
        # if ridx / cidx is negative, text is contained in no table cell
        if cidx < 0 or ridx < 0:  # shouldn't happen: correct cell not found
            raise ValueError(ridx, cidx, f"=> no cell found for: '{text}'")
        return ridx, cidx  # ridx, cidx index

    # -------------------------------------------------------------------------
    # Step 1: Determine column and row borders and prepare empty Python table
    # -------------------------------------------------------------------------
    paths = page.get_drawings()  # all line art / vector graphics on page

    for p in paths:  # iterate over vector graphis to find the lines
        if not p["rect"] in table_bbox:  # omit stuff outside table_bbox
            continue
        for item in p["items"]:  # look at lines and "thin" rectangles
            if item[0] == "l":  # a line
                p1, p2 = item[1:]  # start and stop points
                if p1.x == p2.x:  # a vertical line!
                    vert.add(p1.x)  # store this column border
                elif p1.y == p2.y:  # a horizontal line!
                    hori.add(p1.y)  # store this row border

            # many apparent 'lines' are thin rectangles really ...
            elif item[0] == "re":  # a rectangle item
                rect = item[1]  # rect coordinates
                if rect.width <= 3 and rect.height > 10:
                    vert.add(rect.x0)  # thin vertical rect: treat like col border
                elif rect.height <= 3 and rect.width > 10:
                    hori.add(rect.y1)  # treat like row border

    vert = sorted(list(vert))  # sorted, without duplicates
    clean_list(vert)  # remove "almost" duplicate coordinates
    hori = sorted(list(hori))  # sorted, without duplicates
    clean_list(hori)  # remove "almost" duplicate coordinates

    # Define a Python table with following values:
    #   * has len(hori)-1 rows
    #   * every row has len(vert)-1 columns
    cells = [[""] * (len(vert) - 1) for j in range(len(hori) - 1)]

    # -------------------------------------------------------------------------
    # Step 2: Extract and sort text words
    # -------------------------------------------------------------------------
    # put the text pieces into the Python cells
    for w in page.get_text(
        "words",
        flags=fitz.TEXTFLAGS_TEXT & ~fitz.TEXT_PRESERVE_LIGATURES,
        sort=True,
        clip=table_bbox,
    ):
        ridx, cidx = getcoord(fitz.Rect(w[:4]), w[4])
        cells[ridx][cidx] += w[4] + " "  # append to stuff already in that cell

    # -------------------------------------------------------------------------
    # Step 3: Output as a pandas DataFrame. Row 0 contains column names.
    # -------------------------------------------------------------------------
    pd_dict = {}
    hdr = cells[0]

    for i in range(len(hdr)):
        key = hdr[i].strip()
        if not key:  # may be empty!
            key = f"Col{i}"
        value = []
        for j in range(1, len(cells)):
            value.append(cells[j][i].strip())
        pd_dict[key] = value
    return pd.DataFrame(pd_dict)


if __name__ == "__main__":
    import json
    import pathlib
    import sys

    filename = sys.argv[1]
    doc = fitz.open(filename)
    page = doc[0]
    # Locate table on page.
    # Assuming here, that we can access a JSON version.
    clip = json.loads(pathlib.Path(filename.replace(".pdf", "-bbox.json")).read_text())
    clip = fitz.Rect(clip)
    df = main(page, clip)
    df.to_excel(doc.name + ".xlsx")
