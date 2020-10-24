# Extracting Text from within a Rectangle
Extracting text from within specific rectangular areas of a document page is frequently required.

In PyMuPDF, you can select from several options to achieve this. All methods are applicable to all document types support by MuPDF - not only PDF. Choose the right method from the following list:

## 1. `Page.getTextbox(rect)`
Returns text contained in the rectangle 'rect'. Text appears in the sequence as coded in the document. So it may not adhere to an appropriate reading sequence. Inclusion of text is decided by character. So words may appear mutilated. Line breaks may be present, but one final line break will be omitted. See the example script `textbox-extract-2.py` in this folder.

----------

## 2. `Page.getText("text", clip=rect)`
This is one of the old, standard extraction methods. The `clip` parameter is new and was introduced in version 1.17.7. If `clip`is set, the result looks like the previous method's output, except that there always is a final line break.

----------

## 3. `Page.getText("words")`
This is also an old, standard extraction method. The method delivers a list of tuples, which each represent one string without spaces (called a "word") - together with its position. Each tuple looks like this: `(x0, y0, x1, y1, "string", blocknumber, linenumber, wordnumber)`. The first 4 items are the coordinates of the bbox that surround "string". The last 3 items are the integers number of block on page, number of line in a block, number of word in a line.

You have to write a script which selects the words **_contained in_** (or **_intersecting_**) the given rectangle by using the bbox coordinates, then sort the result, and then glue words together again that belong to the same line.

This approach can cope with documents where text is not stored in desired reading sequence: you will probably sort each string vertically and then horizontally. You may also find a way to put words in the same line even if their vertical coordinates differ by some threshold.

The script `textbox-extract-1.py` is an example for such a script. It also implements two word **selection alternatives:** one with only accepting **_fully contained_** words, and a second one including **_intersecting words_**.

----------

## Notes
This folder contains an example file `search.pdf` with one page and an annotation which shows the area to select from. The TOFU symbol in the outputs further down represents the big black triangle whose character bbox intersects the selection rectangle.

![screen](search.png)

### Output of `textbox-extract-1.py`
This script is based on `Page.getText("words")`. Words are selected in two ways: (1) whether they are fully contained in the given rectangle, or (2) whether their bbox has a non-empty intersection with it. Look at the above picture to compare these effects. The bottom vertical coordinates `y1` of the words are **_rounded_** to cope with any artifacts that may be caused by e.g. font changes or similar things.
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
This is based on `Page.getTextbox(rect)`. This obviously is a lot simpler and may be sufficient if you have no problem with the reading sequence and if you are able to position your rectangle in a way that does not cut through words.

It would also be the typical to verify what has been identified by a previous `Page.searchFor()`.
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
