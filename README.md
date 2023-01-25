# PyMuPDF-Utilities
This repository contains demos, examples and for using PyMuPDF in the respective folders.

> These scripts were written over an extended period of time - each for the then existing PyMuPDF version. I will not (reliably) go over each of them and ensure they still work. Occasionally a script may therefore no longer be compatible with the **current** version. If you find such inconsistencies, please **do not submit issues**, but try to repair the script and submit the corrections via a Pull Request instead. Thank you.

> Up to version 1.18.x of PyMupdf a major effort was undertaken to rename (almost) all methods and attributes to the **_snake_case_** standard. This task is now finished. For the time being and including versions 1.19.x, old and new names will coexist. For example, the old name `doc.newPage()` can be used as well as the new name `doc.new_page()` to create a new page. In versions 1.19.x, a deprecation warning will be issued when old method names are used. In versions thereafter, only the new names will remain being valid. To help migrating your scripts to new names, you may want to use ``alias-changer.py`` in this folder.

> If neither of this is an option for you, you can add a statement after `import fitz` that will add old camelCase names: `fitz.restore_aliases()`.

## OCR Support
Starting with version 1.19.0, PyMuPDF supports MuPDF's integrated Tesseract OCR features. Over time, we will add examples for using this.

There are nonetheless also other ways to use OCR tools in PyMuPDF scripts.

There are now two demo examples in the new folder [OCR](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/OCR) which use MuPDF OCR, Tesseract OCR and `easyocr` respectively.

To see more "interactive" demos of the new OCR features, please also have a look at the notebook collection in the [jupyter-notebooks](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/jupyter-notebooks) folder.

## Advanced TOC Handling
Handling of table of contents (TOC) has been significantly improved in v1.18.6. I have therefore created another new [folder](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/advanced-toc) dealing specifically with this subject.


## Font Replacement
New for PyMuPDF v1.17.6 is the ability to replace selected fonts in existing PDFs. This is a set of two scripts and their documentation in [this](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/font-replacement) folder.

## Image Replacement
[This](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/image-replacement) folder demonstrates the various options to **_replace_** or **_remove_** an image in a PDF.

## Marking Words and Lines
PyMuPDF's features have been extended in this respect. We therefore created this [own](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/word&line-marking) folder to contain dedicated scripts, descriptions and examples.

## Textbox Extraction
PyMuPDF's features have been extended in this respect. We therefore move example scripts and an extended description to its [own](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/textbox-extraction) folder.

## Text Extraction, Layout Preservation
Text extraction scripts have been moved into [this](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/text-extraction) separate folder. They demonstrate alternate ways extracting text from general documents (not only PDF), bargaining simplicity versus layout-faithful text output.

The most advanced script, [fitzcli.py](https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/text-extraction/fitzcli.py) produces text which closeley resembles the original layout of the document, including multi-column text, text thats surrounds images, etc.

## Jupyter Notebooks

A new [folder](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/jupyter-notebooks) with notebooks explaining basic concepts in an interactive way. Will be extended over time.

## Table Analysis

This folder contains a collection of scripts to analyse a table. The intention here, too, is to extend the examples over time.
Already there is a script which can extract table cells to a CSV file, if they are defined by gridlines. This includes any multi-line cell content.


## Examples

Please check out [this collection of examples](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/examples) for using PyMuPDF.

--------------------------------------------
If you find my work for PyMuPDF useful, you might consider a PayPal donation:

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=PE6665GMGMDEY&source=url)
