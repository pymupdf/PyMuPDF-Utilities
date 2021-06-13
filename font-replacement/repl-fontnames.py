# -*- coding: utf-8 -*-
"""
@created: 2020-08-20 13:00:00

@author: Jorj X. McKie

Font Replacement
----------------
This is one of two scripts which allow replacement of specific fonts in a PDF.
It scans through the pages and creates a condensed list of the used fonts, which
its writes to a JSON file.

This file must be edited in order to select the fonts to be exchanged.
After these changes, script 'repl-font.py' may be invoked which reads the PDF
and this JSON file to actually perform the font exchange.

For a given PDF file 'input.pdf' the JSON file 'input.pdf-fontnames.json' is
created. which you must edit. It is a list of one dictionary per font, like

{"oldfont": ["fontname1", ...], "newfont": "keep", "info": "..."}

Where 'oldfont' is a list of fontname aliases of a used font, 'keep'
specifies the default action (do not replace this font), and 'info' contains
some font information to facilitate the replacement decision.
Either replace the 'keep' keyword with a new fontname or just leave it as is.

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
    """Replace hex parts of the fontname."""
    while "#" in name:  # any hexadecimals in the name?
        p = name.find("#")
        c = int(name[p + 1 : p + 3], 16)
        name = name.replace(name[p : p + 3], chr(c))
    if name.find("+") == 6:  # only if '+' at position 5
        return True, name[7:]
    return False, name


def get_fontnames(doc, item):
    """Return a list of fontnames for an item of 'page.get_fonts()'.

    There may be more than one alternative e.g. for Type0 fonts.
    """
    fontname = item[3]
    subset, fontname = norm_name(fontname)
    names = [fontname]
    xref = item[0]
    text = doc.xref_object(item[0])
    font = ""
    descendents = ""
    t, temp = doc.xref_get_key(xref, "BaseFont")
    if t == "name":
        _, font = norm_name(temp[1:])
        names.append(font)
    t, temp = doc.xref_get_key(xref, "DescendantFonts")
    if t != "array":  # no DescendantFonts - done
        return subset, tuple(set(names))
    temp = temp[1:-1]  # remove array brackets

    # DescendantFonts is either one xref or one embedded PDF dictionary
    if temp.endswith(">>"):  # embedded dictionary!
        temp_list = temp.split("/")  # split at name separator
        try:
            p0 = temp_list.index("BaseFont")
        except:  # no fontname provided - done
            return subset, tuple(set(names))
        p0 += 1  # next item is the fontname
        font = temp_list[p0]
        _, font = norm_name(font)
        names.append(font)
        return subset, tuple(set(names))
    # DescendantFonts given as xref
    nxref = int(temp.replace("0 R", ""))  # get xref of DescendantFonts
    t, temp = doc.xref_get_key(nxref, "BaseFont")
    if t == "name":  # fontname, append it
        _, font = norm_name(temp[1:])
        names.append(font)
    return subset, tuple(set(names))


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
    for f in doc.get_page_fonts(i, full=True):
        msg = ""
        subset, fontname = get_fontnames(doc, f)

        if f[1] == "n/a":
            msg = "Not embedded!"
        else:
            extr = doc.extract_font(f[0])
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
