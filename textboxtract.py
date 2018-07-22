"""
Script showing how to select only text that is contained in a given rectangle
on a page.

We use the page method 'getTextWords()' which delivers a list of all words.
Every item contains the word's rectangle (given by its coordinates, not as a
fitz.Rect in this case).
From this list we subselect words positioned in the given rectangle (or are at
least partially contained).
We sort this sublist by ascending y-ccordinate, and then by ascending x value.
Each original line of the rectangle is then reconstructed using the itertools
'groupby' function.
"""
from operator import itemgetter 
from itertools import groupby
import fitz
doc = fitz.open("<some.file>")     # any supported document type
page = doc[pno]                    # we want text from this page

"""
--------------------------------------------------------------------------------
Identify the rectangle. We use the text search function here. The two
search strings are chosen to be unique, to make our case work.
The two returned rectangle lists both have only one item.
--------------------------------------------------------------------------------
"""
rl1 = page.searchFor("Die Altersübereinstimmung") # rect list one
rl2 = page.searchFor("Bombardement durch.")       # rect list two
rect = rl1[0] | rl2[0]       # union rectangle
# Now we have the rectangle ----------------------------------------------------

"""
Get all words on page in a list of lists. Each word is represented by:
[x0, y0, x1, y1, word, bno, lno, wno]
The first 4 entries are the word's rectangle coordinates, the last 3 are just
technical info (block number, line number, word number).
"""
words = page.getTextWords()
# We subselect from above list.

# Case 1: select the words fully contained in rect
#-------------------------------------------------------------------------------
mywords = [w for w in words if fitz.Rect(w[:4]) in rect]
mywords.sort(key = itemgetter(3, 0))
group = groupby(mywords, key = itemgetter(3))
print("Select the words strictly contained in rectangle")
print("------------------------------------------------")
for y, gwords in group:
    print(" ".join(w[4] for w in gwords))

# Case 2: select words partially contained in rect
#-------------------------------------------------------------------------------
mywords = [w for w in words if fitz.Rect(w[:4]).intersects(rect)]
mywords.sort(key = itemgetter(3, 0))
group = groupby(mywords, key = itemgetter(3))
print("\nSelect the words intersecting the rectangle")
print("-------------------------------------------")
for y, gwords in group:
    print(" ".join(w[4] for w in gwords))
