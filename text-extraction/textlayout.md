# Layout-preserving Text Extraction

Script `textlayout.py` extracts text from the pages of a document to a text file with the same name and file extension `.txt` in the same folder.

It strives to position the text in a layout as close to the original as possible, thus surrounding areas where there are images, or reproducing text in tables and multi-column text.

In this folder you find examples for a 1-page and a 3-page PDF and the corresponding text outputs for your review.

**_Note:_**

> Supported are all MuPDF document types - not only PDFs.

## Invocation

`python textlayout.py file.ext`