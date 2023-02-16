# General Text Extraction
This folder contains a number of scripts for extracting and analyzing text from documents.

* `lookup-keywords.py`: easily finds the values for certain keywords whenever the page's layout is "predictable": every keyword is followed by its value, no text is in between and the value's boundary box is not higher up on the page. The location of both items is not otherwise restricted.

* `layout-analyzer.py`: produces a new PDF showing the layout of all text and images.

* `pdf2text.py`: "naive" or "native" text extraction, which simply prints the text as encountered in the document page. In many cases this may lead to text not appearing in the intended reading order or even to illegible text.

* `pdf2textblocks.py`: extracts the text portioned in so-called "blocks", as collected by the underlying MuPDF library. These text blocks are sorted by their accompanying coordinates to establish a "Western" reading order: top-left to bottom-right. In many cases, this output should produce satisfactory results in reading order, while maintaining a high extraction speed. There are however cases, where this expectation cannot be met. For example, multi-column text or text in tables will not show up satisfactorily.

* `fitzcli.py`: is a duplicate of the PyMuPDF batch / CLI module. So it offers all functions and commands described [here](https://pymupdf.readthedocs.io/en/latest/module.html), **_plus_** the new command `"gettext"`, which offers text extraction from arbitrary MuPDF documents. Most importantly, you can now etract text in a **_layout-preserving_** manner. The next section describes this in detail.

# Layout-preserving Text Extraction

Via its subcommand `"gettext"`, script `fitzcli.py` offers text extraction in different formats. Of special interest surely is **_layout preservation_**, which produces text as close to the original physical layout as possible, surrounding areas where there are images, or reproducing text in tables and multi-column text.

Numerous document files (especially PDFs) contain "irregular" text like
* Simulation of bold / shadowed text by double "printing" it (with a small horizontal / vertical offset or inclination). "Naive" extractions may hence deliver multiple copies of the same.
* Permutating the specification sequence of each single character to prevent or impede copy-pasting text from within a PDF viewer window. What you see is **_not_** what you get in such cases: naive extractions might deliver "eci JM .ojrXM" (instead of "Jorj X. McKie") etc. Similar effects may also occur for technical, non-malignant reasons. An example file for this type of thing is `garbled.pdf` in this folder. Copy-paste the text using your PDF viewer or internet browser: many will deliver nonsense (e.g. Linux `evince`, Mozilla Firefox), some do a decent job. File ``textmaker2.pdf`` is another such an example created with PyMuPDF - try it out!
* Unintended specification errors, like writing spaces over preceeding, non-space characters. You may extract "Notifi cation", although no space is visible within the word in any PDF viewer.
* etc.

Many of these pesky situations are being corrected.

In this folder you find examples for PDFs and corresponding text output images for your review.

## Invocation

In its simplest form, the following extracts layouted text from all pages of `filename.ext` and generates file `filename.txt` in "UTF-8" encoding.

`python fitzcli.py gettext filename.ext`

> Since PyMuPDF v1.18.16, the same feature is available via `python -m fitz gettext filename.ext`. You can use the script **earlier**, as long as your PyMuPDF is v1.18.14+.

---------------------------------------

```
python fitzcli.py gettext -h
usage: fitz gettext [-h] [-password PASSWORD] [-mode {simple,blocks,layout}] [-pages PAGES] [-noligatures]
                    [-convert-white] [-extra-spaces] [-noformfeed] [-skip-empty] [-output OUTPUT] [-grid GRID]
                    [-fontsize FONTSIZE]
                    input

----------------- extract text in various formatting modes ----------------

positional arguments:
  input                 input document filename

optional arguments:
  -h, --help            show this help message and exit
  -password PASSWORD    password for input document
  -mode {simple,blocks,layout}
                        mode: simple, block sort, or layout (default)
  -pages PAGES          select pages, format: 1,5-7,50-N
  -noligatures          expand ligature characters (default False)
  -convert-white        convert whitespace characters to space (default False)
  -extra-spaces         fill gaps with spaces (default False)
  -noformfeed           write linefeeds, no formfeeds (default False)
  -skip-empty           suppress pages with no text (default False)
  -output OUTPUT        store text in this file (default inputfilename.txt)
  -grid GRID            merge lines if closer than this (default 2)
  -fontsize FONTSIZE    only include text with a larger fontsize (default 3)
```

The output filename defaults to the input with its extension replaced by ``.txt``.
As with other commands, you can select page ranges in ``mutool`` format as indicated above.

* **mode:** select a formatting mode -- default is "layout". Output of "simple" is the same as for script `pdf2text.py`, and "blocks" produces the output of `pdf2textblocks.py`. So this script is an extended replacement for all of them.
* **noligatures:** corresponds to **not** `TEXT_PRESERVE_LIGATURES`. If specified, ligatures (present in advanced fonts: glyphs combining multiple characters like "fi") are split up into their components (i.e. "f", "i"). Default is passing them through.
* **convert-white:** corresponds to **not** `TEXT_PRESERVE_WHITESPACE`. If specified, all white space characters (like tabs) are replaced with one or more spaces. Default is passing them through.
* **extra-spaces:**  corresponds to **not** `TEXT_INHIBIT_SPACES`. If specified, large gaps between adjacent characters will be filled with one or more spaces. Default is generating spaces to fill gaps.
* **noformfeed:**  instead of ``hex(12)`` (formfeed), write linebreaks ``\n`` at end of output pages.
* **skip-empty:**  skip pages with no text.
* **grid:** lines with a vertical coordinate difference of no more than this value (float, in points) will be merged into the same output line. Only relevant for "layout" mode. **Use with care:** the default 2 should be adequate in most cases. If **too large**, lines intended to be different will result in garbled and / or incomplete merged output. If **too low**, separate, artifact output lines may be generated for text spans just because they are coded in a different font with slightly deviating properties.
* **fontsize:** ignore text with fontsize of less or equal this (float) value, default is 3.

Command options may be abbreviated as long as no ambiguities are introduced. So the following specifications have the same effect:
* `... -output text.txt -noligatures -noformfeed -convert-white -grid 3 -extra-spaces ...`
* `... -o text.txt -nol -nof -c -g 3 -e ...`

