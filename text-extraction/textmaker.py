"""
Generates a PDF page to demonstrate capabilities and limitations of various
text extraction methods.
The page is divided in 4 rectangles like this:
+---------------------------------------+
|                Header                 |
+---------------------------------------+
|                   |                   |
|    Left           |    Right          |
|    Text           |    Text           |
|    Column         |    Column         |
|                   |                   |
|                   |                   |
+---------------------------------------+
|                Footer                 |
+---------------------------------------+
The rectangles are filled with text in the following sequence:
1. Footer
2. Left
3. Right
4. Header
This will prove "naive" text extraction almost useless and blockwise
extraction just roughly sufficient.
The only adequate solution will be layout preservation.
"""
import fitz

font = fitz.Font("helv")
doc = fitz.open()
page = doc.new_page(width=300, height=300)
# define a page area without border
printrect = page.rect + (36, 36, -36, -36)
# define the 4 rectangles
headrect = +printrect
headrect.y1 = printrect.y0 + 36
footrect = +printrect
footrect.y0 = printrect.y1 - 36
textrect = fitz.Rect(headrect.x0, headrect.y1, headrect.x1, footrect.y0)
leftrect = +textrect
leftrect.x1 -= textrect.width / 2
rightrect = +textrect
rightrect.x0 += textrect.width / 2

# now prepare text
tw = fitz.TextWriter(page.rect)
header = "Header"
footer = "Footer"
left = "Left Text Column.\n\nThis is text we want to see in the left text column.\nWe will show it with centered alignment."
right = "Right Text Column.\n\nThis is text we want to see in the right text column.\nWe will show it with centered alignment."
# fill text in rectangles
tw.fill_textbox(footrect, footer, font=font, align=fitz.TEXT_ALIGN_CENTER)
tw.fill_textbox(rightrect, right, font=font, align=fitz.TEXT_ALIGN_CENTER)
tw.fill_textbox(leftrect, left, font=font, align=fitz.TEXT_ALIGN_CENTER)
tw.fill_textbox(headrect, header, font=font, align=fitz.TEXT_ALIGN_CENTER)
tw.write_text(page)
doc.ez_save(__file__.replace(".py", ".pdf"))
