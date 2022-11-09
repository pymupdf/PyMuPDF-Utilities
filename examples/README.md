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

As a rule of thumb, subfolders are named `<action-object>` as if pointing out an action to be performed on an object, e.g. `attach-images`. Python scripts are then named `<action.py>`, e.g. `attach.py`. Thus, the `attach.py` script in the `attach-images` folder is meant to attach all images found in the `attach-images/input` directory. Input files and folders are provided to run the examples. The input files are distributed under [Creative Commons](https://creativecommons.org/licenses/) licenses while images are shared under the [Unsplash](https://unsplash.com/license) license. Output filenames are called `output`, e.g. `output.pdf`.

For further information on how a particular example is to be run please read the documentation section at the beginning of each script.

## Some Files in This Directory

File | Purpose
-----| -------
`csv2meta.py` | Load a PDF metadata dictionary from a CSV file's contents
`csv2toc.py` | Load a PDF TOC (table of contents) from a CSV file's contents
`embedded-copy.py` | Copies embedded files between source and target PDF
`embedded-export.py` | Exports an embedded file from a PDF
`embedded-import.py` | Embeds a new file into a PDF
`embedded-list.py` | Lists embedded file infos of a PDF
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
