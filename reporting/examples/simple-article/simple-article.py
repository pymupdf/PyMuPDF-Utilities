import pathlib
import fitz
from Reports import *

report = Report(mediabox=fitz.paper_rect("a4-l"))

HTML = pathlib.Path("springer.html").read_bytes().decode()
textblock = Block(html=HTML, report=report)

report.sections = [[textblock, Options(cols=2, format=fitz.Rect(0, 0, 400, 600), newpage=True)]]
report.run("output.pdf")
