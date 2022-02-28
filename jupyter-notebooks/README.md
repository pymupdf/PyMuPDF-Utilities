# PyMuPDF JUPYTER Notebooks

These are scripts that explain basic usage of PyMuPDF using jupyter notebook features. Just click on one of the `.ipynb` files to see its fully rendered session!

Over time this script collection will be extended. Your contribution is very welcome!

## Example Files
* `1page.pdf` - 1-pager PDF used as a test file by several notebooks
* `blacked.pdf` - 1-pager PDF with three words covered by black rectangles. Used by `detect-hidden.ipynb` which demonstrates how badly done "redactions" can be detected - **detects hidden text.**
* `partial_ocr.pdf`- 1-pager PDF containing normal text and two images that overlap each other.

## Notebooks
* `dehyphenate-flag.ipynb` - shows the effect of flag `TEXT_DEHYPHENATE` on text search and extraction.
* `detect-hidden.ipynb` - shows how to **_detect text which is hidden_** by objects "drawn above" it.
* `journalling1.ipynb` - introduction to PDF Journalling
* `journalling2.ipynb` - chapter 2 of PDF Journalling
* `journalling3.ipynb` - chapter 3 of PDF Journalling
* `new-circle-annot.ipynb` - simple example for adding an annotation with desired properties
* `ocr-illegible.ipynb` - OCR: how to dynamically make unrecognized characters readable
* `partial-ocr.ipynb` - OCRs a page in full and in partial mode and explain the difference. Requires PyMuPDF v1.19.1.
* `testpage-performance.ipynb` - compare performance of text extraction and search methods, with and without a separately prepared `TextPage` object.
* `object-algebra.ipynb` - explains details on how points, rectangles quads can be added and multiplied as if they were ordinary numbers. This is an extension to the respective [chapter](https://pymupdf.readthedocs.io/en/latest/algebra.html) of the documentation.