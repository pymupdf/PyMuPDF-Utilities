import sys
from pprint import pprint

import fitz

from extractGraphic import extractGraphic

infile = sys.argv[1]
outfile = infile.replace(".pdf", "-new.pdf")
doc = fitz.open(infile)
new = fitz.open()

for page in doc:
    rect = page.rect  # get page dimensions
    # new page containing recreated drawings
    newpage = new.newPage(width=rect.width, height=rect.height)
    # extract drawings as a list of draw paths
    # each path is a dictionary of properties and a list of draw commands
    paths = extractGraphic(page)
    # create a shape / canvas to draw upon
    shape = newpage.newShape()
    for path in paths:  # loop through the paths
        for item in path["items"]:  # these are the draw commands
            if item[0] == "l":  # line
                shape.drawLine(item[1], item[2])
            elif item[0] == "re":  # rectangle
                shape.drawRect(item[1])
            elif item[0] == "qu":  # quad
                shape.drawQuad(item[1])
            elif item[0] == "c":  # curve
                shape.drawBezier(item[1], item[2], item[3], item[4])
            else:
                raise ValueError("unhandled drawing", item)
        shape.finish(  # end of path - output
            fill=path["fill"],
            color=path["stroke"],
            dashes=path["dashes"],
            even_odd=path["even_odd"],
            closePath=path["closePath"],
            lineJoin=path["lineJoin"],
            lineCap=path["lineCap"],
            width=path["width"],
        )
    # all drawings processed - commit to the page
    shape.commit()
    shape = None
    newpage = None
new.save(outfile)

