import fitz
import sys


def make_msg(font):
    flags = font.flags
    msg = ["%i glyphs" % font.glyph_count, "size %i" % len(font.buffer)]
    if flags["mono"] == 1:
        msg.append("mono")
    if flags["serif"]:
        msg.append("serifed")
    if flags["italic"]:
        msg.append("italic")
    if flags["bold"]:
        msg.append("bold")
    msg = "/".join(msg)
    return msg


infilename = sys.argv[1]
font_list = set()
doc = fitz.open(infilename)
for i in range(len(doc)):
    for f in doc.getPageFontList(i, full=True):
        if f[-1] == 0:
            continue  # no support for text in XObjects
        msg = ""
        xref = f[0]
        fontname = f[3]
        if f[1] == "n/a":
            msg = "not embedded"
        else:
            extr = doc.extractFont(xref)
            font = fitz.Font(fontbuffer=extr[-1])
            msg = make_msg(font)
        idx = fontname.find("+") + 1
        fontname = fontname[idx:]
        font_list.add((xref, fontname, msg))

font_list = list(font_list)
font_list.sort(key=lambda x: x[1])
outname = infilename + "-fontnames.csv"
out = open(outname, "w")
for xref, fontname, msg in font_list:
    msg1 = "keep"
    out.write("%i;%s;%s; %s\n" % (xref, fontname, msg1, msg))
out.close()
