# Layout-preserving Text Extraction

Script `textlayout.py` extracts text from the pages of a document to a text file with the same name and file extension `.txt` in the same folder.

It strives to position the text in a layout as close to the original as possible, thus surrounding areas where there are images, or reproducing text in tables and multi-column text.

The script produces results comparable to (and sometimes even better than) the CLI utility `pdftotext -layout ...` of Xpdf software, http://www.foolabs.com/xpdf/.

In this folder you find examples for PDFs and corresponding text output images for your review.

**_Note:_**

> Supported are **_all MuPDF document types_** - not only PDFs.

## Invocation

`python textlayout.py file.ext`

Version updates may include parameter support for specifying passwords, filtering out page ranges, etc.