import fitz

"""
This marks a longer, unique sentence on the page.
The parameters 'start', 'stop' and 'clip' are fully computed from the
returned hit rectangles.
"""
doc = fitz.open("search.pdf")
page = doc[0]

# Search for this text. It is show with hyphens on the page, which we can
# simply delete for our search. Line breaks can be handled like spaces.
text1 = (
    "Erklären ließe sich die Veränderung, wenn Beteigeuze einen",
    "Materieauswurf ins All geschleudert hat, der einen Teil",
    "der Strahlung abfängt, meinen die Forscher der",
    "Europäischen Südsternwarte ESO.",
)

rl = page.search_for(
    " ".join(text1),  # reconstruct full sentence for searching
)

# You should check success here!
start = rl[0].tl  # top-left of first rectangle
stop = rl[-1].br  # bottom-right of last rectangle
clip = fitz.Rect()  # build clip as union of the hit rectangles
for r in rl:
    clip |= r

page.add_highlight_annot(
    start=start,
    stop=stop,
    clip=clip,
)

doc.save(__file__.replace(".py", ".pdf"), garbage=3, deflate=True)
