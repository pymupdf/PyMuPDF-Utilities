"""
Example script: Using PyMuPDF for table analysis
-------------------------------------------------

This script extracts cell content from a table on a PDF page and outputs
a pandas DataFrame (as an Excel file).

The script should work if the following conditions are met:

1. The table is inside a wrapping rectangle (boundary box or "bbox").
2. The table has a clean (row x column) format, no joined cells.
3. Table columns are separable from each other by large enough gaps.

The script executes the following steps:

Step 0: Open file named in the command line, read first page and determine
        the bbox of the table by reading a JSON file with the same filename.
Step 1: Extract the text spans within the bbox.
Step 2: Analyze text spans to compute rectangles: one for each column, one
        for each row. Extract the text found at column / row intersections.
Step 3: Output Python table as a pandas DataFrame (resp. Excel file).

"""
import fitz
import pandas as pd


def main(page, table_bbox):
    page.wrap_contents()
    spans = []
    # extract spans of page
    for b in page.get_text("dict", clip=table_bbox, flags=fitz.TEXTFLAGS_TEXT)[
        "blocks"
    ]:
        for l in b["lines"]:
            for s in l["spans"]:
                spans.append((fitz.Rect(s["bbox"]), s["text"]))

    # sort spans in order top-left to bottom-right
    spans.sort(key=lambda s: (s[0].y1, s[0].x0))
    top = table_bbox.y0
    l_border = min([s[0].x0 for s in spans])
    r_border = max([s[0].x1 for s in spans])
    bot = max([s[0].y1 for s in spans])

    """
    Compute column rectangles:
    Each columns will be represented by a rectangle of table height.
    """
    tspans = sorted(spans, key=lambda s: s[0].x0)  # sort spans by left coordinate
    r = +tspans[0][0]  # take copy of first span bbox, give it max height
    r.y0 = top
    r.y1 = bot
    col_rects = [r]
    for s in tspans[1:]:  # walk through remaining spans
        sr = +s[0]
        sr.y0 = top
        sr.y1 = bot
        found = False
        for i, r in enumerate(col_rects):
            if r.intersects(sr):
                r |= sr
                col_rects[i] = r
                found = True
                break
        if not found:
            col_rects.append(sr)
    # we have the number of columns now

    """
    Determine row separators:
    This may be tough in the general case. Here we compute the average distance
    between lines and assume a new row if a line has an above average distance
    to its predecessor.
    """
    line_bottoms = sorted(list(set([s[0].y1 for s in spans])))
    avg_line_delta = 0

    for i in range(1, len(line_bottoms)):
        avg_line_delta += line_bottoms[i] - line_bottoms[i - 1]

    avg_line_delta /= len(line_bottoms) - 1  # average line distance

    rows = 1
    row_y = []
    for i in range(1, len(line_bottoms)):
        if line_bottoms[i] - line_bottoms[i - 1] > avg_line_delta:
            rows += 1
            row_y.append(line_bottoms[i - 1])

    row_y.append(bot)
    print(f"Table has {rows} rows and {len(col_rects)} columns.")
    row_y.insert(0, top)

    row_rects = []  # make a full width rectangle for each row.
    for i in range(len(row_y) - 1):
        r = fitz.Rect(l_border, row_y[i], r_border, row_y[i + 1])
        row_rects.append(r)

    # store table text in the following cells
    cells = [[""] * (len(col_rects)) for j in range(len(row_rects))]

    # Build intersections of each row / column rectangle and extract text
    # inside as word strings, because we may need to sort them.
    for i, rr in enumerate(row_rects):
        for j, cr in enumerate(col_rects):
            clip = rr & cr  # intersection rectangle
            words = page.get_text("words", clip=clip, sort=True)
            cells[i][j] = " ".join([w[4] for w in words])

    # Now create the pandas DataFrame
    pd_dict = {}  # preapre dictionary
    hdr = cells[0]  # first line contains the column header strings

    for i in range(len(hdr)):
        key = hdr[i].strip()
        if not key:  # column header may be empty!
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
