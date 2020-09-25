# Extracting Drawings from a PDF Page with PyMuPDF
This utility module walks through a PDF page's ``/Contents`` objects and interprets drawings. These are things composed of elementary commands defining lines, curves and rectangles, including their properties like colors and line dashing.

PDF combines these commands in so-called **_paths_**, which can become complex graphics or other objects.

The module returns a list of such paths by converting each PDF path into a Python dictionary. The path dictionary can subsequently be used for a number of purposes.

* Reproduce the path drawing on some other page by using the draw commands of the ``Shape`` class.
* Use the lines, rectangles or curves of a path to locate table borders, help with text positioning or similar.
* Simply make lists e.g. of all lines or all rectangles on the page, potentially subselecting them by properties like fill color or location.

This is the definition of a path dictionary:

```python
{'closePath': False,  # whether to connect last and first path point
 'dashes': '',  # controls line dashing
 'even_odd': True,  # controls colors of overlapping path areas
 'fill': None,  # fill color
 'lineCap': 0,  # controls roundness of line ends
 'lineJoin': 0,  # controls roundness of line join edges
 'stroke': None,  # stroke (line) color
 'width': 0,  # line width
 'rect': rect,  # fitz.Rect surrounding the path
 'items': [...],  # list of draw commands
}
 ```

The ``items`` list contains any number of these entries:

```python
("l", p1, p2)  # line from p1 to p2 (fitz.Points)
("c", p1, p2, p3, p4)  # Bezier curve from p1 to p4, two control points
("re", rect)  # rectangle (fitz.Rect)
("qu", quad)  # rotated original rectangle (fitz.Quad)
```

Multiple consecutive entries in ``items`` in a path indicate a compound drawing. Draw commands are **_"chained"_** together: in general, this implies that the **_last point_** of an entry **_must equal_** the first point of the following entry. But rectangles and quads are drawn starting and ending with the **_top-left_** corner - so this point must be used for chaining.

The programmer must take this into account when modifying a path.

> **Hint:** If encountering 4 consecutive connected Bezier curves "c", then they in often cases jointly define a **_circle_**, because circles need 4 Bezier curves which each form a quarter perimeter. To confirm, check whether ``path["rect"]`` is a square.

> This session draws a circle with radius 100 around the center (300,300) and then extracts this drawing from the page:

```python
>>> import fitz
>>> from pprint import pprint
>>> from extractGraphic import extractGraphic
>>> doc=fitz.open()
>>> page=doc.newPage()
>>> center = fitz.Point(300,300)
>>> radius = 100
>>> blue = (0,0,1)
>>> gold = (1,1,0)
>>> page.drawCircle(center, radius,color=blue, fill=gold, width=0.3)
Point(200.0, 299.99999999999994)
>>> paths=extractGraphic(page)
>>> pprint(paths)
[{'closePath': True,
  'dashes': '',
  'even_odd': False,
  'fill': [1.0, 1.0, 0.0],
  'items': [('c',
             Point(200.0, 300.0),
             Point(200.0, 355.2279968261719),
             Point(244.77200317382812, 400.0),
             Point(300.0, 400.0)),
            ('c',
             Point(300.0, 400.0),  # equals last point of previous "c"
             Point(355.2279968261719, 400.0),
             Point(400.0, 355.2279968261719),
             Point(400.0, 300.0)),
            ('c',
             Point(400.0, 300.0),
             Point(400.0, 244.77197265625),
             Point(355.2279968261719, 200.0),
             Point(300.0, 200.0)),
            ('c',
             Point(300.0, 200.0),
             Point(244.77200317382812, 200.0),
             Point(200.0, 244.77197265625),
             Point(200.0, 300.0))],  # equals first point of first "c"
  'lineCap': 0,
  'lineJoin': 0,
  'rect': Rect(200.0, 200.0, 400.0, 400.0),  # square around the circle
  'stroke': [0.0, 0.0, 1.0],
  'width': 0.3}]
>>> 
```

To reproduce a path drawing use code like this:

```python
paths = extractGraphic(src_page)
...
shape = tar_page.newShape()  # make a Shape to draw on target page
for path in paths:  # loop through the paths
    for item in path["items"]:  # these are the draw commands
        if item[0] == "l":  # line
            shape.drawLine(item[1], item[2])
        elif item[0] == "re":  # rectangle
            shape.drawRect(item[1])
        elif item[0] == "qu":  # quad
            shape.drawQuad(item[1])
        elif item[0] == "c":  # Bezier curve
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
# all drawings processed - commit them to the page
shape.commit(overlay=True)
```

This is a new utility. Although it has been tested with about 20 PDF files ranging from elementary drawings to complex CAD-based files, it is still in its early stages. So, errors must be expected like e.g. undetected drawings, or wrong coordinates reported.

In addition, there are **_known_** shortcomings with respect to the **_reproduction_** of drawings, which may be resolved in future versions:

* Drawing parameters controlled by separate graphics state dictionaries (see page 219 [here](https://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/pdf_reference_1-7.pdf)) are currently ignored. This most prominently pertains to opacity / transparency, but also to
* BlendMode, which controls drawing coloration given a certain background color.
* Shading is not supported.

## Example Uses
### Create a List of all Lines, Rectangles, Quads
Line and rectangle drawings may be useful for detecting the location of tabular information on a page.
```python
lines = []
rects = []
quads = []
for path in paths:
    for item in path["items"]:
        if item[0] == "l":
            lines.append((item[1], item[2]))
        elif item[0] == "re":
            rects.append(item[1])
        elif item[0] == "qu":
            quads.append(item[1])
```

