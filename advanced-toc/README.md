# Handling of Table of Contents

Tables of Content - TOC - can be created for any PyMuPDF document type by method `doc.getToC(simple: bool = True/False)`. The new alias of this method if `get_toc`.

The method returns a Python list like this:

```python
>>> pprint(doc.get_toc(True))
[[1, 'Page 1 - level 1', 1],  # hierarchy level, title, page number
 [2, 'Page 2 - level 2', 2],
 [3, 'Page 3 - level 3', 3],
 [1, 'Page 4 - level 1', 4],
 [2, 'Page 5 - level 2', 5],
 [3, 'Page 6 - level 3', 6],
 [1, 'Page 7 - level 1', 7],
 [2, 'Page 8 - level 2', 8],
 [3, 'Page 9 - level 3', 9]]
>>> 
```
Respectively this:

```python
>>> pprint(doc.get_toc(False))
[[1,  # hierarchy level
  'Page 1 - level 1',  # title
  1,  # page number, followed by item details:
  {'collapse': True,
   'kind': 1,
   'page': 0,
   'to': Point(72.0, 36.0),
   'xref': 15,
   'zoom': 0.0}],
 [2,
  'Page 2 - level 2',
  2,
  {'collapse': True,
   'kind': 1,
   'page': 1,
   'to': Point(72.0, 36.0),
   'xref': 16,
   'zoom': 0.0}],
 [3,
  'Page 3 - level 3',
  3,
  {'kind': 1, 'page': 2, 'to': Point(72.0, 36.0), 'xref': 17, 'zoom': 0.0}],
 [1,
  'Page 4 - level 1',
  4,
  {'collapse': True,
   'kind': 1,
   'page': 3,
   'to': Point(72.0, 36.0),
   'xref': 18,
   'zoom': 0.0}],
 [2,
  'Page 5 - level 2',
  5,
  {'collapse': True,
   'kind': 1,
   'page': 4,
   'to': Point(72.0, 36.0),
   'xref': 19,
   'zoom': 0.0}],
 [3,
  'Page 6 - level 3',
  6,
  {'kind': 1, 'page': 5, 'to': Point(72.0, 36.0), 'xref': 20, 'zoom': 0.0}],
 [1,
  'Page 7 - level 1',
  7,
  {'collapse': True,
   'kind': 1,
   'page': 6,
   'to': Point(72.0, 36.0),
   'xref': 21,
   'zoom': 0.0}],
 [2,
  'Page 8 - level 2',
  8,
  {'collapse': True,
   'kind': 1,
   'page': 7,
   'to': Point(72.0, 36.0),
   'xref': 22,
   'zoom': 0.0}],
 [3,
  'Page 9 - level 3',
  9,
  {'kind': 1, 'page': 8, 'to': Point(72.0, 36.0), 'xref': 23, 'zoom': 0.0}]]
```

The second version provides an additional entry with more detail for each item.

> Please note that the items occur in the sequence as defined in the document. They are **_not sorted_**, specifically not by page number.

> Page numbers may be -1 to indicate that the item does not point to somewhere in the document. In that case the detail dictionary will tell, whether a different document, an internet resource or indeed nothing is the target.

# PDFs Support Additional Features
## (A) - Set the Complete TOC
In PDF documents, a list like a TOC can be used as argument to method `doc.setToC` / `doc.set_toc`. This will either **_completely replace_** any existing TOC or **_create a new one_**.

Both of the above formats are supported here. For items with the simple format, a default detail dictionary will be created internally.

The important thing to note is, that **_you can manipulate the TOC list_** to your liking before using the method. The following rules must be adhered to, however:

* The first item in the list must have a level of 1.
* The level of a successor item must either be (a) smaller, (b) the same, or (c) 1 larger than that of the previous item.
* Page numbers must be 1-based. The maximum value is the document's page count.

If you follow these rules, you can add or remove items, change titles, page numbers, page target points, and target types.

PDF viewers normally support collapsed or expanded views for the TOC.
In PyMuPDF you have the following options to support this:

* Use the `collapse` method parameter: `doc.set_toc(toc, collapse=n)`. This will collapse all items with a hierarchy level greater than `n`. The default is 1, so only top level items are initially shown. To show all items expanded, use 0 or `None` (or some crazily large integer).
* Use key `"collapse"` of the item detail dictionary. If set to `True`, items below this one are collapsed. In this case set the `collapse` **_parameter_** of the method to 0.

Advanced PDF viewers also support colored TOC views and more sophisticated text properties like bold and italics.

In PyMuPDF you can use the item detail dictionary to support this:
* set the `"color"` key to a PDF RGB color triple (red, green, blue) - each of the three entries is a float in range 0 to 1.
* set the `"bold"` key to `True` / `False`.
* set the `"italic"` key to `True` / `False`.

## (B) Manipulate Selected TOC Items

Replacing the complete TOC as offered by `doc.set_toc` may not always be desired. Large PDFs tend to also have large TOCs.

So if all you want is changing e.g. a few bookmark titles out of several hundred or even thousands of TOC items, then replacing the whole bunch may be a waste of disk space and / or processing time.

> For example, the Adobe manual has about 800 TOC items, the Pandas manual over 500 and the SWIG manual about 1240.

To modify a single item, use method `doc.set_toc_item`. All properties are available for change - please see the following call pattern:

```python
toc = doc.get_toc(False)  # recommended to always use this
doc.set_toc_item(idx,  # item index in above list
    dest_dict=dest,  # modified detail dict of item
    kind=int,  # link kind, only if dest_dict omitted
    pno=int,  # target page, only if dest_dict omitted
    uri=str,  # URI, only if dest_dict omitted
    title=str,  # new title
    to=point,  # target point, only if dest_dict omitted
    filename=str,  # only if dest_dict omitted
    zoom=float,  # zoom factor, only if dest_dict omitted
)
```
Here is a "live" script that reads the PDF file in this folder and does the following:
1. expand all items
2. set level 1 to red & bold
3. set level 2 to blue & italic
4. set other levels to green

```python
import fitz

doc = fitz.open("example.pdf")
toc = doc.get_toc(False)
for i, item in enumerate(toc):
    lvl, title, pno, ddict = item
    ddict["collapse"] = False
    if lvl == 1:
        ddict["color"] = (1, 0, 0)
        ddict["bold"] = True
        ddict["italic"] = False
    elif lvl == 2:
        ddict["color"] = (0, 0, 1)
        ddict["bold"] = False
        ddict["italic"] = True
    else:
        ddict["color"] = (0, 1, 0)
        ddict["bold"] = ddict["italic"] = False
    doc.set_toc_item(i, dest_dict=ddict)

doc.save("colored-toc.pdf")
```

This is how the result looks like:

![screen](colored-toc.png)


Obviously in this case, because we in fact changed every single item, the same result could have been achieved by applying the changes directly to the ``toc`` list and then setting that as the new TOC.

There are however more or less subtle differences in favor of this function:
* `doc.set_toc_item()` reuses the old xref number, whereas `doc.set_toc()` acquires new xref numbers (currently - we may be changing this going forward). The old ones must be regained using garbage option of 2 or more on `save()`.
* If an exception occurs within underlying MuPDF functions, `doc.set_toc_item()` is better recoverable because of its granular approach (changes only one xref at a time). `doc.set_toc()` consists of two internal steps, both of which are bulk changes to all xref numbers dealing with TOC storage, making it impossible to roll back except by discarding all changes to the PDF completely.

Other advantages of using `doc.set_toc_item()`:

* If a PDF is signed, only incremental changes are possible without invalidating the signature. Also, incremental saves are fast, but always increase the file size. So you should generally be interested in small overall changed data volumes in order to minimize those increments. This makes the method an ideal candidate for small changes to the TOC.

There are disadvantages, too:
* You cannot change the overall TOC structure with `doc.set_toc_item()` - only the content of each item. You cannot add items, or change hierarchy levels, or positions inside the TOC list.
* You cannot delete TOC items either ... but there is method `doc.del_toc_item(idx)`, which removes an item's title string and sets the item's target to empty.
