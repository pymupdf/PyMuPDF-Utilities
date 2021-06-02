"""
Demo script using Tesseract OCR.

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
Tesseract must be installed and invocable via Python's 'subprocess' module.
You also must install all the Tesseract language support you need to detect.
"""
import fitz
import subprocess
import time

# Tesseract invocation command (Windows version)
# Assume: language English. Detect more languages by add e.g. '+deu' for German.
# Assume: text represents one line (--psm 7)
# Note: Language mix spec increases duration by >40% - only use when needed!
tess = "tesseract stdin stdout --psm 7 -l eng"
mat = fitz.Matrix(4, 4)  # high resolution matrix
ocr_time = 0
pix_time = 0


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
        colorspace=fitz.csGRAY,  # we need no color
        matrix=mat,
        clip=bbox,
    )
    image = pix.tobytes("png")  # make a PNG image
    t1 = time.perf_counter()
    # Step 2: Invoke Tesseract to OCR the image. Text is stored in stdout.
    rc = subprocess.run(
        tess,  # the command
        input=image,  # the pixmap image
        stdout=subprocess.PIPE,  # find the text here
        shell=True,
    )

    # because we told Tesseract to interpret the image as one line, we now need
    # to strip off the line break characters from the tail.
    text = rc.stdout.decode()  # convert to string
    text = text[:-3]  # remove line end characters
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
                if chr(65533) in text:  # invalid characters encountered!
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
