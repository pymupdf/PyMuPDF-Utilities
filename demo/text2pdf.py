import sys

import fitz

assert len(sys.argv) == 2, "usage: python %s text.file" % (sys.argv[0],)
ifn = sys.argv[1]
ofn = ifn + ".pdf"  # name of PDF output
"""
------------------------------------------------------------------------------
A very basic text-to-PDF converter.
-------------------------------------
Any text file.xxx will be converted to file.xxx.pdf
Adjust preferred page format, fontsize, fontname, fontfile below.
Formula of lines per page (nlines) is also used by the 'insertPage' method.
------------------------------------------------------------------------------
"""

width, height = fitz.paper_size("a4")  # choose paper format
fontsz = 10  # choose font size of text
lineheight = fontsz * 1.2  # line height is 20% larger
# the above gives the following lines per page:
nlines = int((height - 108.0) / lineheight)

# choose a nice mono-spaced font of the system, instead of 'Courier'.
font = fitz.Font("cascadia")
fontname = "F0"  # fontname

sourcefile = open(ifn)  # we are going to convert this file
line_ctr = 0  # page line counter
total_ctr = 0  # total line counter
out_ctr = 0  # count output lines
out_buf = ""  # text of one page

doc = fitz.open()  # new empty PDF


def page_out(b):  # only a shortcut
    page = doc.new_page(width=width, height=height)
    page.insert_font(fontname=fontname, fontbuffer=font.buffer)
    return page.insert_text(
        (50, 72),
        text=b,
        fontsize=fontsz,
        fontname=fontname,
    )


while True:
    line = sourcefile.readline()  # read a text line
    if line == "":
        break  # eof encountered
    out_buf += line  # concat line to page buffer
    line_ctr += 1  # increase page ctr
    total_ctr += 1  # increase total ctr
    if line_ctr == nlines:  # page line limit reached
        out_ctr += page_out(out_buf)  # output page to PDF
        out_buf = ""  # clear page buffer
        line_ctr = 0  # clear page line ctr

if len(out_buf) > 0:  # output remaining stuff in buffer
    out_ctr += page_out(out_buf)

print("PDF conversion results for file '%s':" % (ifn,))
print(out_ctr, "lines read,", total_ctr, "lines written,", nlines, "lines per page.")
print(ofn, "contains", len(doc), "pages.")

# Now add some header and footer to each created page

hdr_fontsz = 16  # header fontsize
ftr_fontsz = 8  # footer fontsize
blue = fitz.pdfcolor["blue"]  # header / footer color
pspace = 500  # available line width

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

# finally provide some metadata
m = {
    "creationDate": fitz.get_pdf_now(),  # current timestamp
    "modDate": fitz.get_pdf_now(),  # current timestamp
    "creator": "text2pdf.py",
    "producer": "PyMuPDF %s" % fitz.VersionBind,
    "title": "Content of file " + ifn,
    "subject": "Demonstrate methods new_page, insert_text and draw_line",
    "author": "Jorj McKie",
}

doc.set_metadata(m)

# and save the PDF
doc.subset_fonts()
doc.ez_save(ofn, garbage=4, pretty=True)
doc.close()
