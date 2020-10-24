# Selecting and Marking Text
Prorammatically identifying and marking text is a frequent requirement. This folder is a collection of scripts that solve various tasks in this area.

## 1. Finding "real" words
Page method `getText("words")` delivers a list of tuples. Each tuples identifies a string without embedded spaces, together with its position on the page.

The method knows nothing about the meaning of these strings: it will identify just everything as a "word", that is surrounded spaces.

If you however are looking for occurrences of a certain word, you need a mechanism that strips off punctuation like commas or colons, maybe also numerical components or *"dashed"* combinations with other words.

Script `mark-words.py` aims to solve this problem: inside the strings of the tuples of `getText("words")` it will identify alphabetic substrings and calculate the respective subrectangles.

The demo script looks for and marks all "real" (punctuation-free) words on the example PDF page in this folder, which end with the letter "m". Please note the word circled red: the colon ":" has been detected and correctly separated from the end of the word.

Feel free to modify the selection mechanism: e.g. by using regular expressions.

![screen1](mark-words.jpg)

## 2. Highlighting Textlines
This is possible since some time using

`page.addHighlightAnnot(start=point1, stop=point2, clip=rect)`.

The idea is to mark text across multiple consecutive lines, where the start and the end points may be somewhere in the middle of their respective lines.

The short script `mark-lines.py` is an example for this.

For a satisfactory result, you must provide three information pieces. There is no general rule for how to do this. This example aims to help you find the solution for your situation.
1. The **_start point_**: We search for string **"im vorfeld solch"** and make sure that there is only one hit. the topl left corner of this rectangle is our start point.
2. The **_stop point_**: We similarly search for and ensure a unique string **"stark aus."** The bottom right point of the returned rectangle is our end point.
3. The **_clip rectangle_**: In many cases this may be left to default to the page rectangle. In our case however, text is organized in **_three columns_**, and we certainly want to limit line marking to one of them. Setting the clip rectangle width to a little more than one third of the page rectangle does the job.

![screen](mark-lines.png)

