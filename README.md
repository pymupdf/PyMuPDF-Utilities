# PyMuPDF-Utilities
Various utilities using PyMuPDF

* **all-my-pics-attached.py** - take all files from a given directory and **attach** them to pages (as *'FileAttachment'*) of a new PDF. Non-file entries of the directory will be skipped.

* **all-my-pics-embedded.py** - take all files from a given directory and **embed** them (as *'EmbeddedFile'*) in a new PDF. Non-file entries of the directory will be skipped.

* **all-my-pics-inserted.py** - take all image files from a given directory and **insert** them as pages in a new PDF (actually inserts the first page of any supported, non-PDF document type). Non-file entries of the directory will be skipped.

* **anonymize.py** - scan through a PDF and remove all text of all pages. Also erase metadata / XML metadata. This works by eliminating everything enclosed by the string pairs "BT" and "ET" in the pages' `/Contents` object(s). Text appearing in images cannot be removed with this script. This includes images made by the PDF operator syntax: some utilities synthesize text on the basis of elementary drawing commands, i.e. every single letter is created by drawing rectangles, lines and curves. This is probably done as a way to enforce copyright protection. In these cases, the script will not work either.

* **extract-imga.py** - **(requires v1.13.17)** extract images from a PDF looping through its pages. It takes care of images with a transparency ("stencil") mask and also tries to identify and skip "irrelevant" images. Suppresses extracting the same image multiple times. You may also want to look at ``extract-imgb.py`` below.

* **extract-imgb.py** - **(requires v1.13.17)** extract all images from a PDF looping through its cross references numbers. Ignores the page tree and generally seeks to be as robust as possible with respect to damaged PDFs. Otherwise similar to the previous script in ignoring irrelevant images and working with stencil masks.

* **DeDRM-ebook.py** - repeatedly copies a fixed screen area to a PDF page. Can be used to page through an e-book (which might be DRM protected ...) and create a PDF consisting of all its pages in image format - very much like making a full book foto copy. You would start an e-book reader to read a book and then trigger this skript to page through the displayed book making images of each page.

* **doc-browser.py** - a complete GUI document displaying script using **Tkinter**! It features a zooming facility and can display all document types supported by MuPDF (not just PDFs). It requires [PySimpleGUI](https://pypi.org/project/PySimpleGUI/), an awesome pure Python package exclusively based on Tkinter, which requires Python 3 to be used. For response time improvements, we are also using PIL (Pillow).

* **layout-analyzer.py** - create an output PDF for a given document with text and graphics layout analysis. Each text and graphics block is surrounded by a rectangle (graphics content is not shown, only some metadata). Output PDF has page dimensions of the input's /MediaBox. The input's /CropBox is indicated by a gray background rectangle - see example files in this repo: demo1.pdf and layout-demo1.pdf.

* **clean-cont.py** - **(requires v1.13.5)** Inspect PDF pages whether any have multiple /Contents objects. If not, we exit immediately. If **yes**, we check if any contents are shared between pages. If **yes**, we save the the document using the "clean" option and exit. If **not** we join multiple page contents into one, ignore the multiples and save with option "garbage=4".

* **textboxtract.py** Shows how to extract text from from within a given rectangle. This works for **all document types** - not just PDF.

* **show-no-annots.py** create a pixmap from a PDF page showing no annotations.

* **form-fields.py** demo script: create a PDF with form fields.

* **morph-demo1.py, morph-demo2.py, morph-demo3.py** are scripts showing the effect of the ``morph`` parameter in text insertions. Each script creates a PDF page, fills a  text box and then morphs that box using the box's upper left corner as fixed point. The effects are being shown by [morphing.gif](https://github.com/JorjMcKie/PyMuPDF-Utilities/blob/master/morphing.gif).

