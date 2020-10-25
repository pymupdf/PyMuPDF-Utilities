"""
A PyMuPDF demo script for highlighting lines of text.

This requires 3 parameters:
- start: point where marking should start - upper bound
- stop: point where marking should stop - lower bound
- clip: rectangle for further limiting width of lines. This can be used when
        page text is organized in columns: then we must prevent inclusion of
        text portions from the wrong columns.

The parameters are optional in the following sense:
If 'start' is None, the top-left point of 'clip' is used.
If 'stop' is None, the bottom-right point of 'clip' is used.
If 'clip' is None, the page rectangle is used

Our example page has 3 text columns, and we luckily know that our text is
located in the left column. We also know unique text strings which help us
find the start and stop points.
"""
import fitz

doc = fitz.open("search.pdf")  # the document
page = doc[0]  # the page

# determine start point
rl = page.searchFor("im vorfeld solch ")  # use a unique string on the page
# we might want to check that len(rl) == 1 here
start = rl[0].tl  # top-left point

# determine stop point
rl = page.searchFor("stark aus.")  # use a unique string
# again, possibly check len(rl) == 1
stop = rl[0].br  # bottom-right point

# we need a clip rectangle, because the page has 3 text columns!
clip = page.rect  # start with page rectangle
width = clip.width  # take the width and limit it
clip.x1 = width * 0.35  # to about one third to get the left column

page.addHighlightAnnot(start=start, stop=stop, clip=clip)
# ------------------------------------------------------------
# underlining and strike-through work in the same way:
# ------------------------------------------------------------
# page.addUnderlineAnnot(start=start, stop=stop, clip=clip)
# page.addStrikeoutAnnot(start=start, stop=stop, clip=clip)
# page.addSquigglyAnnot(start=start, stop=stop, clip=clip)

doc.save(__file__.replace(".py", ".pdf"))
