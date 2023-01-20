"""
Example script: Using PyMuPDF for table analysis
-------------------------------------------------

This script extracts cell content from a table on a PDF page and outputs
a CSV file representing it.

The script will work successfully if the following conditions are met:

1. The table has been / can be identified by a wrapping rectangle ("clip").
2. The table has a clean (row x column) format.
3. Each table cell is wrapped by "gridlines", (vector graphics).

The script executes the following steps:

Step 0: Identify a clip rectangle containing the table. This may work by
        identifying text keyword coordinates (the example presented here)
        or by whatever other mechanism, e.g. information passed in.
Step 1: Extract x- and y-coordinates of vector graphic lines. They are
        being used as cell borders to determine the right cell for each
        piece of text. Create a corresponding Python table with empty text
        cells.
Step 2: Extract page text pieces ("spans") within the clip and sort them
        by vertical, then horizontal coordinates. Sorting is required to
        ensure correct sequence of multi-line table cell text content.
        For each text piece, append it to the respective cell text.
Step 3: Output Python table as CSV file.

"""
import fitz

# -------------------------------------------------------------------------
# Make minimal wrapping rectangles:
# Text extraction and searches deliver rectangles with no extra room above
# and below text: their heights will equal the font size.
# Popular fonts have higher line rectangles, e.g. Helvetica has a rectangle
# height which is 37.4% larger than the font size.
# -------------------------------------------------------------------------
fitz.Tools().set_small_glyph_heights(True)

doc = fitz.open("your.pdf")
page = doc[0]  # your page, use 0-based numbers

# -------------------------------------------------------------------------
# Step 0: Identify clip rectangle
# Look up top and bottom coordinates for relevant data, potentially also
# left and right borders.
# The following is just kidding: it assumes that there exist unique text
# pieces above and below the table and searches for them. Then uses their
# hit rectangles to compute the vertical limits 'top' and 'bottom'.
# Your situation will be different!
# -------------------------------------------------------------------------
top = page.search_for("text above")[0].y1  # bottom y of rectangle
bot = page.search_for("text below")[0].y0  # top y of rectangle

# so we extract table data from within the following rectangle, which is made
# from left, top, right, bottom coordinates.
clip = fitz.Rect(0, top, page.rect.width, bot)

# -------------------------------------------------------------------------
# Step 1: Compute x-, y-coordinates of cell borders
# Find table border line coordinates
# -------------------------------------------------------------------------
paths = page.get_drawings()  # all line art / vector graphics on page

# vertical / horizontal line coordinates. Python 'sets' avoid duplicates.
vert = set()  # vertical (x-) coordinates
hori = set()  # horizontal (y-) coordinates

for p in paths:  # iterate over vector graphis to find the lines
    if not p["rect"] in clip:  # omit stuff outside clip
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
hori = sorted(list(hori))  # sorted, without duplicates

# Define a Python table with followingse values:
#   * has len(hori)-1 rows
#   * every row has len(vert)-1 columns
cells = [[""] * (len(vert) - 1) for j in range(len(hori) - 1)]

# -------------------------------------------------------------------------
# Step 2: Extract text spans
# Extract and sort text spans. We use the "dict" output format.
# -------------------------------------------------------------------------

spans = []  # list of text pieces present in each cell on the page

textdict = page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT, clip=clip)
for block in textdict["blocks"]:
    for line in block["lines"]:
        for span in line["spans"]:
            spans.append(span)  # is text dict within whatever cell

spans.sort(key=lambda s: (s["bbox"][3], s["bbox"][0]))


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


# put the text pieces into the Python cells
for s in spans:
    ridx, cidx = getcoord(fitz.Rect(s["bbox"]), s["text"])
    cells[ridx][cidx] += s["text"]  # append to stuff already in that cell

# -------------------------------------------------------------------------
# Step 3: Output the CSV file
# -------------------------------------------------------------------------
out = open("table.csv", "w")
for row in cells:
    out.write(";".join(row) + "\n")
out.close()
