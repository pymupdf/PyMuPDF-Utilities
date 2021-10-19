"""
This is a demo script that uses MuPDF OCR facilities based on Tesseract-OCR.

The main purpose is to extract text spans from a document's pages in a way that
is independent from whether text is extractable in the normal way or if
contained in any images that may be displayed by the page.
This explicitely includes documents that have been scanned and therefore contain
no text that can be extracted by basic means.

The approach is to combine the page's standard text with text that can be
OCR-ed from the page images. This has the following advantages:

- faster execution if only some text is contained in images
- proper text OCR-ing even when images overlap / hide each other
- no unnecessary rendering of standard text - keep all of its properties
- images are each OCR-ed with their native resolution and not re-rendered via
  the page pixmap
- no dpi / resolution concerns: each OCR happens as best as can be.

Remarks:
- This demo just produces a PDF with all recognized text marked. An improvment
  might rewrite OCR text as hidden text underneath each image.
- There is no check yet, whether there already exists OCR-ed text
- Requires PyMuPDF v1.19.0.

-------------------------------------------------------------------------------
PyMuPDF v1.19.1 makes this script obsolete!
-------------------------------------------------------------------------------
"""
import sys
import fitz

if tuple(map(int, fitz.VersionBind.split("."))) < (1, 19, 0):
    raise ValueError("Need at least PyMuPDF v1.19.0")


def image_spans(page):
    """Performs OCR for all images on the page and returns a list of the spans."""
    spans = []
    doc = page.parent
    for item in page.get_images():
        xref = item[0]
        pix = fitz.Pixmap(doc, xref)
        try:
            bbox = page.get_image_rects(xref)[0]
        except IndexError:
            continue  # img in list, but not displayed
        imgdoc = fitz.open("pdf", pix.pdfocr_tobytes())  # pdf with OCR-ed page
        imgpage = imgdoc.load_page(0)
        imgrect = imgpage.rect  # page size in image PDF
        shrink = fitz.Matrix(bbox.width / imgrect.width, bbox.height / imgrect.height)
        shift = fitz.Matrix(1, 0, 0, 1, bbox.x0, bbox.y0)
        mat = shrink * shift  # transform img coords back to coords on original page
        # extract text in image and store spans in list
        for b in imgpage.get_text("dict", flags=0)["blocks"]:
            for l in b["lines"]:
                for s in l["spans"]:  # re-compute span bbox to original
                    s["bbox"] = tuple(fitz.Rect(s["bbox"]) * mat)
                    spans.append(s)
    return spans


doc = fitz.open(sys.argv[1])

for page in doc:
    spans = image_spans(page)

    # we now have all image text as a list of spans.
    # extend this with "normal" text.
    for b in page.get_text("dict", flags=0)["blocks"]:
        for l in b["lines"]:
            for s in l["spans"]:
                spans.append(s)
    # for demo purposes, mark each span
    for s in spans:
        page.draw_rect(s["bbox"], color=(1, 0, 0), width=0.3)

doc.ez_save(__file__.replace(".py", ".pdf"))
