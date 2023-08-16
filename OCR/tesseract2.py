"""
Demo script using Mupdf OCR.

Extract text of a page and interpret unrecognized characters using Tesseract.
MuPDF codes unrecognizable characters as 0xFFFD = 65533.
Extraction option is "dict", which delivers contiguous text pieces within one
line, that have the same font properties (color, fontsize, etc.). Together with
the language parameter, this helps Tesseract finding the correct character.

The basic approach is to only invoke OCR, if the span text contains
chr(65533). Because Tesseract's response ignores leading spaces and appends
line break characters, some adjustments are made.

--------------
This demo will OCR only text, that is known to be text. This means, it
does not look at parts of a page containing images or text encoded as drawings.
--------------

Dependencies:
PyMuPDF v1.19.0
"""
import fitz
import time

mat = fitz.Matrix(5, 5)  # high resolution matrix
ocr_time = 0
pix_time = 0
INVALID_UNICODE = chr(0xFFFD)  # the "Invalid Unicode" character


def get_tessocr(page, bbox):
    """Return OCR-ed span text using Tesseract.

    Args:
        page: fitz.Page
        bbox: fitz.Rect or its tuple
    Returns:
        The OCR-ed text of the bbox.
    """
    global ocr_time, pix_time, tess, mat
    # Step 1: Make a high-resolution image of the bbox.
    t0 = time.perf_counter()
    pix = page.get_pixmap(
        matrix=mat,
        clip=bbox,
    )
    t1 = time.perf_counter()
    ocrpdf = fitz.open("pdf", pix.pdfocr_tobytes())
    ocrpage = ocrpdf[0]
    text = ocrpage.get_text()
    if text.endswith("\n"):
        text = text[:-1]
    t2 = time.perf_counter()
    ocr_time += t2 - t1
    pix_time += t1 - t0
    return text


doc = fitz.open("v110-changes.pdf")
ocr_count = 0
for page in doc:
    blocks = page.get_text("dict", flags=0)["blocks"]
    for b in blocks:
        for l in b["lines"]:
            for s in l["spans"]:
                text = s["text"]
                if INVALID_UNICODE in text:  # invalid characters encountered!
                    # invoke OCR
                    ocr_count += 1
                    print("before: '%s'" % text)
                    text1 = text.lstrip()
                    sb = " " * (len(text) - len(text1))  # leading spaces
                    text1 = text.rstrip()
                    sa = " " * (len(text) - len(text1))  # trailing spaces
                    new_text = sb + get_tessocr(page, s["bbox"]) + sa
                    print(" after: '%s'" % new_text)

print("-------------------------")
print("OCR invocations: %i." % ocr_count)
print(
    "Pixmap time: %g (avg %g) seconds."
    % (round(pix_time, 5), round(pix_time / ocr_count, 5))
)
print(
    "OCR time: %g (avg %g) seconds."
    % (round(ocr_time, 5), round(ocr_time / ocr_count, 5))
)
