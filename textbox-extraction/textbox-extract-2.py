"""
Script showing how to select only text that is contained in a given rectangle
on a page.

We use "page.getTextbox", which is available since PyMuPDF v1.18.0.
The decision on what whill be included is made by character, so while much
simpler to use than the other script in this folder, it will ignore word
integrity and cut through any part overlaps.

There also is no logic that maintains natural reading order, so text will
appear as stored in the document.

"""
import fitz

doc = fitz.open("search.pdf")  # any supported document type
page = doc[0]  # we want text from this page

"""
-------------------------------------------------------------------------------
Identify the rectangle.
-------------------------------------------------------------------------------
"""
rect = page.firstAnnot.rect  # this annot has been prepared for us!
# Now we have the rectangle ---------------------------------------------------

print(page.getTextbox(rect))
