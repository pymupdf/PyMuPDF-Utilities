"""
A basic text-to-PDF converter
--------------------------------------------------------------------------------
License: GNU GPL V3
(c) 2018 Jorj X. McKie

Usage
-----
python convert.py input.txt
"""

import sys
import fitz

assert len(sys.argv) == 2, "usage: python %s text.file" % (sys.argv[0],)
ifn = sys.argv[1]
ofn = "output.pdf"

width, height = fitz.paper_size("a4")
fontsz = 10
lineheight = fontsz * 1.2

nlines = int((height - 108.0) / lineheight)

sourcefile = open(ifn)
line_ctr = 0  # page line counter
total_ctr = 0  # total line counter
out_ctr = 0  # count output lines
out_buf = ""  # text of one page

doc = fitz.open()


def page_out(b):
    page = doc.new_page(width=width, height=height)
    return page.insert_text(
        (50, 72),
        text=b,
        fontsize=fontsz,
    )


while True:
    line = sourcefile.readline()
    if line == "":
        break
    out_buf += line
    line_ctr += 1
    total_ctr += 1
    if line_ctr == nlines:
        out_ctr += page_out(out_buf)
        out_buf = ""
        line_ctr = 0

if len(out_buf) > 0:
    out_ctr += page_out(out_buf)

print("PDF conversion results for file '%s':" % (ifn,))
print(out_ctr, "lines read,", total_ctr, "lines written,", nlines, "lines per page.")
print(ofn, "contains", len(doc), "pages.")

# Now add a header and footer to each page
hdr_fontsz = 16
ftr_fontsz = 8
blue = fitz.pdfcolor["blue"]
pspace = 500

for page in doc:
    footer = "%i (%i)" % (page.number + 1, len(doc))  # footer text
    plen_ftr = fitz.get_text_length(footer, fontname="Helvetica", fontsize=ftr_fontsz)
    page.insert_text(
        (50, 50), ifn, color=blue, fontsize=hdr_fontsz  # header = input filename
    )
    page.draw_line(
        fitz.Point(50, 60),
        fitz.Point(50 + pspace, 60),  # line below hdr
        color=blue,
        width=0.5,
    )
    page.draw_line(
        fitz.Point(50, height - 33),  # line above footer
        fitz.Point(50 + pspace, height - 33),
        color=blue,
        width=0.5,
    )
    page.insert_text(
        (50 + pspace - plen_ftr, height - 33 + ftr_fontsz * 1.2),  # insert footer
        footer,
        fontsize=ftr_fontsz,
        color=blue,
    )
    page.clean_contents()

doc.set_metadata(
    {
        "creationDate": fitz.get_pdf_now(),
        "modDate": fitz.get_pdf_now(),
        "creator": "convert.py",
        "producer": "PyMuPDF %s" % fitz.VersionBind,
        "title": "Content of file " + ifn,
        "subject": "Demonstrate methods new_page, insert_text and draw_line",
        "author": "Jorj McKie",
    }
)
doc.subset_fonts()
doc.ez_save(ofn, garbage=4, pretty=True)
doc.close()
