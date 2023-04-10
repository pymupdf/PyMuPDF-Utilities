# Example scripts for table analysis

This folder contains example scripts for analyzing the contents of a table on a document page.

In PyMuPDF there is currently no support for directly detecting rectangles that surround tables. This in general is a highly complex task that requires advanced technologies like ML or AI.

For simpler cases, PyMuPDF does offer tools like text search and vector graphics analysis to come up with a bounding box wrapping a given table.

The scripts in this folder focus on analyzing table **_contents,_** once some wrapping rectangle is provided. The example documents are therefore chosen such that the first page contains the table in question and there exists a JSON file which specifies the table boundary box.

## Example scripts
If running standalone, the example scripts accept the file name via CLI parameter and expect a same-named JSON file containing the bbox covering the table to be found on first page.

The scripts can also be imported. In that case, the `main` function can be invoked with page (`fitz.Page`) and table bbox as parameters. The bbox must fully cover the table (and nothing else), but it may be arbitrarily large otherwise.

The function `main` analyzes the table structure (columns and rows), extracts cell content and stores it in a pandas DataFrame. This data frame is then returned to the caller.

* `gridlines-to-pandas.py` table analysis: all cells are surrounded by grid lines.
* `span-analysis-to-pandas.py` table analysis: gaps exist between adjacent columns 