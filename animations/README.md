This folder contains a few scripts which may best be characterized as "fun" or "entertainment" ... using PyMuPDF of course.

They all work following the same basic approach:

1. Draw or write something on an empty page of a new PDF
2. Convert the page to an image
3. Show this image in a GUI (using PySimpleGUI)
4. Destroy image, page and PDF document
5. Modify some parameters
6. Start over with step 1 above in an endless loop.

Because of the excellent performance of PyMuPDF (😉), this process is fast enough to be shown like a little video clip - mostly achieving more than 100 frames per second.

Scripts `morph-demo1.py`, `morph-demo2.py` and `morph-demo3.py` show the effect of morphing a text box given some fixpoint.

Scripts `quad-show2.py` and `quad-show2.py` simply draw quadrilaterals to demonstrate what happens when their corners are modified following certain patterns.
