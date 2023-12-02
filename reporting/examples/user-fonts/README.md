# Example for PyMuPDF Reporting: Using User Fonts

This script is a duplicate of another example in this folder: please see the [Film Festival](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/reporting/examples/filmfestival-2tables) script.

The only purpose here is to explain how a user-supplied font may be integrated in the reporting system.

As mentioned before, this happens via styling (CSS) instructions.

## Case: Use the DejaVu Sans Condensed Font

Assuming we want to use the fonts from the DejaVu Sans Condensed, we define the following CSS styling (see lines 58 - 63 in [dejavu.py](https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/reporting/examples/user-fonts/dejavu.py)):

```python
css = '@font-face {font-family: myfont; src: url("DejaVuSansCondensed.ttf");} '
css += '@font-face {font-family: myfont; src: url("DejaVuSansCondensed-Bold.ttf");font-weight:bold;} '
css += "* {font-family: myfont;}"

mediabox = fitz.paper_rect("A4")
report = Report(mediabox, css=css, archive=".")
```

These lines refer to two font files which must exist in a folder as specified in the `archive` parameter. Each variant of our font (regular, bold, italic or bold-italic) should be represented by its own file and referenced by the `url` parameter.

The final string `"* {...}"` requests to use font family "myfont" throughout the report.

On report creation, characters from the bold or regular font versions are automatically selected whenever a regular or bold character is encountered. As we have omitted any italic versions, italic characters will be taken from the regular font file.

As we can see, the report definition refers to the `css` variable. Therefore all report sections will use the same fonts - **_except_** when they use their own font definitions, respectively their own CSS instructions.

Nothing else in the report program has to be changed: The Story's layout engine will take care of the rest and compute appropriate table and field widths, page breaks etc.

## Case: Kenpixel
For further illustration purposes, script [kenpixel.py](https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/reporting/examples/user-fonts/kenpixel.py) does the same thing with the small and quite exotic font "kenpixel.ttf".

When looking at the resulting report files, both have similar sizes - although the DejaVu font files are very much larger than Kenpixel. This effect is achieved by PyMuPDF's in-built font subsetting engine which compresses fonts by eliminating all unused characters.