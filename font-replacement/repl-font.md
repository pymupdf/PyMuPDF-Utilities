# Replacing Font in Existing PDFs with PyMuPDF

Using PyMuPDF v1.17.6 or later, replacing fonts in an existing PDF becomes possible. This describes a set of scripts which allow replacing selected fonts by some others.

## Features
It supports the following features:

* Replace selected or all fonts in a PDF.
* Ensure that all fonts in a PDF are embedded.
* Maintain the page layout, table of contents, links, images, etc.
* Build font subsets based on the characters used.

This makes it e.g. possible to replace **Courier** by a nicer monospaced font, take a non-serifed font instead of Times-Roman, etc.

## Technical Approach

* Each page is searched for text written with one of the replaceable fonts.
* These text pieces are inspected for their used unicodes.
* Build subsets for replacing fonts based on the used unicodes.
* Remove and rewrite each text span for a replaceable font.

The script makes heavy use of and is dependent on MuPDF's page cleaning and text extraction facilities, `Page.cleanContents()` and `Page.getText("dict")`.

## Choosing Replacement Fonts
The font replacing script expects a CSV file which specifies, which fonts should be replace. You must execute a utility script which creates a list of all used fonts and stores it in a CSV file.

Edit this file to specify which fonts you wish to change.

Here is an example output:

| xref | fontname | replace | information |
|------|----------|-------------|-------------|
| 26 | Utopia-Regular-Identity-H | keep |  58 glyphs/size 7498/serifed |
| 30 | Utopia-Semibold-Identity-H | keep |  58 glyphs/size 8037/serifed/bold |
| 34 | Utopia-Italic-Identity-H | keep |  229 glyphs/size 5103/serifed |
| 42 | ZapfDingbats-Identity-H | keep |  2 glyphs/size 371/serifed |
| 47 | ArialMT-Identity-H | keep |  20 glyphs/size 2675/serifed |

Change the **"replace"** column value with a desired replacement font. If you want to keep the old font, ignore that line or delete it.

Use the "information" column to help make up your decision. If the old font contains only a few glyphs ("ZapfDingbats") or a small size, you might want to leave it untouched. Other information like "bold", "mono", etc. may also help choosing the right replacement. Keep in mind however, that this information (provided by the font creator) cannot be garantied to be complete or even correct: you may see "serifed" although it is a "sans" font, or "mono" is missing for a monospaced font, etc.

Use the following values to replace "keep" with a new font name:

* One of the Base-14 builtin fontnames Times-Roman, Helvetica, Courier, Symbol or ZapfDingbats and their font weight alternatives (like "heit" = Helvetica-Oblique).
* One of the CJK builtin fontnames, e.g. "china-t" for traditional Chinese.
* One of the builtin fontnames for repositiory `pymupdf-fonts` fonts, e.g. "figo" for "FiraGO Regular", or "spacemo" for "Space Mono Regular".
* The file name of a font installed on your system, e.g. `C:/Windows/Fonts/DejaVuSerif-Bold.ttf`. In this case, make sure that the file name contains a "`.`" or a path separater ("`/`", "`\`") to be recognized as such.

## Limitations, TODOs, Quality Checks
Existing text is extracted via `page.getText("dict")`. While this contains a lot of information about each text span, it is still not complete, e.g.

* There is currently no way to determine whether extracted text is actually visible in the original. It may be covered by other objects like images (i.e. be in "background"), or be attributed as "hidden" - we wouldn't know this. Rewritten text will always be visible afterwards.
* There is currently no way to tell whether text is under control of some opacity (transparency) instruction. The only way to "simulate" this is via a semi-manual intervention along the line ``if fontsize > some threshold, then opacity=0.2``.
* TODO: The precision of text extraction is critical foro successful execution. On rare occasions, inter-character spacing may be incorrectly computed by MuPDF. Words may be erroneously joined or, vice versa characters in a word may show misplaced gaps. Maybe this can be healed by choosing the more detailed extraction method `page.getText("rawdict")`.
* Another important, heavily used MuPDF utility function is invoked by `Page.cleanContents()`. It concatenates multiple `/Contents` objects, purifies their command syntax and snychronizes fonts actually **used** with fonts **named** in the `/Resources` page object.

## Usage
Follow this procedure to replace fonts in a given file ``input.pdf``

1. **_Run_** ``repl-fontnames.py input.pdf``. This will produce file ``input.pdf-fontnames.csv``.

2. **_Edit_** the produced CSV as decscribed above. It is required as input for the next step.

3. **_Run_** ``repl-font.py input.pdf``. This will read the PDF and CSV files and replace the specified font(s). The resulting PDF is saved as ``input-new.pdf``.
