"""
@created: 2020-08-20 13:00:00

@author: Jorj X. McKie

@copyright: (c) 2020, Jorj X. McKie

@license: GNU GPL 3.0 or later

Description
-----------
This script surrounds each "real" word with a rectangle annotation.

The goal is to catch "conventional" words only: meaning strings containing
alphabetic characters without punctuations (dots, commas, ...), digits,
special characters etc.

The approach is as follows:
1. Make a list of "technical" words of the page via page.getText("words"), i.e.
   strings without spaces.
2. Inspect each list item and compute a list of sub-rectangles surrounding
   strings of alphabetic characters. If selection criteria (prefix / suffix)
   are given, discard non-matching sub-rectangles.
3. Return list of sub-rectangles.

There are a number of ways to down-select the words to consider:
- Specify parameters 'prefix and / or 'suffix'. Then only words satisfying the
  respective condition(s) will be considered. If specifying both, then the
  conditions are combined like with an OR.
- Specify parameter 'lower' to True or False. If False, then only words with a
  correct casing in prefix / suffix will be considered.
- You are certainly free to extend or replace this logic, e.g. by using regular
  expressions.

Performance considerations
--------------------------
Every execution of function 'find_words' creates and destroys the page's
TextPage. Hence, to improve performance, **prevent** executing it. In many
cases it should be possible to decide beforehand, whether a 'word_tuple' is
a possible candidate at all.

Dependencies
------------
PyMuPDF v1.18.0
"""
import fitz


def find_words(page, word_tuple, prefix="", suffix="", lower=True):
    """Make list of sub-rectangles which each contain contiguous alphabetic
    strings only.

    Args:
        word_tuple: an item of page.getText("words")
        prefix: select, if starting like this
        suffix: select, if ending like this
        lower: ignore case - increases hit rate.
    """

    def take_this(checkword, prefix, suffix, lower):
        if not prefix and not suffix:
            return True
        if lower == True:
            checkword = checkword.lower()
        if prefix and checkword.startswith(prefix):
            return True
        if suffix and checkword.endswith(suffix):
            return True
        return False

    rlist = []  # this will be returned
    rect = fitz.Rect(word_tuple[:4])  # this is the word bbox

    # make dict of character details
    blocks = page.getText("rawdict", clip=rect, flags=0)[  # restrict to word bbox
        "blocks"
    ]

    for block in blocks:
        for line in block["lines"]:
            for span in line["spans"]:
                r = fitz.Rect()  # start with an empty rectangle
                checkword = ""
                for char in span["chars"]:
                    # change the following to account for non-Latin
                    # alphabets, any exceptions, etc.
                    if char["c"].isalpha():  # alphabetic character?
                        r |= char["bbox"]  # extend current rectangle
                        checkword += char["c"]
                    else:  # non-alphabetic character detected
                        if take_this(checkword, prefix, suffix, lower):
                            rlist.append(r)  # append what we have so far
                        r = fitz.Rect()  # start over with empty rect
                        checkword = ""
                if take_this(checkword, prefix, suffix, lower):
                    rlist.append(r)  # append any dangling rect
    return rlist


if __name__ == "__main__":
    doc = fitz.open("search.pdf")
    page = doc[0]

    # make a list of "technical" words
    wordlist = page.getText("words")

    for word_tuple in wordlist:
        """
        For performance reasons, be stingy with invoking find_words!
        Insert any pre-selection here by e.g. pre-checking the string in
        word_tuple (word_tuple[4]).
        """
        text = word_tuple[4].lower()
        if not "m" in text:  # skip strings which cannot be correct
            continue
        rlist = find_words(
            page, word_tuple, prefix="", suffix="m", lower=True
        )  # get list of sub-rects
        for rect in rlist:
            if rect.isEmpty:  # skip empty ones
                continue
            annot = page.addRectAnnot(rect)  # else surround the word with a thin
            annot.setBorder(width=0.3)  # border (cosmetics)
            annot.update()

    doc.save(__file__.replace(".py", ".pdf"), garbage=3, deflate=True)
