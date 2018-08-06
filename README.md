# PyMuPDF-Utilities
Various utilities using PyMuPDF

* **anonymize.py** - scan through a PDF and remove all text of all pages. Also erase metadata / XML metadata. This works by eliminating everything enclosed by the string pairs "BT" and "ET" in the pages' `/Contents` object(s). Text appearing in images cannot be removed with this script. This includes images made by the PDF operator syntax: some utilities synthesize text on the basis of elementary drawing commands, i.e. every single letter is created by drawing rectangles, lines and curves. This is probably done as a way to enforce copyright protection. In these cases, the script will not work either.

* **gluepix.py** - extract images from a PDF, also taking care of images with a transparency mask. You may want to look at ``extract_img.py`` in this repo, too. It does a similar job, but scans through **all** images, not just the ones referenced by pages. This makes sense when the PDF has structure issues, e.g. a broken page tree.

* **extract-img.py** - **(requires v1.13.17)** extract all images from a PDF, ignoring the page tree. It focuses on execution speed, aims to tolerate damaged files, respects the original image format and avoids using Pixmaps. Masked images are rebuilt like in ``gluepix.py``. Tries to identify and ignore "garbage" images like small artefacts, lines and unicolor rectangles.

* **DeDRM-ebook.py** - repeatedly copies a fixed screen area to a PDF page. Can be used to page through an e-book (which might be DRM protected ...) and create a PDF consisting of all its pages in image format - very much like making a full book foto copy. You would start an e-book reader to read a book and then trigger this skript to page through the displayed book making images of each page.

* **layout-analyzer.py** - create an output PDF for a given document with text and graphics layout analysis. Each text and graphics block is surrounded by a rectangle (graphics content is not shown, only some metadata). Output PDF has page dimensions of the input's /MediaBox. The input's /CropBox is indicated by a gray background rectangle - see example files in this repo: demo1.pdf and layout-demo1.pdf.

* **clean-cont.py** - **(requires v1.13.5)** Inspect PDF pages whether any have multiple /Contents objects. If not, we exit immediately. If **yes**, we check if any contents are shared between pages. If **yes**, we save the the document using the "clean" option and exit. If **not** we join multiple page contents into one, ignore the multiples and save with option "garbage=4".

* **textboxtract.py** Shows how to extract text from from within a given rectangle. This works for **all document types** - not just PDF.

* **show-no-annots.py** create a pixmap from a PDF page showing no annotations.
