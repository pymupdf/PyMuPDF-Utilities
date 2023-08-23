## Breaking News: PyMuPDF's Table Support Starting with Version 1.23.0!
Starting with its version 1.23.0, PyMuPDF offers complete integrated support for identifying tables on document pages and extracting their content.

Just use the new [Page](https://pymupdf.readthedocs.io/en/latest/page.html) method [find_tables()]((https://pymupdf.readthedocs.io/en/latest/page.html#Page.find_tables)) to obtain an object that contains all detected tables on the page in a list.

You can iterate over these table objects to find details about their headers, table cells and their content. A growing number of example scripts shows how to do this and how to pass the extracted information downstream to pandas Dataframes and Excel, CSV or JSON files.

The following examples have been collected starting as of 2023-08-20:

* `find_tables.ipynb` (Jupyter notebook) reads a 1-page PDF with Chinese text and two tables.
* `join-tables.ipynb` (Jupyter notebook) reads a multi-page PDF and joins the parts of a table that has been fragmented across these pages.
* `compare-xps-pdf.ipynb` (Jupyter notebook) confirms support of PyMuPDF's table feature for general document (comparison XPS vs. PDF).
