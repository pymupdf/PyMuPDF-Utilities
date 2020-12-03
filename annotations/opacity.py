import os
import time

import fitz

print(fitz.__doc__)
doc = fitz.open()
page = doc.newPage()

annot1 = page.addCircleAnnot((50, 50, 100, 100))
annot1.setColors(fill=(1, 0, 0), stroke=(1, 0, 0))
annot1.setOpacity(2 / 3)
annot1.update(blend_mode="Multiply")

annot2 = page.addCircleAnnot((75, 75, 125, 125))
annot2.setColors(fill=(0, 0, 1), stroke=(0, 0, 1))
annot2.setOpacity(1 / 3)
annot2.update(blend_mode="Multiply")
outfile = os.path.abspath(__file__).replace(".py", ".pdf")
doc.save(outfile, expand=True, pretty=True)
print("saved", outfile)
