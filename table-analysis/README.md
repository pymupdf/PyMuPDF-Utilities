# Example scripts for table analysis

This folder contains example scripts for analyzing the contents of a table on a document page.

In PyMuPDF there is currently no support for directly detecting rectangles that surround tables. This in general is a highly complex task that requires advanced technologies like ML or AI.

For simpler cases, PyMuPDF does offer tools like text search and vector graphics analysis to come up with a bounding box wrapping a given table.

The scripts in this folder focus on analyzing table **_contents,_** once some wrapping rectangle is provided. The example documents are therefore chosen such that the first page contains the table in question and there exists a JSON file which specifies the table boundary box.

## Breaking News: PyMuPDF's Table Support Starting with Version 1.23.0!
Starting with its version 1.23.0, PyMuPDF offers complete integrated support for identifying tables on document pages and extracting their content.

Just use the new [Page](https://pymupdf.readthedocs.io/en/latest/page.html) method [find_tables()]((https://pymupdf.readthedocs.io/en/latest/page.html#Page.find_tables)) to obtain an object that contains all detected tables on the page in a list.

You can iterate over these table objects to find details about their headers, table cells and their content. A growing number of example scripts shows how to do this and how to pass the extracted information downstream to pandas Dataframes and Excel, CSV or JSON files.

The following examples have been collected starting as of 2023-08-20:

* `find_tables.ipynb` (Jupyter notebook) reads a 1-page PDF with Chinese text and two tables.
* `join-tables.ipynb` (Jupyter notebook) reads a multi-page PDF and joins the parts of a table that has been fragmented across these pages.
* `XPS-table.ipynb` (Jupyter notebook) confirms support of PyMuPDF's table feature for general document (comparison XPS vs. PDF).

## Example scripts
If running standalone, the example scripts accept the file name via CLI parameter and expect a same-named JSON file containing the bbox covering the table to be found on first page.

The scripts can also be imported. In that case, the `main` function can be invoked with page (`fitz.Page`) and table bbox as parameters. The bbox must fully cover the table (and nothing else), but it may be arbitrarily large otherwise.

The function `main` analyzes the table structure (columns and rows), extracts cell content and stores it in a pandas DataFrame. This data frame is then returned to the caller.

* `gridlines-to-pandas.py` table analysis: all cells are surrounded by grid lines.
* `span-analysis-to-pandas.py` table analysis: gaps exist between adjacent columns 
