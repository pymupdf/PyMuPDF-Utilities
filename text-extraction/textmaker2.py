"""
Generates a PDF page to demonstrate capabilities and limitations of various
text extraction methods.
Reads "textmaker.pdf" created previously, then extracts every single
character and arbitrarily re-arranges the character list.
The make a new PDF page and write each character of the shuffled list
to the same position it had on the original page.
The resulting PDF looks exactly like the original, but refuses to deliver
meaningful results for all conventional text extraction methods.
Also if you try to copy-paste with PDF viewers like Adobe Acrobat,
Foxit Reader, PDF XChange, ... the result will be complete garbage.
Evince on Linux is not as bad. I don't know how OSX tools would compare.

The only possible solution to recover the text is layout preservation.
"""
import fitz
import random

doc = fitz.open("textmaker.pdf")
page = doc[0]
w = page.rect.width
h = page.rect.height
chars = []  # save extracted characters here
font = fitz.Font("helv")  # use same font for output
for b in page.get_text("rawdict")["blocks"]:
    for l in b["lines"]:
        for s in l["spans"]:
            for c in s["chars"]:
                chars.append(c)
doc.close()
doc = fitz.open()  # make new PDF
page = doc.new_page(width=w, height=h)  # new page with the old dimensions
random.shuffle(chars)  # arbitrarily re-order characters
tw = fitz.TextWriter(page.rect)
# write the re-ordered characters to the page
for c in chars:
    tw.append(c["origin"], c["c"], font=font)
tw.write_text(page)
doc.ez_save(__file__.replace(".py", ".pdf"))
