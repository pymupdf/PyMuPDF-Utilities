# Example for PyMuPDF Reporting

This script creates a report about a fictitious film festival.

It extracts data from an SQL database (sqlite3). The database contains two tables:
* **films** - columns: **title**, **director**, **year**
* **actors** - columns: **name**, **film**

Two tabular reports are created in one common PDF.
1. Table 1 lists all films and names all actors being cast.
2. Table 2 lists all actors together with all the films where they have been cast.

Noteworthy details:
* Demonstrate how to use fonts from the [pymupdf-fonts](https://pypi.org/project/pymupdf-fonts/) package.
* Demonstrate how to **combine multiple report sections** (here: two table sections) in one report.
* **Automatic layout:** major layout changes **without coding effort**, like
    - page size (Letter, ISO A4) or paper format (portrait, landscape)
    - number of columns per page
    - page breaks between report sections
* Appearance changes, like text colors or fonts just by modifying HTML and styling (CSS) definitions.