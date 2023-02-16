"""
Utility
--------
This demo script show how to extract key-value pairs from a page with a
"predictable" layout, as it can be found in invoices and other formalized
documents.

In such cases, a text extraction based on "words" leads to results that
are both, simple and fast and avoid using regular expressions.

The example analyzes an invoice and extracts the date, invoice number, and
various amounts.

Because of the sort, correct values for each keyword will be found if the
value's boundary box bottom is not higher than that of the keyword.
So it could just as well be on the next line. The only condition is, that
no other text exists in between.

Please note that the code works unchanged also for other supported document
types, such as XPS or EPUB, etc.
"""

import fitz

doc = fitz.open("invoice-simple.pdf")  # example document
page = doc[0]  # first page
words = page.get_text("words", sort=True)  # extract sorted words

for i, word in enumerate(words):
    # information items will be found prefixed with their "key"
    text = word[4]
    if text == "DATE:":  # the following word will be the date!
        date = words[i + 1][4]
        print("Invoice date:", date)
    elif text == "Subtotal":
        subtotal = words[i + 1][4]
        print("Subtotal:", subtotal)
    elif text == "Tax":
        tax = words[i + 1][4]
        print("Tax:", tax)
    elif text == "INVOICE":
        inv_number = words[i + 2][4]  # skip the "#" sign
        print("Invoice number:", inv_number)
    elif text == "BALANCE":
        balance = words[i + 2][4]  # skip the word "DUE"
        print("Balance due:", balance)
