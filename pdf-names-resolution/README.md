# Under Construction

This contains two demo script currently, which examine the PDF catalog and
resolve named destinations to pages.

We intend to make this available as a fitz.Document method.

Currently, invoke like this:

## Alternative 1: `find_names.py`
This version works for both, the ca´lassic and the rebased architecture of PyMuPDF.
However, the solution is not complete yet: there are cases, where names are not detected completely.
```python
import fitz
from find_names import resolve_names

doc=fitz.open("pymupdf.pdf")
resolved_name = resolve_names(doc)

resolved_name["chapter.1"]
{'page': 6, 'to': (72.0, 720.0), 'zoom': 0}
```

## Alternative 2: `list_names.py`

This version shuld cover all cases for encoding named destinations - in contrast to Alternative 1.
It can only be used with the rebased version of PyMuPDF. Example:
```python
In [1]: import fitz_new as fitz
In [2]: from list_names import resolve_names
In [3]: doc=fitz.open("pymupdf.pdf")
In [4]: resolved_name=resolve_names(doc)
In [7]: resolved_name["chapter.1"]
Out[7]: {'page': 6, 'to': (72.0, 720.0), 'zoom': 0.0}
```