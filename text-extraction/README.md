# General Text Extraction
This folder contains a number of scripts for extracting and analyzing text from documents.

* `layout-analyzer.py`: produces a new PDF showing the layout of all text and images.

* `pdf2text.py`: "naive" or "native" text extraction, which simply prints the text as encountered in the document page. In many cases this may lead to text not appearing in the intended reading order or even to illegible text.

* `pdf2textblocks.py`: extracts the text portioned in so-called "blocks", as collected by the underlying MuPDF library. These text blocks are sorted by their accompanying coordinates to establish a "Western" reading order: top-left to bottom-right. In many cases, this output should produce satisfactory results in reading order, while maintaining a high extraction speed. There are however cases, where this expectation cannot be met. For example, multi-column text or text in tables will not show up satisfactorily.

* `textlayout.py`: goes considerably further by extracting each character separately and positioning it on the output as closely resembling the original layout as possible. This is explained in the next section.

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