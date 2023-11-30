import pathlib
import fitz
from Reports import Report, Block

report = Report(mediabox=fitz.paper_rect("a4-l"))

HTML = pathlib.Path("springer.html").read_bytes().decode()
textblock = Block(html=HTML, report=report)

report.sections = [[textblock, {"cols": 2, "format": "a4-l", "newpage": True}]]
report.run("output.pdf")
