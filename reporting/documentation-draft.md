# PyMuPDF Documentation - Upfront

This is a non-final, heads-up documentation for PyMuPDF's new reporting feature.

## Introduction
The reporting feature is based on PyMuPDF's class `Story`.

Its goal is to **_radically simplify_** producing reports - especially standard reports - and put all the hassle and technical detail around defining headers and footers, tables and multi-column pages behind the curtain.

Nevertheless, for a better understanding of the following, reading the documentation about the `Story` class is recommended.

You should also read the the articles [How to Layout Articles Using PyMuPDF](https://artifex.com/blog/pymupdfs-new-story-feature-provides-advanced-pdf-layout-styling) and [The ‘Story’ Concept at Work](https://artifex.com/blog/how-to-layout-articles-using-pymupdfs-story-feature-part-2) on Artifex' blogging website.

This [presentation](https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/reporting/pymupdf-reporting.pdf) gives you a good 4-page impression.

## Defining a Report
### The Layout
Prereqisite for any report is the definition of its layout. Being based on PyMuPDF's `Story` class, this must happen using HTML source and optional styling using CSS.

These sources may be defined inside the report program or in separate files or any combination of these options.

It is also possible to build HTML source programmatically in the program itself and / or modify external sources.

It is however recommended to use external sources for easier maintenance and visual checks using some browser.

### Coding the Program
All support for the reporting feature is contained in one Python file `Reports.py`. This file can be find in the current folder and in each of the example solutions' sub-folders.

Access to the all reporting features is available via the import statement

```python
from Reports import Report, Table, Block, ImageBlock
```

After becoming an official part of PyMuPDF itself, change this import statement like so and you are done:

```python
from fitz.reports import Report, Table, Block, ImageBlock
```

----------

#### **Report**
Every report requires defining a `Report` object:

```python
report = Report(
    mediabox=None,
    margins=None,
    css=None,
    archive=None,
    font_families=None,
    )
```
* mediabox:  (required) a rectangle defining the page size. For example `fitz.paper_rect("A4")` (ISO A4), or `fitz.paper_rect("lettler-l")` (Letter landscape).

* margins:  (optional) 4 floats defining the desired margins (left, top, right, bottom) as distance from the respective border in points (1 inch = 72 points). If omitted, a value of 36 is substituted for all 4 items.

* css: (optional) a string containing any styling information to be used as default for this report.

* archive:  (optional) a PyMuPDF `Archive` object that points to any folders, ZIP or TAR objects that contain fonts or images required by the report. Please consult PyMuPDF's [documentation](https://pymupdf.readthedocs.io/en/latest/archive-class.html#archive) for details. If omitted, the folder of the script will be used as the default.

* font_families: (optional) a dictionary with _keys_ that each name a font-family and a font defined in pymupdf-fonts. This will automatically generate required CSS `@font-face` definitions and archive entries to support the font named as _value_. A specificaton `font_families={"sans-serif": "ubuntu", "serif": "ubuntu"}` will cause the "Ubuntu" font to be used globally for any text in the report. Please see [pymupdf-fonts](https://pypi.org/project/pymupdf-fonts/) for a list of available fonts in that package. The package must be installed in your Python for this parameter to work.

----------
#### **Block**
Most building blocks in your report will be a `Block`. This is true for header, footer, and normal text.

```python
header = Block(
    report=None,
    html=None,
    archive=None,
    css=None,
    story=None,
)
```

* report:  (mandatory) the name of the previously defined `Report`.

* html:  (string) the HTML source for the block. Either this parameter, or story (below) **_must_** be given.

* archive:  (optional) a PyMuPDF `Archive` pointing to fonts or images specific to this block. The report's archive will prefix this object - i.e. the result is a concatenation of the report archive and this one.

* css:  (string, optional) any styling information specific to this block. Default is the empty string. The report's CSS will be taken to prefix the value given here.

* story:  (optional) a PyMuPDF `Story` object. Exactly one of `html` and `story` **_must_** be provided. Use this parameter, if you have a prepared `Story` for whatever reason. This shouldn't be required often.

----------

#### **ImageBlock**
A company logo image is best provided by an `ImageBlock` because it allows more direct control to position it at desired places.

It however perfectly possible to specify images inside HTML used in any other block.

```python
logo = ImageBlock(
    report = None,
    url=None,
    archive=None,
    css=None,
    story=None,
    width=None,
    height=None,
)
```

Most parameters have the same meanings.

But care should be taken setting width and height. Both can be integers or strings. Please read the documentation about the HTML [`<img>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img) tag to learn details.

The import point is that you should be careful using both parameters, because it will scale the image in both dimensions - with a high probability to destroy the original aspect ratio.

Try to set **_either_** width **_or_** height, but not both. If you for instance want a logo to not exceed a square of 100 points, find out whether the image height is larger than its width and if so, set height=100 letting width default to `None`.

----------

#### **Table**

A table is an important - maybe the most imaportant - building block for reports. There are no invoices or financial statements without one or more tables.

At the same time, it is a more complex object, because a table regularly depends on data records in some database from where the single fields of each table row get their values.

It also must decided whether rows should receive special background colors (like alternativing between two different shades of gray), whether the top row should be repeated for every output segment.

```python
items = Table(
    report=None,
    html=None,
    story=None,
    fetch_rows=None,
    top_row=None,
    last_row_bg=None,
    archive=None,
    css=None,
    alternating_bg=None,
)
```

Parameters `report`, `html`, `story`, `archive` and `css` have the same meanings as before. The other parameters are specific for Tables:

* top_row:  (optional, str) the name (`id` tag) of the variable in the HTML that identifies the table that should be repeated on subsequent pages. A typical example would be `<tr id="toprow">`. For the default, no top-row repeat will take place.

* fetch_rows:  (optional, callable) a Python function that will deliver a list of data rows from which the Table object will create the report rows. In order to work, the HTML **_must_** contain a table row called **"template"** like this: `<tr id="template">`, and be followed by `<td>` tags that define variable names for each field contained in the items returned by the callable. For instance, if the callable returns data where some column is called `"amount"`, then there must exist a tag `<td id="amount"></td>` inside the row definition of "template".

    > It is perfectly possible to provide HTML source that already contains everything to be reported. In that case, this callable and some other parameters are not required.

    > The same is true if a `Story` object is provided instead of some HTML source.
    
    > Except for repeating any specified top row, the Table object will not modify anything of the story of the html source, if this parameter is omitted.

* last_row_bg:  (optional, str) a HTML color to specify the background of the last table row. Typically use to emphaize a table total. Ignored if `fetch_rows` is `None`.

* alternating_bg: (optional, list/str) one or more HTML colors to use as background for each table row. The default background is white. Ignored if `fetch_rows` is `None`.

----------

#### **Defining the `fetch_rows` callable**

This must be a Python function with no parameters. It must return the row data for writing the complete report. In other words this must be a list of lists, where the first sub-list contains the names ("id") of the data that follow. Where the data come from is completely at the discretion of the callable: anything that can be accessed using Python can be used as a data store.

If for instance data records with three fields "description", "count", "amount" are read from a database and the report expects them plus the product (called "total") of count and amount, the function would return a list like the following (the last column containing computed values).
```python
[
    ["description", "count", "ammount", "total"],
    ["coffee", 10, 15, 150],
    ["table", 1, 250, 250],
    ["chair", 4, 50, 200],
    ["", "", "Total", 600]
]
```
The corresponding table definition must be this:
```html
<tr id="template">
    <td id="description"></td>
    <td id="count"></td>
    <td id="amount"></td>
    <td id="total"></td>
</tr>
```
