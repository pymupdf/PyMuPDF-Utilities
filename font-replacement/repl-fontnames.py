# -*- coding: utf-8 -*-
"""
@created: 2020-08-20 13:00:00

@author: Jorj X. McKie

Font Replacement
----------------
This is one of two scripts which allow replacement of specific fonts in a PDF.
It scans through the pages and creates a condensed list of the used fonts, which
its writes to a CSV file.

This file must be edited in order to select the fonts to be exchanged.
After these changes, script 'repl-font.py' may be invoked which reads the PDF
and this CSV file to actually perform the font exchange.

For a given PDF files 'input.pdf' the CSV file 'input.pdf-fontnames.csv' is
created. Its entries are:

oldfont;"keep";comments

Where 'oldfont' is an existing fontname, 'keep' specifies the default action
(do not replace this font), and 'comment' contains a number of font information
to facilitate any replacement decision.
The editor of the file is expected to replace the 'keep' keyword with a new font
name or just leave it untouched.

Dependencies
------------
PyMuPDF v1.18.4

License
-------
GNU GPL 3.x (this script)
GNU AFFERO GPL 3.0 (MuPDF components)
MIT license (fontTools)

Copyright
---------
(c) 2020 Jorj X. McKie

Changes
-------
* Version 2020-09-02:
- Now also supporting text in so-called "Form XObjects", i.e. text not encoded
  in the page's /Contents.
- The intermediate CSV file containing mappings between old and new font names
  is now handled as a binary file (read / write options "rb", resp. "wb") to
  support fontnames encoded as general UTF-8.

* Version 2020-09-10:
- Change the CSV parameter file to JSON format. This hopefully covers more
  peculiarities for fontname specifications.

* Version 2020-11-27:
- The fontname to replace ("old" fontname) is now a list to account for
  potentially different name variants in the various entangled PDF objects
  like /FontName, /BaseName, etc.
"""
import fitz
import sys
import json


def norm_name(name):
    while "#" in name:
        p = name.find("#")
        c = int(name[p + 1 : p + 3], 16)
        name = name.replace(name[p : p + 3], chr(c))
    p = name.find("+") + 1
    return name[p:]


def get_fontnames(doc, item):
    """Return a list of fontnames.

    There may be more than one alternative e.g. for Type0 fonts.
    """
    subset = False
    fontname = item[3]
    idx = fontname.find("+") + 1
    fontname = fontname[idx:]
    if idx > 0:
        subset = True
    names = [fontname]
    text = doc.xref_object(item[0])
    font = ""
    descendents = ""

    for line in text.splitlines():
        line = line.split()
        if line[0] == "/BaseFont":
            font = norm_name(line[1][1:])
        elif line[0] == "/DescendantFonts":
            descendents = " ".join(line[1:]).replace(" 0 R", " ")
            if descendents.startswith("["):
                descendents = descendents[1:-1]
            descendents = map(int, descendents.split())

    if font and font not in names:
        names.append(font)
    if not descendents:
        return subset, tuple(names)

    # 'descendents' is a list of descendent font xrefs.
    # Should be just one by the books.
    for xref in descendents:
        for line in doc.xref_object(xref).splitlines():
            line = line.split()
            if line[0] == "/BaseFont":
                font = norm_name(line[1][1:])
                if font not in names:
                    names.append(font)
    return subset, tuple(names)


def make_msg(font):
    flags = font.flags
    msg = ["%i glyphs" % font.glyph_count, "size %i" % len(font.buffer)]
    if flags["mono"] == 1:
        msg.append("mono")
    if flags["serif"]:
        msg.append("serifed")
    if flags["italic"]:
        msg.append("italic")
    if flags["bold"]:
        msg.append("bold")
    msg = ", ".join(msg)
    return msg


infilename = sys.argv[1]
font_list = set()
doc = fitz.open(infilename)
for i in range(len(doc)):
    for f in doc.getPageFontList(i, full=True):
        msg = ""
        subset, fontname = get_fontnames(doc, f)

        if f[1] == "n/a":
            msg = "Not embedded!"
        else:
            extr = doc.extractFont(f[0])
            font = fitz.Font(fontbuffer=extr[-1])
            msg = make_msg(font)

        if subset:
            msg += ", subset font"
        font_list.add((fontname, msg))

font_list = list(font_list)
font_list.sort(key=lambda x: x[0])
outname = infilename + "-fontnames.json"
out = open(outname, "w")
outlist = []
for fontname, msg in font_list:
    msg1 = "keep"
    outlist.append({"oldfont": fontname, "newfont": msg1, "info": msg})

json.dump(outlist, out, indent=2)
out.close()
