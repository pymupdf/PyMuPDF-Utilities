import os
import time

import fitz

print(fitz.__doc__)
doc = fitz.open()
page = doc.new_page()

annot1 = page.add_circle_annot((50, 50, 100, 100))
annot1.set_colors(fill=(1, 0, 0), stroke=(1, 0, 0))
annot1.set_opacity(2 / 3)
annot1.update(blend_mode="Multiply")

annot2 = page.add_circle_annot((75, 75, 125, 125))
annot2.set_colors(fill=(0, 0, 1), stroke=(0, 0, 1))
annot2.set_opacity(1 / 3)
annot2.update(blend_mode="Multiply")
outfile = os.path.abspath(__file__).replace(".py", ".pdf")
doc.save(outfile, expand=True, pretty=True)
print("saved", outfile)
