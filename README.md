# PyMuPDF-Utilities
Various utilities using PyMuPDF

* **anonymize.py** - scan through a PDF and remove all text of all pages. Also erase metadata / XML metadata. This works by eliminating everything enclosed by the string pairs "BT" and "ET" in the pages' `/Contents` object(s). Text appearing in images cannot be removed with this script. This includes images made by the PDF operator syntax: some utilities synthesize text on the basis of elementary drawing commands, i.e. every single letter is created by drawing rectangles, lines and curves. This is probably done as a way to enforce copyright protwection. In these cases, the script will not work either.
* **gluepix.py** - extract images from a PDF, also taking care of images with a transparency mask.
* **DeDRM-ebook.py** - repeatedly copies a fixed screen area to a PDF page. Can be used to page through an e-book (which might be DRM protected ...) and create a PDF consisting of all its pages in image format - very much like making a full book foto copy. You would start an e-book reader to read a book and then trigger this skript to page through the displayed book making images of each page.
