import pymupdf
from deep_translator import GoogleTranslator

# Define color "white"
WHITE = pymupdf.pdfcolor["white"]

# This flag ensures that text will be dehyphenated after extraction.
textflags = pymupdf.TEXT_DEHYPHENATE

# Configure the desired translator
to_korean = GoogleTranslator(source="en", target="ko")

# Open the document
doc = pymupdf.open("orca-english.pdf")

# Define an Optional Content layer in the document named "Korean".
# Activate it by default.
ocg_xref = doc.add_ocg("Korean", on=True)

# Iterate over all pages
for page in doc:
    # Extract text grouped like lines in a paragraph.
    blocks = page.get_text("blocks", flags=textflags)

    # Every block of text is contained in a rectangle ("bbox")
    for block in blocks:
        bbox = block[:4]  # area containing the text
        text = block[4]  # the text of this block

        # Invoke the actual translation to deliver us a Korean string
        korean = to_korean.translate(text)

        # Cover the English text with a white rectangle.
        page.draw_rect(bbox, color=None, fill=WHITE, oc=ocg_xref)

        # Write the Korean text into the original rectangle
        page.insert_htmlbox(
            bbox, korean, css="* {font-family: sans-serif;}", oc=ocg_xref
        )

doc.subset_fonts()
doc.ez_save("orca-korean.pdf")
