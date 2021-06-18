# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
A demo script to show how annotations can be added to a PDF using PyMuPDF.

It contains the following annotation types:
Caret, Text, FreeText, text markers (underline, strike-out, highlight,
squiggle), Circle, Square, Line, PolyLine, Polygon, FileAttachment, Stamp
and Redaction.

There is some effort to vary appearances by adding colors, line ends,
opacity, rotation, dashed lines, etc.

Using class TextWriter
----------------------
The script is a functional equivalent of "new-annots.py". Instead of the old
method of inserting text it uses the new PyMuPDF class TextWriter.
Using this feature, the rectangle of written text can be **calculated**,
which obsoletes the search for text for determining its rectangle.

Dependencies
------------
PyMuPDF v1.17.0
-------------------------------------------------------------------------------
"""
from __future__ import print_function

import os
import sys

import fitz

print(fitz.__doc__)

highlight = "this text is highlighted"
underline = "this text is underlined"
strikeout = "this text is striked out"
squiggled = "this text is zigzag-underlined"
red = (1, 0, 0)
blue = (0, 0, 1)
gold = (1, 1, 0)
green = (0, 1, 0)

displ = fitz.Rect(0, 50, 0, 50)
r = fitz.Rect(72, 72, 220, 100)
t1 = u"têxt üsès Lätiñ charß,\nEUR: €, mu: µ, super scripts: ²³!"

font = fitz.Font("helv")  # used by the TextWriter class

doc = fitz.open()
page = doc.new_page()

page.set_rotation(0)

# following makes sure that TextWriter references the **unrotated** page rect
# as everything else does ...
page_rect = page.rect * page.derotation_matrix


def print_descr(annot):
    """Print a short description to the right of the annot rect."""
    rect = annot.rect
    page = annot.parent
    writer = fitz.TextWriter(page_rect, color=red)
    writer.append(rect.br + (10, -5), "%s annotation" % annot.type[1], font=font)
    writer.write_text(page)


annot = page.add_caret_annot(r.tl)
print_descr(annot)

r = r + displ
annot = page.add_freetext_annot(
    r,
    t1,
    fontsize=10,
    rotate=90,
    text_color=blue,
    fill_color=gold,
    align=fitz.TEXT_ALIGN_CENTER,
)
annot.set_border(width=0.3, dashes=[2])
annot.update(text_color=blue, fill_color=gold)

print_descr(annot)
r = annot.rect + displ

annot = page.add_text_annot(r.tl, t1)
print_descr(annot)

# Adding text marker annotations: For each annotation type, first insert a
# a (unique) text and tilt it a bit. Then calculate the quad of the text
# and feed it into annot creation.
pos = annot.rect.tl + displ.tl
mat = fitz.Matrix(-15)

writer = fitz.TextWriter(page_rect)  # create TextWriter object
writer.append(pos, highlight, font=font)  # append text
writer.write_text(page, morph=(pos, mat))  # write to the page with rotation
writer.text_rect.x0 = pos.x  # use actual text start / end
writer.text_rect.x1 = writer.last_point.x
quad_highlight = writer.text_rect.morph(pos, ~mat)  # calculate text quad
pos = quad_highlight.rect.bl  # the next writing position

writer = fitz.TextWriter(page_rect)
writer.append(pos, underline, font=font)
writer.write_text(page, morph=(pos, mat))
writer.text_rect.x0 = pos.x
writer.text_rect.x1 = writer.last_point.x
quad_underline = writer.text_rect.morph(pos, ~mat)
pos = quad_underline.rect.bl

writer = fitz.TextWriter(page_rect)
writer.append(pos, strikeout, font=font)
writer.write_text(page, morph=(pos, mat))
writer.text_rect.x0 = pos.x
writer.text_rect.x1 = writer.last_point.x
quad_strikeout = writer.text_rect.morph(pos, ~mat)
pos = quad_strikeout.rect.bl

writer = fitz.TextWriter(page_rect)
writer.append(pos, squiggled, font=font)
writer.write_text(page, morph=(pos, mat))
writer.text_rect.x0 = pos.x
writer.text_rect.x1 = writer.last_point.x
quad_squiggled = writer.text_rect.morph(pos, ~mat)
pos = quad_squiggled.rect.bl

# we now add the four text marker annots
annot = page.add_highlight_annot(quad_highlight)
print_descr(annot)

annot = page.add_underline_annot(quad_underline)
print_descr(annot)

annot = page.add_strikeout_annot(quad_strikeout)
print_descr(annot)

annot = page.add_squiggly_annot(quad_squiggled)
print_descr(annot)

# calculate rect for the next annot
r = fitz.Rect(pos, pos.x + 75, pos.y + 35) + (0, 20, 0, 20)

annot = page.add_polyline_annot([r.bl, r.tr, r.br, r.tl])  # 'Polyline'
annot.set_border(width=0.3, dashes=[2])
annot.set_colors(stroke=blue, fill=green)
annot.set_line_ends(fitz.PDF_ANNOT_LE_CLOSED_ARROW, fitz.PDF_ANNOT_LE_R_CLOSED_ARROW)
annot.update(fill_color=(1, 1, 0))
print_descr(annot)
r += displ

annot = page.add_polygon_annot([r.bl, r.tr, r.br, r.tl])  # 'Polygon'
annot.set_border(width=0.3, dashes=[2])
annot.set_colors(stroke=blue, fill=gold)
annot.set_line_ends(fitz.PDF_ANNOT_LE_DIAMOND, fitz.PDF_ANNOT_LE_CIRCLE)
annot.update()
print_descr(annot)
r += displ

annot = page.add_line_annot(r.tr, r.bl)  # 'Line'
annot.set_border(width=0.3, dashes=[2])
annot.set_colors(stroke=blue, fill=gold)
annot.set_line_ends(fitz.PDF_ANNOT_LE_DIAMOND, fitz.PDF_ANNOT_LE_CIRCLE)
annot.update()
print_descr(annot)
r += displ

annot = page.add_rect_annot(r)  # 'Square'
annot.set_border(width=1, dashes=[1, 2])
annot.set_colors(stroke=blue, fill=gold)
annot.update(opacity=0.5)
print_descr(annot)
r += displ

annot = page.add_circle_annot(r)  # 'Circle'
annot.set_border(width=0.3, dashes=[2])
annot.set_colors(stroke=blue, fill=gold)
annot.update()
print_descr(annot)
r += displ

annot = page.add_file_annot(
    r.tl, b"just anything for testing", "testdata.txt"  # 'FileAttachment'
)
print_descr(annot)  # annot.rect
r += displ

annot = page.add_stamp_annot(r, stamp=10)  # 'Stamp'
annot.set_colors(stroke=green)
annot.update()
print_descr(annot)
r += displ + (0, 0, 50, 15)

writer = fitz.TextWriter(page_rect, color=blue)
writer.fill_textbox(
    r,
    "This content will be removed upon applying the redaction.",
    font=font,
    fontsize=11,
    align=fitz.TEXT_ALIGN_CENTER,
)
writer.write_text(page)
annot = page.add_redact_annot(r)
print_descr(annot)

outpdf = os.path.abspath(__file__).replace(".py", "-%i.pdf" % page.rotation)
doc.ez_save(outpdf)
