"""
This is a basic script demonstrating the use of OCRmyPDF together with PyMuPDF.

It reads a PDF's pages and passes them to ocrmypdf one by one. One could at this
point insert some checks as to whether the page is actually an, contains no text,
or text with many unrecognized characters or the like.

Each page is then converted to a 1-page temporary PDF which is
- passed to ocrmypdf for OCR-ing it
- the 1-page output PDF of the pervious step is then text-extracted
- return the extracted text

Instead of extracting simple naive text format, one could also use all other
text extraction formats like "dict" to get text position information.

Requires
---------
ocrmypdf
"""
import fitz
import ocrmypdf
import sys
import io


def ocr_the_page(page):
    """Extract the text from passed-in PDF page."""
    src = page.parent  # the page's document
    doc = fitz.open()  # make temporary 1-pager
    doc.insert_pdf(src, from_page=page.number, to_page=page.number)
    pdfbytes = doc.tobytes()
    inbytes = io.BytesIO(pdfbytes)  # transform to BytesIO object
    outbytes = io.BytesIO()  # let ocrmypdf store its result pdf here
    ocrmypdf.ocr(
        inbytes,  # input 1-pager
        outbytes,  # ouput 1-pager
        language="eng",  # modify as required e.g. ("eng", "ger")
        output_type="pdf",  # only need simple PDF format
        # add more paramneters, e.g. to enforce OCR-ing, etc., e.g.
        # force_ocr=True, redo_ocr=True
    )
    ocr_pdf = fitz.open("pdf", outbytes.getvalue())  # read output as fitz PDF
    text = ocr_pdf[0].get_text()  # ...and extract text from the page
    return text  # return it


if __name__ == "__main__":
    doc = fitz.open(sys.argv[1])
    for page in doc:
        text = ocr_the_page(page)
        print("Text from page %i:" % page.number)
        print(text)
