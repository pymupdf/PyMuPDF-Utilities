# Example for PyMuPDF Reporting

This script creates a table from items in a CSV file.

Notes of interest:

* Table rows contain images that are stored in a ZIP file. The report generator "understands" field text that is prefixed with the string "|img|" and interprets it as a file name.
* Three alternating row background colors.