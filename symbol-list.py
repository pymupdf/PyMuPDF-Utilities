# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 08:34:06 2018

@author: Jorj
@license: GNU GPL 3.0+

Create a list of available symbols defined in shapes_and_symbols.py

This also demonstrates an example usage: how these symbols could be used
as bullet-point symbols in some text.

"""

import fitz
import shapes_and_symbols as sas

# list of available symbol functions and their descriptions
tlist = [
         (sas.arrow, "arrow"),
         (sas.caro, "caro"),
         (sas.clover, "clover"),
         (sas.diamond, "diamond"),
         (sas.dontenter, "do not enter"),
         (sas.frowney, "frowney"),
         (sas.hand, "hand"),
         (sas.heart, "heart"),
         (sas.pencil, "pencil"),
         (sas.smiley, "smiley"),
         ]

r = fitz.Rect(50, 50, 100, 100)        # first rect to contain a symbol
d = fitz.Rect(0, r.height + 10, 0, r.height + 10) # displacement to next ret
p = (15, -r.height * 0.2)              # starting point of explanation text
rlist = [r]                            # rectangle list

for i in range(1, len(tlist)):         # fill in all the rectangles
    rlist.append(rlist[i-1] + d)

doc = fitz.open()                      # create empty PDF
page = doc.newPage()                   # create an empty page
img = page.newShape()                  # start a Shape (canvas)

for i, r in enumerate(rlist):
    tlist[i][0](img, rlist[i])         # execute symbol creation
    img.insertText(rlist[i].br + p,    # insert description text
                   tlist[i][1], fontsize=r.height/1.2)

# store everything to the page's /Contents object
img.commit()

import os
scriptdir = os.path.dirname(__file__)
doc.save(os.path.join(scriptdir, "symbol-list.pdf"))  # save the PDF
