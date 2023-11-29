# Example for PyMuPDF Reporting

This script creates an invoice with a layout involving fairly complex HTML definitions.

The single invoice items are contained in an SQL database (sqlite).

Points of interest:

* Company logo top-left on every page - defined as being part of the report header
* The report header also includes a small constant table top-right
* On page 1 only, there is a "prolog" section cotaining some introductory explanations.
    - The HTML skeleton contains 4 variables to be filled with actual data
* We are giving the last report row an extra backgound color
* The function providing item data also computes an overall invoice total and appends
