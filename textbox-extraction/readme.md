# Extracting Text from within a Rectangle
Extracting text from within specific rectangular areas of a document page is frequently required.

In PyMuPDF, you can select from several options to achieve this. All methods are applicable to all document types support by MuPDF - not only PDF. Choose the right method from the following list:

----------

## 1. `Page.get_text("words")`
This is an old, standard extraction method. The method delivers a list of tuples, which each represent one string without spaces (called a "word") - together with its position. Each tuple looks like this: `(x0, y0, x1, y1, "string", blocknumber, linenumber, wordnumber)`. The first 4 items are the coordinates of the bbox that surround "string". The last 3 items are block number on the page, line number in a block, word number in a line.

You have to write a script which selects the words **_contained in_** (or **_intersecting_**) the given rectangle by using the bbox coordinates, then sort the result, and then glue words together again that belong to the same line.

This approach can cope with documents where text is not stored in desired reading sequence: you will probably sort the word list by vertical and then by horizontal coordinates. You may also find a way to put words in the same line even if their vertical coordinates differ by some small threshold.

The script `textbox-extract-1.py` is an example for such a script. It also implements two word **selection alternatives:** one with only accepting **_fully contained_** words, and a second one including **_intersecting words_**.

----------

## 2. `Page.get_textbox(rect)`
Returns text contained in the rectangle 'rect'. Text appears in the sequence as coded in the document. So it may not be in a desirable reading sequence. Inclusion of text is decided by character and words may hence appear mutilated. Line breaks may be present, but one final line break will be omitted. See the example script `textbox-extract-2.py` in this folder.

----------

## 3. `Page.get_text("text", clip=rect)`
This is one of the old, standard extraction methods. The `clip` parameter is new and was introduced in version 1.17.7. If `clip` is not `None`, the result looks like the previous method's output, except that there always is a final line break.

----------

## Notes
This folder contains an example file `search.pdf` with one page and an annotation which shows the area to select from. The **_TOFU_** symbol in some of the outputs further down represents the big black triangle whose character bbox intersects the selection rectangle.

![screen](search.png)

### Output of `textbox-extract-1.py`
This script is based on `Page.get_text("words")`. Words are selected in two ways: (1) whether they are fully contained in the given rectangle, or (2) whether their bbox has a non-empty intersection with it. Look at the above picture to compare these effects. The bottom vertical coordinates `y1` of the words are **_rounded_** to cope with any artifacts that may be caused by e.g. font changes or similar things.
```
Select the words strictly contained in rectangle
------------------------------------------------
Wer eine perfekte
schaffen will, braucht
und Seife.
das schon länger und
diesbezüglich mit
aus. Unter
sie auf den
Guaran (E 412).

Select the words intersecting the rectangle
-------------------------------------------
Wer eine perfekte Seifenblase
schaffen will, braucht mehr

Wasser und Seife. Enthusiasten
sen das schon länger und tauschen
sich diesbezüglich mit Hilfe
Online-Wikis aus. Unter anderem
schwören sie auf den Lebensmittel-
zusatzstoff Guaran (E 412).
```

### Output of `textbox-extract-2.py`
This is based on `Page.get_textbox(rect)`. The selection is based on single characters: a character belongs to the party if its bbox intersects rect. Apart from this, text is selected as present in the document - including any spaces and line breaks, no reordering takes place.

This obviously is a lot simpler and may be sufficient if you have no issue with the reading sequence and properly positioning the selection rectangle.

It would also be the typical way to verify that the text found by some previous `Page.search_for()` really is what you have been looking for.
```

Wer eine perfekte Seife
schaffen will, braucht m
asser und Seife. Enthusia
n das schon länger und t
ch diesbezüglich mit Hilfe
nline-Wikis aus. Unter an
hwören sie auf den Lebe
satzstoff Guaran (E 412).
```
