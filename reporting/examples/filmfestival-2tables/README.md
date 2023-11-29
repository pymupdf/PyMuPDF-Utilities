# Example for PyMuPDF Reporting

This script creates a report about a fictitious film festival.

It extracts data from an SQL database (sqlite3). The database contains two tables:
* films
* actors

The **_films_** table has columns **title**, **director**, **year** and the **_actors_** table has columns **name** and **film** title.

Two tabular reports are created in one common PDF.
1. Report 1 lists all films and names all actors being cast.
2. Report 2 lists all actors together with all the films where they have been cast.

The following are noteworthy details:
* Demonstrate how to use fonts from the [pymupdf-fonts](https://pypi.org/project/pymupdf-fonts/) package.
* Demonstrate how to combine multiple report sections (here: two table sections) in one report.
* Due to MuPDF's automatic layouting algorithm, major layout changes can be achieved without coding effort, like
    - choice of page size or paper format
    - choice of number of columns per page
* Influence on the layout can only be taken via the HTML and styling (CSS) definitions.