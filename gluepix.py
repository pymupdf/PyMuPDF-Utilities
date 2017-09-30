from __future__ import print_function
import fitz
"""
PyMuPDF utility
----------------
For a given entry in a page's getImagleList() list, function "recoverpix"
returns the PNG image. This can then e.g. be saved to disk.
The item's first two entries are PDF xref numbers. The first one is the image in
question, the second one may be 0 or the object id of a soft-image mask. In this
case, we assume it being a sequence of alpha bytes belonging to our image.
We then create a new Pixmap giving it these alpha values, and return the PNG
image of it.
This an intermediate solution while PyMuPDF is developing a better one.
So currently, we only support RGB images. A final PyMuPDF solution should look
like this:
(1) A new Pixmap creation method, which takes a zero-alpha input and
    creates a copy of it with an alpha channel (filled with 0xff).
(2) A new Pixmap method allowing to fill the alpha channel with the contents
    of a given sequence of bytes.
"""

def recoverpix(doc, item):
    x = item[0]
    s = item[1]
    pix1 = fitz.Pixmap(doc, x)
    if s == 0:
        return pix1.getPNGData()
    pix2 = fitz.Pixmap(doc, s)
    assert pix1.n == 3, "unexpected colorspace " + pix1.colorspace.name
    assert pix2.n == 1, "unexpected colorspace " + pix2.colorspace.name
    balen = len(pix1.samples) + len(pix2.samples)
    ba = bytearray(b"?" * balen)       # allocate bytearray (performance)
    i = j = k = 0
    while i < balen:
        ba[i+0] = pix1.samples[j+0]    # copy over pixel data
        ba[i+1] = pix1.samples[j+1]    # copy over pixel data
        ba[i+2] = pix1.samples[j+2]    # copy over pixel data
        ba[i+3] = pix2.samples[k]      # mask samples are our alpha
        i += 4
        j += 3
        k += 1
    pix = fitz.Pixmap(pix1.colorspace, pix1.width, pix1.height, ba, 1)
    pix1 = None
    pix2 = None
    return pix.getPNGData()

doc = fitz.open("test.pdf")
il = doc.getPageImageList(0)
for img in il:
    data = recoverpix(doc, img)
    f = open(img[7]+".png", "wb")
    f.write(data)
    f.close()