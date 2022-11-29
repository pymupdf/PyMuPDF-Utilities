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

## Examples
From the [examples](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/examples) folder, here is a synopsis of some scripts that you may find interesting.

* **image-maintenance.py** a really cool GUI script (wxPython) which allows insertion, deletion and modification of images on PDF pages in a visually controlled mode. Requires v1.17.5 and a Phoenix version of wxPython.
* **morph-demo1.py, morph-demo2.py, morph-demo3.py** are scripts showing the effect of the ``morph`` parameter in text insertions. Each script creates a PDF page, fills a  text box and then morphs that box using its upper left corner as fixed point. Each morphing result is put on a new PDF page and the resulting pixmap is shown in an endless loop. Now require PyMuPDF v1.14.5 and can be run with Python v2.7.

* **quad-show1.py, quad-show2.py** require PyMuPDF v1.14.5 and can be run with Python v2.7. They demonstrate how the modified version of `drawOval` can be used to create a wide range of shapes, both displaying the results in an endless loop.

* **all-my-pics-attached.py** - take all files from a given directory and **attach** them to pages (as *'FileAttachment'* annotations) of a new PDF. Non-file entries of the directory will be skipped.

* **all-my-pics-embedded.py** - take all files from a given directory and **embed** them (as *'EmbeddedFile'* entries) in a new PDF. Non-file entries of the directory will be skipped.

* **all-my-pics-inserted.py** - take all _**image**_ (only) files from a given directory and **insert** them as pages in a new PDF (actually inserts the **first page** of any supported non-PDF document). Non-file entries of the directory will be skipped.

* **anonymize.py** - scan through a PDF and remove all text of all pages. Also erase metadata / XML metadata. This works by eliminating everything enclosed by the string pairs "BT" and "ET" in the pages' `/Contents` object(s). Text appearing in images cannot be removed with this script -- this includes images made by the PDF operator syntax: some utilities synthesize text on the basis of elementary drawing commands, i.e. every single letter is created by drawing rectangles, lines and curves. This is probably done as a way to enforce copyright protection. In these cases, the script will not work either.

* **extract-imga.py** - **(requires v1.13.17)** extract images from a PDF looping through its pages. It takes care of images with a transparency ("stencil") mask and also tries to identify and skip "irrelevant" images. Suppresses extracting the same image multiple times. You may also want to look at ``extract-imgb.py`` below.

* **extract-imgb.py** - **(requires v1.13.17)** extract all images from a PDF looping through its cross references numbers. Ignores the page tree and generally seeks to be as robust as possible with respect to damaged PDFs. Otherwise similar to the previous script in ignoring irrelevant images and working with stencil masks.

* **DeDRM-ebook.py** - repeatedly copies a fixed screen area to a PDF page. Can be used to page through an e-book (which might be DRM protected ...) and create a PDF consisting of all its pages in image format - very much like making a full book photo copy. You would start an e-book reader to read a book and then trigger this skript to page through the displayed book making images page by page.

* **doc-browser.py** - a complete GUI document displaying script using **Tkinter**! It features a zooming facility and can display all document types supported by MuPDF (i.e. **not just PDFs!**). It requires [PySimpleGUI](https://pypi.org/project/PySimpleGUI/), an awesome pure Python package exclusively based on Tkinter. For response time improvements, we are also using [Pillow](https://pypi.org/project/Pillow/).

* **layout-analyzer.py** - create an output PDF for a given PDF with text and graphics layout analysis. Each text and graphics block is surrounded by a rectangle (only metadata is shown, no image content). Output PDF has page dimensions of the input's `/MediaBox`. The input's `/CropBox` is indicated by a gray background rectangle - see example files in this repo: demo1.pdf and layout-demo1.pdf in folder `text-extraction`.

* **clean-cont.py** - **(requires v1.13.5)** Inspect PDF pages whether any have multiple /Contents objects. If not, exit immediately. If **yes**, check if any contents are shared between pages. If **yes**, save the document using the "clean" option and exit. If **not,**  join multiple page contents into one and save with option "garbage=3" (which removes now unused objects).

* **form-fields.py** demo script: create a PDF with form fields.

* **shapes_and_symbols.py** contains ca. 10 predefined symbols, which can be imported and used in PDF page creation. If invoked standalone, a PDF is created with one page per each of the symbols.

* **symbol-list.py** creates a list of symbols and their descriptions, which are implemented in **shapes_and_symbols.py** -- thus also demonstrating how to use this module.

* **sierpinski-fitz.py** demonstrates the use of ``Pixmaps`` be creating Sierpinski's carpet (a fractal).

* **sierpinski-punch.py** does the same thing, but this time uses a more intuitive recursive function.

* the **animations** folder contains more examples which all display some animation in endless loops. If you have installed PyMuPDF and PySimpleGUI, you can execute any of them rightaway.

--------------------------------------------
If you find my work for PyMuPDF useful, you might consider a PayPal donation:

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=PE6665GMGMDEY&source=url)
