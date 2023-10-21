# Under Construction

This contains one demo script currently, which examines the PDF catalog and
tries to resolve named destinations to pages.

We intend to make this available as a fitz.Document method.

Currently, invoke like this:

```python
import fitz
from find_names import resolve_names

doc=fitz.open("pymupdf.pdf")
resolved_name = resolve_names(doc)

resolved_name["chapter.1"]
{'page': 6, 'to': (72.0, 720.0), 'zoom': 0}
```