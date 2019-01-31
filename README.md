# PyMuPDF-Utilities
Various utilities using PyMuPDF

* **morph-demo1.py, morph-demo2.py, morph-demo3.py** are scripts showing the effect of the ``morph`` parameter in text insertions. Each script creates a PDF page, fills a  text box and then morphs that box using its upper left corner as fixed point. Each morphing result is put on a new PDF page and the resulting pixmap is shown in an endless loop. Now require PyMuPDF v1.14.5 and can be run with Python v2.7.

* **quad-show1.py, quad-show2.py** require PyMuPDF v1.14.5 and can be run with Python v2.7. They demonstrate how the modified version of `drawOval` can be used to create a wide range of shapes, both displaying the results in an endless loop.

* **all-my-pics-attached.py** - take all files from a given directory and **attach** them to pages (as *'FileAttachment'* annotations) of a new PDF. Non-file entries of the directory will be skipped.

* **all-my-pics-embedded.py** - take all files from a given directory and **embed** them (as *'EmbeddedFile'* entries) in a new PDF. Non-file entries of the directory will be skipped.

* **all-my-pics-inserted.py** - take all *image* files from a given directory and **insert** them as pages in a new PDF (actually inserts the **first page** of any supported non-PDF document). Non-file entries of the directory will be skipped.

* **anonymize.py** - scan through a PDF and remove all text of all pages. Also erase metadata / XML metadata. This works by eliminating everything enclosed by the string pairs "BT" and "ET" in the pages' `/Contents` object(s). Text appearing in images cannot be removed with this script -- this includes images made by the PDF operator syntax: some utilities synthesize text on the basis of elementary drawing commands, i.e. every single letter is created by drawing rectangles, lines and curves. This is probably done as a way to enforce copyright protection. In these cases, the script will not work either.

* **extract-imga.py** - **(requires v1.13.17)** extract images from a PDF looping through its pages. It takes care of images with a transparency ("stencil") mask and also tries to identify and skip "irrelevant" images. Suppresses extracting the same image multiple times. You may also want to look at ``extract-imgb.py`` below.

* **extract-imgb.py** - **(requires v1.13.17)** extract all images from a PDF looping through its cross references numbers. Ignores the page tree and generally seeks to be as robust as possible with respect to damaged PDFs. Otherwise similar to the previous script in ignoring irrelevant images and working with stencil masks.

* **DeDRM-ebook.py** - repeatedly copies a fixed screen area to a PDF page. Can be used to page through an e-book (which might be DRM protected ...) and create a PDF consisting of all its pages in image format - very much like making a full book photo copy. You would start an e-book reader to read a book and then trigger this skript to page through the displayed book making images page by page.

* **doc-browser.py** - a complete GUI document displaying script using **Tkinter**! It features a zooming facility and can display all document types supported by MuPDF (i.e. **not just PDFs!**). It requires [PySimpleGUI](https://pypi.org/project/PySimpleGUI/), an awesome pure Python package exclusively based on Tkinter. For response time improvements, we are also using [Pillow](https://pypi.org/project/Pillow/).

* **layout-analyzer.py** - create an output PDF for a given PDF with text and graphics layout analysis. Each text and graphics block is surrounded by a rectangle (graphics content is not shown, only some metadata). Output PDF has page dimensions of the input's /MediaBox. The input's /CropBox is indicated by a gray background rectangle - see example files in this repo: demo1.pdf and layout-demo1.pdf.

* **clean-cont.py** - **(requires v1.13.5)** Inspect PDF pages whether any have multiple /Contents objects. If not, exit immediately. If **yes**, check if any contents are shared between pages. If **yes**, save the document using the "clean" option and exit. If **not,**  join multiple page contents into one and save with option "garbage=3" (which removes now unused objects).

* **textboxtract.py** Shows how to extract the text from within a given rectangle. This works for **all document types** - not just PDF.

* **show-no-annots.py** create a pixmap from a PDF page showing **no annotations**.

* **form-fields.py** demo script: create a PDF with form fields.

* **shapes_and_symbols.py** contains ca. 10 predefined symbols, which can be imported and used in PDF page creation. If invoked standalone, a PDF is created with one page per each of the symbols.

* **symbol-list.py** creates a list of symbols and their descriptions, which are implemented in **shapes_and_symbols.py** -- thus also demonstrating how to use this module.

* **sierpinski-fitz.py** demonstrates the use of ``Pixmaps`` be creating Sierpinski's carpet (a fractal).

* **sierpinski-punch.py** does the same thing, but this time uses a more intuitive recursive function.

* the **animations** folder contains more examples which all display some animation in endless loops. If you have installed PyMuPDF and PySimpleGUI, you can execute any of them rightaway.

--------------------------------------------
If you find my work for PyMuPDF useful, you might consider a PayPal donation:

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=PE6665GMGMDEY&source=url)