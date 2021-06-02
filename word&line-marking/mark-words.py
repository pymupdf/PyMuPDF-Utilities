"""
@created: 2020-08-20 13:00:00

@author: Jorj X. McKie

@copyright: (c) 2020, Jorj X. McKie

@license: GNU AFFERO GPL V3 or later

Description
-----------
This script surrounds each "real" word with a rectangle annotation.

The goal is to catch "conventional" words only: meaning strings containing
alphabetic characters without punctuations (dots, commas, ...), digits,
special characters etc.

The approach is as follows:
1. Make a list of "technical" words of the page via page.get_text("words"), i.e.
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
import time
import fitz


def find_words(page, word_tuple, prefix="", suffix="", lower=True):
    """Make list of sub-rectangles which each contain contiguous alphabetic
    strings only.

    Args:
        word_tuple: an item of page.get_text("words")
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
    blocks = page.get_text("rawdict", clip=rect, flags=0)[  # restrict to word bbox
        "blocks"
    ]

    for block in blocks:
        for line in block["lines"]:
            if line["spans"] == []:
                continue
            r = fitz.Rect()  # start with an empty rectangle
            checkword = ""
            for span in line["spans"]:
                for char in span["chars"]:
                    # change the following to account for non-Latin
                    # alphabets, any exceptions, etc.
                    if char["c"].isalpha():  # alphabetic character?
                        r |= char["bbox"]  # extend current rectangle
                        checkword += char["c"]
                    else:  # non-alphabetic character detected
                        if take_this(checkword, prefix, suffix, lower):
                            rlist.append((r, checkword))  # append what we have so far
                        r = fitz.Rect()  # start over with empty rect
                        checkword = ""
            if take_this(checkword, prefix, suffix, lower):
                rlist.append((r, checkword))  # append any dangling rect
    return rlist


if __name__ == "__main__":
    doc = fitz.open("search.pdf")
    page = doc[0]
    time0 = time.perf_counter()
    # make a list of "technical" words
    wordlist = page.get_text("words")
    m = ("seife", "wissenschaft")  # only accept these full words
    for word_tuple in wordlist:
        """
        For performance reasons, be stingy with invoking find_words!
        Do as much pre-selection as is possible here, by skipping strings,
        which will definitely be no match.
        """
        text = word_tuple[4].lower()
        if not text.startswith(m):  # skip strings that we know cannot fit
            continue
        items = find_words(
            page,
            word_tuple,
            prefix="",  # restrict to this prefix
            suffix="",  # restrict to this suffix
            lower=True,  # comparisons ignore upper / lower case
        )  # get list of sub-rects and matching words
        for item in items:
            if item[0].is_empty:  # skip empty ones
                continue
            if not item[1].lower() in m:
                continue  # skip what does not exactly fit.
            annot = page.add_rect_annot(item[0])  # else surround the word with a thin
            annot.set_border(width=0.3)  # border (cosmetics)
            annot.update()

    time1 = time.perf_counter()
    print("Duration %g" % (time1 - time0))
    doc.save(__file__.replace(".py", ".pdf"), garbage=3, deflate=True)
