# "TXT" Document Support

PyMuPDF supports files in plain text formats as a `Document`.

They can be opened as usual, text can be etracted and searched for, and pages can be rendered as Pixmaps and more.

You can use it for general text files, program sources, markdown documents and many more: ASCII, UTF-8 and UTF-16 are supported.

File extensions ".txt"  and ".text" are natively recognized. Files with other extensions can be opened via the `filetype` argument: `doc = fitz.open("myscript.py", filetype="txt")`.

TXT documents are "reflowable" so [doc.is_reflowable](https://pymupdf.readthedocs.io/en/latest/document.html#Document.is_reflowable) will return `True`, you can re-layout them via [doc.layout()](https://pymupdf.readthedocs.io/en/latest/document.html#Document.layout), or open them with the additional, layout-oriented options, namely a rectangle, width, height and font size.

Like with e-books (EPUB, MOBI, etc.), there is **_no fixed page size_** (dimension - width / height). At open time, the defaults `width=400`, `height=600` and `fontsize=11` will be used.

When extracting text details, a Courier-equivalent monospace font will be reported for unicodes from the extended Latin range. But consistently with the occurring characters, any language-compliant font names will also be shown for CJK, Hindi, Tamil, Thai etc.

> At least for Latin text. If however the text contains characters from the CJK unicode range, other fonts will autonamtically be considered, making things more complicated.

If only (extended) Latin characters occur (usually the case in program text), it is easy to predict the number of characters per line:

* Each character of the Courier font has a width of `0.6 * fontsize`.

* There exist left and right margins of `2 * fontsize` each. A character written in the left-most position will have a bbox where `x0 = 2 * fontsize`. The last character's bbox will end before start of the right margin, `x1 <= page.rect.width - 2 * fontsize`.

* The default page (width of 400 points, font size 11) therefore can contain up to 53 characters per line: `int((400 - 4 * 11) / (0.6 * 11))`.

* If you want to conveniently layout your program source (e.g. 80 characters per line), you could do the following
    - Page `width = (4 + 80 * 0.6) * 11`, which is 572.
    - Using an "A4" rectangle with a width of 595 points can contain up to 83 characters per line. "Letter" rectangles even yield up to 86 characters per line.
    - `doc = fitz.open("myscript.py", filetype="txt", rect=fitz.paper_rect("letter"))` should normally give you a layout with only a few "unintended" line breaks.

Other, rarely used document methods may receive more attention with TXT documents: [Document.make_bookmark()](https://pymupdf.readthedocs.io/en/latest/document.html#Document.make_bookmark) and [Document.find_bookmark()](https://pymupdf.readthedocs.io/en/latest/document.html#Document.find_bookmark).

While accessing pages, you may decide to re-layout the document, but you want to quickly find the current location afterwards again:

```python
bm = doc.make_bookmark()  # compute current position in document
doc.layout(width=612, height=792, fontsize=10)  # layout document
chapter, pno = doc.find_bookmark(bm)  # retrieve new location
```

Method `find_bookmark()` returns a location in `(chapter, pno)` style. TXT documents only have one chapter, so `chapter = 0`.

`bm` is an integer with a special internal structure - which must not be touched in any way.