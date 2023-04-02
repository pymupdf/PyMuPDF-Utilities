# PyMuPDF-Utilities
This repository contains demos and examples to help you create PDF, XPS, and eBook applications with PyMuPDF.

## Disclaimer

Some examples were initially created in the early days of the package. API changes implemented over time may have caused discrepancies in the scripts. We may not update them every time an update is released, so there's no guarantee they all will work as originally expected. If you look at the scripts as what they are intended to be, examples, then they will give you a good start.

Up to PyMupdf 1.18.x, methods and attributes have been renamed according to the snake-case standard. For the time being including versions 1.19.x, old and new names will coexist. For example, `doc.newPage()` can be used as well as `doc.new_page()` to create a new page.

> In versions 1.19.x, a deprecation warning is issued if camel-case names are used. In newest versions only snake-case names are valid. You may want to use the `alias-changer.py` script in this folder to keep your code up-to-date. Alternatively, use `fitz.restore_aliases()`.

## OCR Support
Starting with version 1.19.0, PyMuPDF supports MuPDF's integrated Tesseract OCR features. Over time, we will add examples for using this.

There are nonetheless also other ways to use OCR tools in PyMuPDF scripts.

There are now two demo examples in the new folder [OCR](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/OCR) which use MuPDF OCR, Tesseract OCR and `easyocr` respectively.

To see more "interactive" demos of the new OCR features, please also have a look at the notebook collection in the [jupyter-notebooks](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/jupyter-notebooks) folder.

## Advanced TOC Handling
Handling of table of contents (TOC) has been significantly improved in v1.18.6. I have therefore created another new [folder](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/advanced-toc) dealing specifically with this subject.


## Font Replacement
New for PyMuPDF v1.17.6 is the ability to replace selected fonts in existing PDFs. This is a set of two scripts and their documentation in [this](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/font-replacement) folder.

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
Already there is a script which can extract table cells to a pandas DataFrame (saved to EXCEL), if they are defined by gridlines. This includes any multi-line cell content.


## Examples

Please check out [the examples](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/examples).