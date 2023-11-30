import pathlib

import fitz

from Reports import Block, Report, Table

ITEMS = """
    <p><i>Percent "%" is city population as a percentage of the country, as of "Year".</i></p><p></p>
    <table>
    <tr id="toprow" style="background-color: #ff0;">
        <th >Country</th>
        <th >Capital</th>
        <th >Population</th>
        <th >%</th>
        <th >Year</th>
    </tr>
    <tr id="template">
        <td id="country"></td>
        <td id="capital"></td>
        <td id="population"></td>
        <td id="percent"></td>
        <td id="year"></td>
    </tr>
    </table>
"""

# define some styling for the table
CSS = """
body {
    font-family: sans-serif;
}
td[id="population"], td[id="percent"], td[id="year"] {
    text-align: right;
    padding-right: 2px;
}"""

HEADER = '<h1 style="text-align: center;">Capital Cities of the World</h1>'

mediabox = fitz.paper_rect("a3")  # page format
report = Report(
    mediabox,
    # use pymupdf-fonts to replace both, Helvetica and Times-Roman:
    font_families={"sans-serif": "notos", "serif": "notos"},
)

header = Block(html=HEADER, report=report)


def get_data():
    """Read data and prepare table rows."""
    item_data = pathlib.Path("national-capitals.csv").read_bytes().decode()

    # row zero must contain column id's in the html table definition
    rows = [["country", "capital", "population", "percent", "year"]]
    rows.extend([row.split(";") for row in item_data.splitlines()])
    return rows


items = Table(
    report=report,
    html=ITEMS,
    css=CSS,
    fetch_rows=get_data,  # provides the data
    top_row="toprow",  # name (id) of repeated top row
    alternating_bg=("#ddd", "#fff"),  # alternating row background colors
)

# compose the report from above sections
report.header = [header]  # appears on every page
report.sections = [
    [items, {"cols": 2, "format": "a3", "newpage": True}]
]  # 2 columns per page

# output the report
report.run("output.pdf")
