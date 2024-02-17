"""
PyMuPDF demo script

Show how to extend the standard "dict" and "rawdict" text extraction outputs
with information from the Page method "get_texttrace()":
* Sequenz number ("seqno")
* Type (stroke, fill, hidden)
* Opacity
"""

import fitz
import time

doc = fitz.open("extend-dicts.pdf")
page = doc[0]
char_dict = {}
t0 = time.perf_counter()
for span in page.get_texttrace():
    seqno = span["seqno"]
    stype = span["type"]
    opacity = span["opacity"]
    for char in span["chars"]:
        origin = char[2]
        char_dict[origin] = (seqno, stype, opacity)

t1 = time.perf_counter()
print(f"Number of characters detected {len(char_dict.keys())}.")

text_blocks = page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)["blocks"]
t2 = time.perf_counter()
for b in text_blocks:
    for l in b["lines"]:
        for s in l["spans"]:
            origin = s["origin"]
            val = char_dict.get(s["origin"])
            if val is None:  # a previous span has all this info
                s["seqno"] = seqno
                s["opacity"] = opacity
                s["type"] = stype
                continue
            seqno, stype, opacity = val
            s["seqno"] = seqno
            s["opacity"] = opacity
            s["type"] = stype

t3 = time.perf_counter()
print("Timings:")
print(f"Make texttrace dictionary: {t1-t0}")
print(f"Extend standard dictionary: {t3-t2}")
