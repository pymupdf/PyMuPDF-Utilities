#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Sun June 11 16:00:00 2017

@author: Jorj McKie
Copyright (c) 2017-2020 Jorj X. McKie

The license of this program is governed by the GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007 or later.

Demo program for the Python binding PyMuPDF of MuPDF.

Dependencies:
-------------
* PyMuPDF v1.17.4
* calendar (either use LocaleTextCalendar or just TextCalendar)

This program creates calendars for three years in a row (starting with
the one given as parameter) and stores the result in a PDF.
"""
import fitz
import calendar
import sys

if not fitz.VersionBind.split(".") >= ["1", "17", "4"]:
    raise ValueError("Need PyMuPDF v.1.17.4 at least.")
if len(sys.argv) != 2:
    startyear = fitz.get_pdf_now()[2:6]  # take current year
else:
    startyear = sys.argv[1]

if len(startyear) != 4 or not startyear.isnumeric():
    raise ValueError("Start year must be 4 digits")

suffix = "-%s.pdf" % startyear
outfile = __file__.replace(".py", suffix)
startyear = int(startyear)

doc = fitz.open()  # new empty PDF
# font = fitz.Font("cour")  # use the built-in font Courier
font = fitz.Font("spacemo")  # use Space Mono - a nicer mono-spaced font
cal = calendar.LocaleTextCalendar(locale="de")  # use your locale
# cal = calendar.TextCalendar()  # or stick with English


page_rect = fitz.paper_rect("a4-l")  # A4 landscape paper
w = page_rect.width
h = page_rect.height
print_rect = page_rect + (36, 72, -36, -36)  # fill this rectangle

# one line in calendar output is at most 98 characters, so we calculate
# the maximum possible fontsize cum grano salis as:
char_width = font.glyph_advance(32)  # character width of the font
fontsize = print_rect.width / (char_width * 100)


def page_out(doc, text):
    page = doc.new_page(width=w, height=h)  # make new page
    tw = fitz.TextWriter(page_rect)  # make text writer
    tw.fill_textbox(print_rect, text, font=font, fontsize=fontsize)
    tw.write_text(page)  # write the text to the page


for i in range(3):  # make calendar for 3 years
    text = cal.formatyear(startyear + i, m=4)
    page_out(doc, text)


doc.save(outfile, garbage=4, deflate=True, pretty=True)

