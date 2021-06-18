# -*- coding: utf-8 -*-
"""
PyMuPDF demo program for text output as of v1.17.0.


"""
import os

import fitz

outfile = os.path.abspath(__file__).replace(".py", ".pdf")

doc = fitz.open()
page = doc.new_page()

page_rect = page.rect

blue = (0, 0, 1)  # color 1
red = (1, 0, 0)

# This font will be used for Latin, Greek, Russian characters only.
# CJK characters always are looked up in 'Doid Sans Fallback Regular'.
font = fitz.Font(ordering=0)  # results in fallback font for everything
fsize = 11  # fontsize

"""
-------------------------------------------------------------------------------
Our text lines. We split them into words such that the first word of each
line starts with a line break. Multiple spaces between words will be kept.

Disclaimer:
Non-English text pieces are arbitrary copies out of Wikipedia pages. I have no
idea what they mean nor am I responsible for that content.
-------------------------------------------------------------------------------
"""
# Our text: a language mix. Font above (if different from fallback) will be
# used for non-CJK characters. For CJK, the fallback is always used.
text = """This is a text of mixed languages to demonstrate MuPDF's text output capabilities.
Font used for the non-CJK characters: '%s', font size: %g, color: %s.
Euro: €, some special signs: |~°²³, general Latin: ñäöüßâ
Japan: 熊野三山本願所は、15世紀末以降における熊野三山（熊野本宮、熊野新宮
Greece: Στα ερείπια της πόλης, που ήταν ένα σημαντικό
Korea: 에듀롬은 하나의 계정으로 전 세계 고등교육 기관의 인터넷에 접속할
Russia: Ко времени восшествия на престол Якова I в значительной
China: 北京作为城市的历史可以追溯到3,000年前。西周初年，周武王封召公奭于燕國。
This longer text part checks, whether the very last line will not be justified either.""" % (
    font.name,
    fsize,
    blue,
)

fill_rect = fitz.Rect(72, 72, 372, 372)  #  keep above text in here
writer = fitz.TextWriter(page_rect, color=blue)  # start a text writer

writer.fill_textbox(  # fill in above text
    fill_rect,  # keep text inside this
    text,  # the text
    align=fitz.TEXT_ALIGN_JUSTIFY,  # alignment
    warn=True,  # keep going if too much text
    fontsize=fsize,
    font=font,
)

# write our results to the PDF page.
writer.write_text(page)

# To show what happened, draw the rectangles, etc.
shape = page.new_shape()
shape.draw_rect(writer.text_rect)  # the generated TextWriter rectangle
shape.draw_circle(writer.last_point, 2)  # coordinates of end of text
shape.finish(color=blue, width=0.3)  # show with blue color
shape.draw_rect(fill_rect)  # the rect within which we had to stay
shape.finish(color=red, width=0.3)  # show in red color
shape.commit()

textbox = writer.text_rect & fill_rect  # calculate rect intersection

"""
Write once more, but shifted, scaled and rotated by some amount.
This uses the 'morph' argument introduced in v1.17.0.
"""
mat = fitz.Matrix(1, 1)
mat *= fitz.Matrix(-15)  # rotation
mat *= fitz.Matrix(0.8, 0.8)  # scaling
mat.pretranslate(50, -fill_rect.height)  # translation
point = fill_rect.bl  # use as pivotal point for morphing
writer.write_text(
    page,
    morph=(point, mat),
    color=0,  # choose a different text color
    opacity=0.5,  # also override opacity property
)

"""
Write the text box also in a number of other ways on subsequent pages.
Method 'Page.write_text' supports:
    - combining several TextWriter objects
    - putting directly in specific rectangles
    - automatic scaling
    - controlling aspect ratio
    - using rotation
    - put in foreground or background
It internally uses method 'show_pdf_page'.
"""
page = doc.new_page()
# Rotation by 180 degrees can use the same textbox. The same effect can be
# achieved with TextWriter by using morph=(M, Matrix(180)), where M is the
# middle point of textbox.
page.write_text(
    textbox,  # content will always be contained in this rect
    rotate=180,  # other angles will result in scaling down
    writers=writer,
)

page = doc.new_page()
# now rotate by 90 and by 270 degrees. For this we exchange width and height
# and for more fun, we also scale down.
textbox1 = fitz.Rect(
    textbox.tl, textbox.x0 + textbox.height / 2, textbox.y0 + textbox.width / 2
)
textbox2 = textbox1 + fitz.Rect(0, 1, 0, 1) * textbox1.height
page.write_text(textbox1, writers=writer, rotate=90)
page.write_text(textbox2, writers=writer, rotate=-90, color=red)

page = doc.new_page()
# now a rotation by other than 90-degree-multiples
page.write_text(page.rect, writers=writer, rotate=-45)


doc.save(
    outfile,
    garbage=4,  # this eliminates duplicates of large binary objects!
    deflate=True,
)
