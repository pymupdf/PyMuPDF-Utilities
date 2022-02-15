This directory contains example programs for using PyMuPDF.

The scope of these examples should clearly exceed the category "demo".
Instead it should contain complete, working programs, or at least snippets of working code.

Licensing:
===========
See the COPYING file.

Disclaimer
===========
These are quite a number of examples by now. Many of them have originated in early times of the package. Therefore discrepancies may have occurred with any API changes implemented over time. We we will not scan through these scripts for every release, so please regard them as what they are intended for: **examples** which should give you a start - there is no guaranty that everything here works unchanged for all times.

If you find an issue, please fix it and submit a PR, and we will gladly incorporate it.


Some Files in this Directory
==============================

======================= ===========================================================================================
File                    Purpose
======================= ===========================================================================================
4-up.py                 Combines 4 PDF input pages to 1 output PDF page
cal-maker.py            creates a PDF with 3-year calendars
colordbHSV.py           like colordbRGB.py but in sort order "Hue, Saturation, Value"
colordbRGB.py           creates a PDF showing all available color database colors
csv2meta.py             load a PDF metadata dictionary from a CSV file's contents
csv2toc.py              load a PDF TOC (table of contents) from a CSV file's contents
embedded-copy.py        copies embedded files between source and target PDF
embedded-export.py      exports an emdedded file from a PDF
embedded-import.py      embeds a new file into a PDF
embedded-list.py        lists emdedded file infos of a PDF
extract-imga.py         extract images of a page to separate files
extract-imgb.py         extract images of a PDF to separate files
image-maintenance.py    GUI to modify images in an existing PDF (new with v1.17.5)
meta2csv.py             export a document metadata dictionary to a CSV file
PageFormat.py           function returns a page's paper format
ParseTab.py             a function to parse tables within documents
PDF2Text.py             a program to extract all text of a PDF `moved to PyMuPDF-Utilities/text-extraction <https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/text-extraction>`_
PDF2TextJS.py           a program to extract all text of a PDF preserving normal reading sequence `moved to PyMuPDF-Utilities/text-extraction <https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/text-extraction>`_
PDFjoiner.py            a full-featured program to join PDF files
PDFoptimizer.py         a wrapper for FileOptimizer - see WIKI page
PDFoutline.py           a program to edit a PDF's table of contents
PDFoutlineHelp.html     help for PDFoutline.py
posterize.py            Splits up input PDF pages
TableExtract.py         example CLI program using ParseTab
toc2csv.py              export a document TOC (Table of contents) to a CSV file
wxTableExtract.py       full-featured GUI using ParseTab. Supports automatic and manual column definitions
======================= ===========================================================================================
