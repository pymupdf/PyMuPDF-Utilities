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
doc = fitz.open("x.pdf")
page = doc[59]

# identify a rectangle, e.g. via text search function
# search strings are chosen to be unique in this case
rl1 = page.searchFor("Die Altersübereinstimmung")
rl2 = page.searchFor("Bombardement durch.")
rect = rl1[0] | rl2[0]       # union rectangle
words = page.getTextWords()  # get all words on the page

# select the words fully contained in rect
mywords = [w for w in words if fitz.Rect(w[:4]) in rect]
mywords.sort(key = itemgetter(3, 0))
group = groupby(mywords, key = itemgetter(3))
print("Select the words strictly contained in rectangle")
print("------------------------------------------------")
for y, gwords in group:
    print(" ".join(w[4] for w in gwords))

# select words partially contained in rect
mywords = [w for w in words if fitz.Rect(w[:4]).intersects(rect)]
mywords.sort(key = itemgetter(3, 0))
group = groupby(mywords, key = itemgetter(3))
print("\nSelect the words intersecting the rectangle")
print("-------------------------------------------")
for y, gwords in group:
    print(" ".join(w[4] for w in gwords))
