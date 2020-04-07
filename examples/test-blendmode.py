"""
Purpose
--------
This utility is an example application of PyMuPDF to demonstrate the
(rather complex) influencing factors background and text colors, opacity and
blend mode for the appearance of an annotation.
For each of the standard PDF blend modes (as defined in the manual
http://www.adobe.com/content/dam/Adobe/en/devnet/acrobat/pdfs/pdf_reference_1-7.pdf
pages 520+) it generates a highlight annotation which uses it.

Date of creation: 2020-03-27
Dependcy: PyMuPDF v1.16.15 or later

Copyright
----------
(c) 2020, Jorj McKie, mailto:<jorj.x.mckie@outlook.de>

License
--------
GNU GPL 3.0 or later, uses MuPDF v1.16.0 by Artifex Software Inc. licensed
under GNU AGPL 3.0

"""
import os

import fitz

print(fitz.__doc__)
thisdir = lambda f: os.path.join(os.path.dirname(__file__), f)

blend_modes = (
    fitz.PDF_BM_ColorBurn,
    fitz.PDF_BM_ColorDodge,
    fitz.PDF_BM_Darken,
    fitz.PDF_BM_Difference,
    fitz.PDF_BM_Exclusion,
    fitz.PDF_BM_HardLight,
    fitz.PDF_BM_Lighten,
    fitz.PDF_BM_Multiply,
    fitz.PDF_BM_Normal,
    fitz.PDF_BM_Overlay,
    fitz.PDF_BM_Screen,
    fitz.PDF_BM_SoftLight,
    fitz.PDF_BM_Hue,
    fitz.PDF_BM_Saturation,
    fitz.PDF_BM_Color,
    fitz.PDF_BM_Luminosity,
)


def table(rect=(0, 0, 1, 1), cols=1, rows=1):
    """Return a list of (rows x cols) equal sized rectangles.

    Notes:
        A little utility to fill a given area with table cells of equal size.
    Args:
        rect: rect_like to use as the table area
        rows: number of rows
        cols: number of columns
    Returns:
        A list with <rows> items, where each item is a list of <cols>
        PyMuPDF Rect objects of equal sizes.
    """
    rect = fitz.Rect(rect)  # ensure that this is a Rect
    if rect.isEmpty or rect.isInfinite:
        raise ValueError("rect must be finite and not empty")
    tl = rect.tl

    # compute width and height of one table cell
    height = rect.height / rows
    width = rect.width / cols

    # first rectangle
    r = fitz.Rect(tl, tl.x + width, tl.y + height)

    delta_h = (width, 0, width, 0)  # diff to next right rect
    delta_v = (0, height, 0, height)  # diff to next lower rect

    row = [r]  # make the first row
    for i in range(1, cols):
        r += delta_h  # build next rect to the right
        row.append(r)

    rects = [row]  # make the result starting with the first row
    for i in range(1, rows):
        row = rects[i - 1]  # take previously appended row
        nrow = []  # the new row to append
        for r in row:  # for each previous cell add its downward copy
            nrow.append(r + delta_v)
        rects.append(nrow)  # append new row to result

    return rects


doc = fitz.open()  # new PDF
page = doc.newPage()  # new page
shape = page.newShape()  # make a page draw area
opacity = 0.3  # all annotation use this opacity
tcol = (0, 0, 1)  # text color
gold = (1, 1, 0)  # highlight color
bg_color = "skyblue3"
background = fitz.utils.getColor(bg_color)  # background color
fname = "hebo"  # Helvetica Bold
fsize = 12  # generous font size
tl = page.rect.tl + (150, 100)
br = page.rect.br - (150, 62)
rect = fitz.Rect(tl, br)  # only use this area of the page

rects = table(  # define a table with 2 cells per blend mode
    rows=len(blend_modes),  # one row per blend mode
    cols=2,  # for the blend mode and its highlighted version
    rect=rect,  # inside this rectangle
)

# paint page background
# will provide better visibility of highlighted text
shape.drawRect(page.rect)
shape.finish(fill=background, color=background)

# fill the table
for i, bmode in enumerate(blend_modes):
    r = rects[i]  # contains 2 rectangles
    text = "\n" + bmode  # try to center the name a bit
    shape.insertTextbox(  # blend mode name in left rectangle
        r[0],
        text,
        fontsize=fsize,
        color=tcol,
        fontname=fname,
        align=fitz.TEXT_ALIGN_CENTER,
    )
    shape.insertTextbox(  # blend mode name in right rectangle
        r[1],
        text,
        fontsize=fsize,
        color=tcol,
        fontname=fname,
        align=fitz.TEXT_ALIGN_CENTER,
    )

shape.insertTextbox(
    (80, 36, page.rect.width - 80, 70),
    "Show how blend mode, opacity %g and background\ncolor '%s' affect a highlight annotation"
    % (opacity, bg_color.upper()),
    fontname=fname,
    color=tcol,
    fontsize=fsize,
    align=fitz.TEXT_ALIGN_CENTER,
)

shape.commit()  # this commits text and paintings to the page

# Now add highlight annotations for text in the right column.
# To find the respective text, we search for the blend mode name,
# then take its second occurrence for highlighting
for i, bmode in enumerate(blend_modes):
    annot = page.addHighlightAnnot(rects[i][1])  # take second one
    annot.update(blend_mode=bmode, opacity=opacity)  # and finish the annotation

doc.save(thisdir("test-blendmode.pdf"), garbage=3, deflate=True)
