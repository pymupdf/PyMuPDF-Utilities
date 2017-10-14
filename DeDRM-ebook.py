from __future__ import print_function
import pyautogui
import fitz
import time
"""
@created: 2017-06-05 18:00:00

@author: (c) 2017 Jorj X. McKie

Create a readable PDF copy of any (potentially DRM protected) pageable content
-------------------------------------------------------------------------------

Dependencies:
-------------
PyMuPDF v1.11.0+, pyautogui


License:
--------
GNU GPL V3+

Description
------------
Page through the display of an e-book and store each page as a full page image
in a new PDF.

The page image grabbing and paging through the book is done with pyautogui.
"""
if str == bytes:
    getResponse = raw_input
else:
    getResponse = input


# This is the rectangle copied. You should adjust it until it fits!
# PyAutoGUI region parameter expects
#      (left, top, width, height)
bbox = (70, 100, 850-70, 1008-100)     # the screen area to grab

width = bbox[2] / 2.         # determines PDF page width
height = bbox[3] / 2.        # ... and page height

# If you need to test your bbox image, answer "y"
answer = getResponse("need a test picture? y/n >")
if answer == "y":
    print("activate the e-book window NOW (5 sec) ...")
    time.sleep(5)
    print("grabbing picture now")
    img = pyautogui.screenshot(region = bbox)
    img.show()
    raise SystemExit

print("activate / click the e-book window NOW (5 sec) ...")
time.sleep(5)    
print("starting process now")
print("Hands off! The e-book window needs focus all the time!")

doc = fitz.open()                      # new empty PDF
old_samples = None                     # used to check end of e-book
i = 0
while 1:
    img = pyautogui.screenshot(region = bbox)  # get the displayed e-book page
    samples = img.tobytes()            # copy for PyMuPDF
    if samples == old_samples:         # if no change: assume end of book
        print("end of book encountered ... finishing")
        break
    old_samples = samples              # store this page image
    pix = fitz.Pixmap(fitz.csGRAY, img.size[0], img.size[1], samples, 0)
    page = doc.newPage(-1, width = width, height = height)
    page.insertImage(page.rect, pixmap = pix)    # insert screen print as image
    pyautogui.hotkey("pagedown")       # next page in e-book reader
    time.sleep(2)                      # allow for slow response time
    i += 1

# new PDF now contains page images as if scanned-in.
doc.save("ebook.pdf", deflate=True)     # save our PDF copy with compression
print(i, "pages saved.")
    
