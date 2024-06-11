import pymupdf

# import helper functions from pymupdf4llm
from pymupdf4llm.helpers.get_text_lines import get_text_lines
from pymupdf4llm.helpers.multi_column import column_boxes


def get_page_text(page):
    """Extract plain text respecting any page columns."""
    alltext = ""  # result text goes in here

    # ensure automatic resolution of hyphenated words
    flags = pymupdf.TEXT_DEHYPHENATE

    # make a TextPage object to ensure optimum performance
    tp = page.get_textpage(flags=flags)

    # identify text blocks that respect page columns
    text_blocks = column_boxes(page, textpage=tp)

    # separately extract, then join text per column block
    for block in text_blocks:
        text = get_text_lines(page, textpage=tp, clip=block)
        alltext += text

    # return text of the page
    return alltext


if __name__ == "__main__":
    """When using the script as a CLI program."""
    import pathlib
    import sys

    filename = sys.argv[1]

    doc = pymupdf.open(filename)
    alltext = ""
    for page in doc:
        alltext += chr(12) + get_page_text(page)

    # output document text as one string
    pathlib.Path(f"{doc.name}-plain.txt").write_bytes(alltext.encode())
