"""
Demo script using package easyocr.

Extract text of a page and interpret unrecognized characters using easyocr.
MuPDF codes unrecognizable characters as 0xFFFD = 65533.
Extraction option is "dict", which delivers contiguous text pieces within one
line, that have the same font properties (color, fontsize, etc.). Together with
the language parameter, this helps easyocr finding the correct character.

The basic approach is to only invoke OCR, if the span text contains
chr(65533). Because easyocr's response ignores leading spaces, some adjustments are made.

--------------
This demo will OCR only text, that is known to be text. This means, it
does not look at parts of a page containing images or text encoded as drawings.
--------------

Dependencies:
easyocr
Potentially CUDA for improved performance.
"""
# ------------------------------------------
# Based on ideas by Github user @victor-ab
# ------------------------------------------
import fitz
import easyocr
import time

easyocr_reader = easyocr.Reader(["en"])

mat = fitz.Matrix(4, 4)  # high resolution matrix
ocr_time = 0
pix_time = 0


def get_easyocr(page, bbox):
    """Return OCR-ed span text using Tesseract.

    Args:
        page: fitz.Page
        bbox: fitz.Rect or its tuple
    Returns:
        The OCR-ed text of the bbox.
    """
    global mat, ocr_time, pix_time
    # Step 1: Make a high-resolution image of the bbox.
    t0 = time.perf_counter()
    pix = page.get_pixmap(
        colorspace=fitz.csGRAY,
        matrix=mat,
        clip=bbox,
    )
    image = pix.getImageData("png")
    t1 = time.perf_counter()

    # Step 2: Invoke easyocr to OCR the image.
    detected_text = easyocr_reader.readtext(
        image,
        detail=0,
    )
    t2 = time.perf_counter()
    ocr_time += t2 - t1
    pix_time += t1 - t0
    if len(detected_text) > 0:
        return detected_text[0]
    else:
        return "*** could not interpret ***"


doc = fitz.open("v110-changes.pdf")
ocr_count = 0
for page in doc:
    text_blocks = page.getText("dict", flags=0)["blocks"]
    for b in text_blocks:
        for l in b["lines"]:
            for s in l["spans"]:
                text = s["text"]
                if chr(65533) in text:  # invalid characters encountered!
                    ocr_count += 1
                    print("before: '%s'" % text)
                    text1 = text.lstrip()
                    sb = " " * (len(text) - len(text1))  # leading spaces
                    text1 = text.rstrip()
                    sa = " " * (len(text) - len(text1))  # trailing spaces
                    new_text = sb + get_easyocr(page, s["bbox"]) + sa
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
