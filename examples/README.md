# PyMuPDF Examples

This directory contains example programs for using PyMuPDF.

The scope of these examples should clearly exceed the category "demo". Instead it should contain complete, working programs, or at least snippets of working code.

## Licensing

See the COPYING file.

## Disclaimer

These are quite a number of examples by now. Many of them have originated in early times of the package. Therefore discrepancies may have occurred with any API changes implemented over time. We we will not scan through these scripts for every release, so please regard them as what they are intended for: **examples** which should give you a start - there is no guaranty that everything here works unchanged for all times.

If you find an issue, please fix it and submit a PR, and we will gladly incorporate it.

## Conventions

At the moment the `examples` folder is being restructured by using a self-explanatory naming convention.

Subfolders are named `<verb-object>`. The Python scripts are named `verb.py`. Input files and folders are provided in order to run the examples. Document files are distributed under [Creative Commons](https://creativecommons.org/licenses/) licenses while images are shared under the [Unsplash](https://unsplash.com/license) license.

For further information please read the documentation section at the beginning of each script.

## Some Files in This Directory

File | Purpose
-----| -------
`colordbHSV.py` | Like `colordbRGB.py` but in sort order "Hue, Saturation, Value"
`colordbRGB.py` | Creates a PDF showing all available color database colors
`csv2meta.py` | Load a PDF metadata dictionary from a CSV file's contents
`csv2toc.py` | Load a PDF TOC (table of contents) from a CSV file's contents
`embedded-copy.py` | Copies embedded files between source and target PDF
`embedded-export.py` | Exports an embedded file from a PDF
`embedded-import.py` | Embeds a new file into a PDF
`embedded-list.py` | Lists embedded file infos of a PDF
`extract-imga.py` | Extract images of a page to separate files
`extract-imgb.py` | Extract images of a PDF to separate files
`image-maintenance.py` | GUI to modify images in an existing PDF (new with v1.17.5)
`ParseTab.py` | A function to parse tables within documents
`PDF2Text.py` | A program to extract all text of a PDF moved to [PyMuPDF-Utilities/text-extraction](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/text-extraction)
`PDF2TextJS.py` | A program to extract all text of a PDF preserving normal reading sequence moved to [PyMuPDF-Utilities/text-extraction](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/text-extraction)
`PDFjoiner.py` | A full-featured program to join PDF files
`PDFoptimizer.py` | A wrapper for FileOptimizer - see WIKI page
`PDFoutline.py` | A program to edit a PDF's table of contents
`PDFoutlineHelp.html` | Help for PDFoutline.py
`posterize.py` | Splits up input PDF pages
`TableExtract.py` | Example CLI program using ParseTab
`toc2csv.py` | Export a document TOC (Table of contents) to a CSV file
`wxTableExtract.py` | Full-featured GUI using ParseTab. Supports automatic and manual column definitions
