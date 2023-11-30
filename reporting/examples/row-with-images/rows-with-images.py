import pathlib
import fitz
import zipfile
from Reports import Block, Table, Report, ImageBlock

# The following defines the overall report object
mediabox = fitz.paper_rect("a4")  # the only required parameter
report = Report(mediabox, font_families={"sans-serif": "ubuntu", "serif": "ubuntu"})

# Predefined HTML to define the header for all pages

HEADER = (
    """<h1 style="text-align:center;font-family: sans-serif;">Report Example</h1>"""
)
header = Block(html=HEADER, report=report)

FOOTER = """<h5 style="text-align:center;font-family: sans-serif;">Report Footer</h5>"""
footer = Block(html=FOOTER, report=report)
footer.make_story()

HTML = """
<style>
body {font-family: sans-serif;font-size: 14px;}
td, th {
    padding-left: 10px;
    padding-right: 10px;
}
</style>

<body>
<table>
<tr id="header" style="background-color: #aaceeb;">
    <th>Country</th>
    <th>Type</th>
    <th>Flag</th>
    <th>Since</th>
</tr>

<tr id="template">
    <td id="country"></td>
    <td id="member"></td>
    <td id="flag"></td>
    <td id="since"></td>
</tr>
</table>
</body>
"""

national_flags = zipfile.ZipFile("flags.zip")


def fetch_rows():
    table_data = pathlib.Path("items.csv").read_bytes().decode()
    data = [l.split(";") for l in table_data.splitlines()]
    return data


items = Table(
    report=report,
    html=HTML,
    top_row="header",
    fetch_rows=fetch_rows,
    archive=national_flags,
    alternating_bg=("#ccc", "#aaa", "#fff"),
)

report.sections = [
    [items, {"cols": 1, "format": "letter", "newpage": True}],
]  # set sections list
report.header = [header]
report.footer = [footer]

# This generates the report and saves it to the given path name.
report.run("output.pdf")
