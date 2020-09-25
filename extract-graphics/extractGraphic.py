"""
@created: 2020-09-22 20:00:00

@author: (c) Jorj X. McKie

@license: GNU GPL 3.0 or later

Extraction of draw commands in a PDF page
-----------------------------------------
This module is called with a PDF page and returns a list of "path" dicts.
Each path contains a number of path-wide properies like line width or
dashing, and a list of draw commands.
There are only 3 relevant draw commands occurring in a PDF page. All other
draw shapes like circles, triangles, ... are composed by these atomic draws.

- "l" draw a line
- "c" draw a Bezier curve
- "re" draw a rectangle

Each item of the draw command list looks like one of the following:

("l", p1, p2) - with two fitz.Point objects
("re", rect) - with a fitz.Rect
("qu", quad) - with a fitz.Quad, generated for rotated rectangles
("c", p1, p2, p3, p4) - with four fitz.Point objects

The original drawings can be reproduced by using the PyMuPDF Shape class and
its methods "drawLine(p1, p2)", "drawRect(rect)", "drawQuad(quad)" and
"drawBezier(p1, p2, p3, p4)".
After drawing all the the list items like this, a "Shape.finish()" must be
executed using the remaining values of the path.

"""
import fitz


def extractGraphic(page):
    """Extract geometry objects from a /Contents.

    Args:
        page: a PDF page
    Returns:
        List of paths in the contents. 
    """
    gs_list = []  # list for stacking graphic states
    path_list = []  # return this list
    ignored_commands = (  # ignore these PDF commands
        b"'",
        b'"',
        b"BDC",
        b"BMC",
        b"BX",
        b"CS",
        b"cs",
        b"d0",
        b"d1",
        b"Do",
        b"DP",
        b"EMC",
        b"EX",
        b"gs",
        b"i",
        b"ID",
        b"M",
        b"MP",
        b"ri",
        b"sh",
        b"T*",
        b"Tc",
        b"Td",
        b"TD",
        b"Tf",
        b"Tj",
        b"TJ",
        b"TL",
        b"Tm",
        b"Tr",
        b"Ts",
        b"Tw",
        b"Tz",
        b"W",
        b"W*",
    )

    def copy_gs(curr_gs, curr_path):
        curr_path["width"] = curr_gs["width"]
        curr_path["lineJoin"] = curr_gs["lineJoin"]
        curr_path["lineCap"] = curr_gs["lineCap"]
        curr_path["dashes"] = curr_gs["dashes"]
        curr_path["stroke"] = curr_gs["stroke"]
        curr_path["fill"] = curr_gs["fill"]

    def new_path():
        return {
            "stroke": None,
            "fill": None,
            "width": None,
            "lineJoin": 0,
            "lineCap": 0,
            "dashes": "",
            "closePath": False,
            "even_odd": False,
            "rect": fitz.Rect(),
            "items": [],
        }

    def new_gs():
        return {
            "ctm": fitz.Matrix(1, 1),
            "stroke": None,
            "fill": None,
            "width": 0,
            "lineJoin": 0,
            "lineCap": 0,
            "dashes": "",
        }

    def get_floats(line, l, count):
        """Extract the floats from a command.

        Args:
            line: command line
            l: length of command
            count: acceptable number of floats
        """
        t = list(map(float, line[:-l].split()))
        if count and len(t) != count:
            raise ValueError("bad command", line.decode())
        return t

    page.cleanContents()
    cont = bytearray(page.readContents())
    ctm = page.transformationMatrix
    i1 = 0
    while i1 >= 0:  # remove any text objects
        i1 = cont.find(b"BT\n")
        if i1 < 0:
            break
        i2 = cont.find(b"ET\n", i1)
        if i2 < 0:
            break
        cont[i1 : i2 + 2] = b""
    i1 = 0
    while i1 >= 0:  # remove any inline images
        i1 = cont.find(b"BI\n")
        if i1 < 0:
            break
        i2 = cont.find(b"EI\n", i1)
        if i2 < 0:
            break
        cont[i1 : i2 + 2] = b""

    lines = cont.splitlines()
    curr_gs = new_gs()
    curr_path = new_path()
    current = None
    for line in lines:
        if line.endswith(ignored_commands):
            continue
        if line == b"":
            continue

        if line == b"q":
            gs_list.append(curr_gs)
            curr_gs = new_gs()

        elif line == b"Q":
            curr_gs = gs_list.pop(-1)

        elif line.endswith(b"n"):
            curr_path = new_path()

        elif line.endswith(b"cm"):
            m = fitz.Matrix(get_floats(line, 2, 6))
            curr_gs["ctm"] *= m

        elif line.endswith(b"m"):
            t = get_floats(line, 1, 2)
            current = fitz.Point(t) * curr_gs["ctm"] * ctm

        elif line.endswith(b"l"):
            t = get_floats(line, 1, 2)
            p = fitz.Point(t) * curr_gs["ctm"] * ctm
            curr_path["items"].append(("l", current, p))
            curr_path["rect"] |= fitz.Rect(current, p).normalize()
            current = p

        elif line.endswith(b"c"):
            x1, y1, x2, y2, x3, y3 = get_floats(line, 1, 6)
            p1 = fitz.Point(x1, y1) * curr_gs["ctm"] * ctm
            p2 = fitz.Point(x2, y2) * curr_gs["ctm"] * ctm
            p3 = fitz.Point(x3, y3) * curr_gs["ctm"] * ctm
            curr_path["items"].append(("c", current, p1, p2, p3))
            r = fitz.Rect(current, current)
            r |= p1
            r |= p2
            r |= p3
            curr_path["rect"] |= r
            current = p3

        elif line.endswith(b"v"):
            x2, y2, x3, y3 = get_floats(line, 1, 4)
            p2 = fitz.Point(x2, y2) * curr_gs["ctm"] * ctm
            p3 = fitz.Point(x3, y3) * curr_gs["ctm"] * ctm
            curr_path["items"].append(("c", current, current, p2, p3))
            r = fitz.Rect(current, current)
            r |= p2
            r |= p3
            curr_path["rect"] |= r
            current = p3

        elif line.endswith(b"y"):
            x1, y1, x3, y3 = get_floats(line, 1, 4)
            p1 = fitz.Point(x1, y1) * curr_gs["ctm"] * ctm
            p3 = fitz.Point(x3, y3) * curr_gs["ctm"] * ctm
            curr_path["items"].append(("c", current, p1, p3, p3))
            r = fitz.Rect(current, current)
            r |= p1
            r |= p3
            curr_path["rect"] |= r
            current = p3

        elif line.endswith(b"re"):
            # either accept rectangle, or make a quad if current
            # matrix is not rectilinear
            x0, y0, w, h = get_floats(line, 2, 4)
            r = fitz.Rect(x0, y0, x0 + w, y0 + h)
            if curr_gs["ctm"].isRectilinear:
                r *= curr_gs["ctm"] * ctm
                curr_path["items"].append(("re", r))
                curr_path["rect"] |= r
                current = r.tl
            else:
                r = (r.quad) * curr_gs["ctm"] * ctm
                curr_path["items"].append(("qu", r))
                curr_path["rect"] |= r.rect
                current = r.ul

        elif line.endswith(b"j"):
            curr_gs["lineJoin"] = int(line[:-1])

        elif line.endswith(b"J"):
            curr_gs["lineCap"] = int(line[:-1])

        elif line.endswith(b"w"):
            curr_gs["width"] = get_floats(line, 1, 1)[0]

        elif line.endswith(b"d"):
            curr_gs["dashes"] = line[:-1].strip().decode()

        elif line.endswith((b"g", b"rg", b"k", b"sc")):
            curr_gs["fill"] = get_floats(line, 2, 0)

        elif line.endswith(b"scn"):
            curr_gs["fill"] = get_floats(line, 3, 0)

        elif line.endswith(b"SCN"):
            curr_gs["stroke"] = get_floats(line, 3, 0)

        elif line.endswith((b"G", b"RG", b"K", b"SC")):
            curr_gs["stroke"] = get_floats(line, 2, 0)

        elif line == b"h":
            curr_path["closePath"] = True

        elif line in (b"b", b"B", b"b*", b"B*"):
            if line in (b"b", b"b*"):
                curr_path["closePath"] = True
            if line in (b"b*", b"B*"):
                curr_path["even_odd"] = True
            else:
                curr_path["even_odd"] = False
            copy_gs(curr_gs, curr_path)
            path_list.append(curr_path)
            curr_path = new_path()

        elif line in (b"f", b"F", b"f*"):  # fill, no stroke
            if line == b"f*":
                curr_path["even_odd"] = True
            else:
                curr_path["even_odd"] = False
            copy_gs(curr_gs, curr_path)
            curr_path["stroke"] = None
            path_list.append(curr_path)
            curr_path = new_path()

        elif line in (b"s", b"S"):  # stroke, no fill
            copy_gs(curr_gs, curr_path)
            curr_path["fill"] = None
            path_list.append(curr_path)
            curr_path = new_path()

        else:
            print("Unhandled command: '%s'." % line.decode())

    return path_list
