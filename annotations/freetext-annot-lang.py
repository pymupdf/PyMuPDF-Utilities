# -*- coding: utf-8 -*-
from __future__ import division, print_function

import os
import sys

import fitz

print(fitz.__doc__)
if fitz.VersionBind.split(".") < ["1", "17", "0"]:
    sys.exit("Need PyMuPDF v1.17.0 or later.")

outfile = os.path.abspath(__file__).replace(".py", ".pdf")


doc = fitz.open()  # new PDF
page = doc.newPage()  # new page

text = r"""This is a text of mixed languages to generate FreeText annotations with automatic font selection - a feature new in MuPDF v1.17.
Euro: €, general Latin and other signs: | ~ ° ² ³ ñ ä ö ü ß â ¿ ¡ µ ¶ œ ¼ ½ ¾ ‰
Japan: 熊野三山本願所は、 15世紀末以降における熊野三山 （熊野本宮、 熊野新宮
Greece: Στα ερείπια της πόλης, που ήταν ένα σημαντικό
Korea: 에듀롬은 하나의 계정으로 전 세계 고등교육 기관의 인터넷에 접속할
Russia: Ко времени восшествия на престол Якова I в значительной
China: 北京作为城市的历史 可以追溯到 3,000 年前。西周初年， 周武王封召公奭于燕國。
Devanagari (not supported): नि:शुल्क ज्ञानको लागी लाई धन्यबाद""".splitlines()

blue = (0, 0, 1)
red = (1, 0, 0)
gold = (1, 1, 0)
green = (0, 1, 0)

# make the rectangles for filling in above text lines
tl = page.rect.tl + (72, 144)  # some distance from the page's corners
br = page.rect.br - (72, 144)
rect = fitz.Rect(tl, br)  # put all annots inside this rectangle
cells = fitz.make_table(rect, cols=1, rows=len(text))
shrink = (0, 5, 0, 0)  # makes distance between annots
for i in range(len(text)):
    annot = page.addFreetextAnnot(
        cells[i][0] + shrink,
        text[i],
        fontsize=16,
        fontname="tiro",  # used for non-CJK characters only!
        align=fitz.TEXT_ALIGN_CENTER,
        text_color=blue,
    )
    annot.setBorder(width=1.0)
    annot.update(fill_color=gold, border_color=green)

doc.save(outfile, garbage=3, deflate=True)
