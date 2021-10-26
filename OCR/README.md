# Demo Scripts using PyMuPDF with OCR
Starting with its version 1.18.0, MuPDF supports dynamically invoking Tesseract OCR to interpret text on pages or images. With its version 1.19.0, PyMuPDF has started supporting this interface.

The folder contains examples for using OCR alternatives - with and without using the MuPDF interface.

## Script `tesseract1.py` - Direct Use of Tesseract
This demo script reads the text of a document containing characters that cannot be interpreted. Such characters are coded as `chr(65533)` by MuPDF. On every encounter of a text span with this a character, Tesseract OCR is invoked via Python's `subprocess` for interpretation. There is no other / direct connection between the script and the Tesseract installation.

The script's approach is this
* Extract the page's text to a `dict` via `get_text("dict", flags=0)["blocks"]`.
* Iterate through the dict and check whether the span text contains a `chr(65533)`.
* In this case, create a pixmap of the span's bbox and invoke Tesseract to OCR this image.
* Print old and new text for visual comparison.

The average duration for each such OCR action is around 0.65 seconds (Windows 10, 64bit, Intel 2.6 GHz, 16 GB memory).

The example PDF (4 pages) has been created via MS Word's PDF output and contains overall 5 spans with problem characters.

> There is a MuPDF version ``tesseract2.py`` - which is more than **_10 times_** faster! Requires v1.19.0.

## Script `easyocr1.py` - Uses Python Package `easyocr`
A very similar script with the same approach as `tesseract1.py`.

In contrast, Python package `easyocr` is invoked to do the OCR job. Other than that, the code is exactly the same.

`easyocr` is a very heavy-weight package, which depends on a lot of yet other packages with a significant footprint - among them are scipy, numpy, torch and several others.

With the same example PDF, the duration per OCR action is about three times longer (2 seconds each) than using Tesseract. Admittedly, I do not have installed GPU / CUDA support on my machine, which should improve performance a lot.

There are also a few unresolved issues with the correct OCR results: if text contains a hyphen "-", then the resulting OCR-ed text tends to be mutilated.

## Script `ocrpages.py` - Uses Python Package `ocrmypdf`
A very basic script that uses Python package OCRmyPDF.
Loops over a PDF's pages and passes each to ocrmypdf. To be used like:

```
python ocrpages.py scanned.pdf
```

I hope it is obvious how this script can be adapted to a specific need - for example:
* one could decide whether or not OCR-ing a page based on criteria like (1) is it a fullpage image, (2) normal text extractions deliver nothing or deliver a lot of unrecognized characters, etc.
* one could OCR **_all_** pages of the input and work with the fully OCR-ed output PDF instead.
* Instead of naive text extraction, more advanced forms can be used, like "dict", "html", etc.

> This script is no longer necessary with PyMuPDF verion 1.19.0 or higher. Its only value is that it shows how to **_interface with OCRmyPDF_** from within Python.

## Script ``images-to-ocr-pdf.py`` - Convert List of Images to an OCR PDF
Walks through some list of image filenames, OCRs the image and appends the result as a page of a new PDF.
