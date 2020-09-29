# Extracting Drawings from a PDF Page with PyMuPDF
This utility module walks through a PDF page's ``/Contents`` objects and interprets drawings. These are things composed of elementary commands defining lines, curves and rectangles, including their properties like colors and line dashing.

PDF combines these commands in so-called **_paths_**, which can become complex graphics or other objects. [Here](https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/shapes/symbol-list.pdf) is an example.

The module returns a list of such paths by converting each PDF path into a Python dictionary. This path dictionary can subsequently be used for a number of purposes.

* Reproduce the original path drawing on some other page.
* Use the lines, rectangles or curves of a path to locate table borders, help with text positioning or similar.
* Simply make lists e.g. of all lines or all rectangles on the page, potentially subselecting them by properties like fill color or location.

## How PDF Encodes its Paths
PDF uses a special mini-language for "painting" a page's appearance. Every PDF viewer, like Adobe Acrobat, must be able to interpret this language - and it indeed is "source code", which must be interpreted. A subset of commands of the language are used to paint paths. Please note, the unusual convention used by this language: function / command parameters **precede** the function! With some simplification, this works using the following:

* `"x y m"` **_opens_** a new path by positioning ("move") on point (x, y).
* `"x y l"` **_defines_** a line, ending at point (x, y). The start point of the line must either be the point defined by `"m"`, or is taken to be the end point of the preceeding command.
* `"x1 y1 x2 y2 x3 y3 c"` **_defines_** a (cubic) Bézier curve with two control points ((x1, y1) and (x2, y2)), which ends at point (x3, y3). Its start point must again either be defined by `"m"` or is taken to be the end point of the preceeding command. There are variants of `"c"`, called `"v"` and `"y"` respectively. They are the same thing except that they either duplicate the start point (`"v"`) or the end point (`"y"`) and use this copy as one of the two control points. So both are just abbreviated versions of `"c"`.
* `"x y w h re"` **_defines_** a rectangle. (x, y) is its lower-left point, w and h are its width and height. This command defines a **complete (sub) path** and does not require a preceeding `"m"` or other command. It therefore in most cases is the **_only command_** in a path. But it may be part of the command sequence of a higher level path, in which case (x, y) must be used as the connector.
* `"h"` (no parameters) **defines** a connection of the last point of the path with its first point using a straight line.

There are other commands which define stroke and fill color, line width and line dashing and other path property modifications.

All of these commands are definitions only - they do not **paint** or draw anything.

Several commands exist which actually **draw** the path. Each one of them also **closes** the path. The individual command names control how the drawing should happen: stroking or filling or both, handling of colors if the interiors of parts of the path overlap, etc.

> Circles and most other mathematical curves are **never represented with 100% precision in PDF**. Instead, approximations of them with Bézier curves are used - which in essence are polynomials of degree 3. This approach requires a piece-wise presentation. For example, circles are represented by 4 Bézier curves, each of which approximate a quarter circle perimeter - with amazing precision. For details on Bézier curves consult [this article](https://en.wikipedia.org/wiki/B%C3%A9zier_curve) for example. Quote: "TrueType fonts use composite Bézier curves composed of quadratic Bézier curves. Other languages and imaging tools (such as PostScript, Asymptote, Metafont, and SVG) use composite Béziers composed of cubic Bézier curves for drawing curved shapes. OpenType fonts can use either kind, depending on the flavor of the font."


For details on PDF operators see page 985 in the [manual](https://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/pdf_reference_1-7.pdf).

## Converting a PDF Path to Python

Module ``extractGraphic`` converts each PDF path to the following Python dictionary:

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
("l", p1, p2)  # line from p1 to p2 (fitz.Points). p1 is created
               # from either the "m" PDF command or a previous end point.
("c", p1, p2, p3, p4)  # Bezier curve from p1 to p4. p1 is created
               # from either the "m" PDF command or a previous end point.
               # PDF "v", "y" commands are converted to this format.
("re", rect)  # rectangle (fitz.Rect)
("qu", quad)  # created from "re" if current matrix is a rotation.
```

Multiple consecutive entries in ``items`` in a path indicate a compound drawing. They are **_"chained"_** together: in general, this implies that the **_last point_** of an entry **_must equal_** the first point of the following entry. The exceptions are rectangles and quads. They are complete sub-paths and drawn starting and ending at their **_top-left_** corner - so this point must be used for chaining where needed.

The programmer must take this into account when modifying a path.

> **Hint:** If encountering 4 consecutive connected Bezier curves "c", then they in many cases jointly define a **_circle_**, because circles need 4 Bézier curves which each form a quarter perimeter (see previous section). To confirm, check whether ``path["rect"]`` is a square.

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
>>> #--------------------------------------------
>>> # now extract the paths to see what happened
>>> #--------------------------------------------
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

To **reproduce** a path drawing, use code like this:

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
    shape.finish(  # end of drawings - output the path
        fill=path["fill"],
        color=path["stroke"],
        dashes=path["dashes"],
        even_odd=path["even_odd"],
        closePath=path["closePath"],
        lineJoin=path["lineJoin"],
        lineCap=path["lineCap"],
        width=path["width"],
    )
# all paths processed - commit them to the page
shape.commit(overlay=True)
```

This is a new utility. Although tested with dozens of PDF files ranging from elementary drawings to complex CAD-based files, it is still in its early stages. Errors must be expected like e.g. undetected drawings, or wrong coordinates reported.

In addition, there are **_known_** shortcomings with respect to the **_reproduction_** of drawings, which may be resolved in future versions:

* Drawing parameters controlled by separate graphics state dictionaries (see page 219 [here](https://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/pdf_reference_1-7.pdf)) are currently ignored. This most prominently pertains to opacity / transparency, but also to
* BlendMode, which controls drawing coloration given a certain background color.
* Shading is not supported.

## Example Use
### Create Lists of Lines, Rectangles, Quads
Line and rectangle definitions may be useful for detecting the location of tables.
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

