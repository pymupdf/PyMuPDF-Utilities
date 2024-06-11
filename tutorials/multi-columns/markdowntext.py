"""
Convert document to Markdown text.

Execute as "python markdowntext.py input.pdf"

The output will be a file named "input.pdf-markdown.md"
"""

import pymupdf4llm
import pathlib
import sys


filename = sys.argv[1]
md_text = pymupdf4llm.to_markdown(filename)

# output document markdown text as one string
pathlib.Path(f"{filename}-markdown.md").write_bytes(md_text.encode())
