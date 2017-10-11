# PyMuPDF-Utilities
Various utilities using PyMuPDF

* anonymize.py - scan through a PDF and remove all text of all pages. Also erase metadata / XML metadata. This works by eliminating everything enclosed by string pairs ("BT", "ET") in the pages' `/Contents` objects. Text appearing in images cannot be removed with this skript. What I have recently been amazed to see: some utilities synthesize text on the basis of elementary drawing commands, i.e. every single letter is created by drawing rectangles, lines and curves (e.g. Microsft's print to PDF acting on web pages). For these cases, the skript will not work either.
* gluepix.py - extract images from a PDF, taking care of transparency masks.
