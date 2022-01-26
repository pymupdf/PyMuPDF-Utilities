# Replacing an Image in a PDF

Occasionally it is desireable to replace an image by another one. Reasons may include:

* higher or lower resolution
* different colorspace (grayscale instead of colored) or alpha value
* etc.

The example script in this folder makes this possible.

The new image will be displayed  exactly like the old one. This includes any optional content conditions, image rotation and being in foreground or background.

The demo script `replacer.py` replaces the PNG background image on page 1 by its JPG equivalent, which is 20% of the original's size only.

The demo script `remover.py` replaces the PNG image by a small empty, fully transparent pixmap. The effect is **_like_** removing the image.

## Replacement Approach

* Get to know the original's xref.
* Clean page `/Contents` so that only one such exists.
* Insert new image on the page - somewhere: location irrelevant.
* Take new image's xref and duplicate it under the old xref number.
* Remove the new created `/Contents` object created by the image insertion.

## Comparing with Redaction Annotations

An image can be removed using redaction annotations. Its vacant bbox can then be filled with any image. This approach may therefore lead to a similar result as the one presented here. The following table compares the two options:

| Citeria | Redaction | XREF copy |
|---------|-----------|-------------------|
| **Specificity** | Removes **everything** in the bbox - which may be more than you wanted.| Nothing else is touched.|
| **Visibility** | Original image visibility is unknown, so you must decide: foreground or background.| No change.|
| **Flexibility** | No restrictions for new image.| Page will use same command for displaying new image. May or may not look awkward if e.g. different dimensions.|
| **Locality** | Affects **only the current page.**| Image will be relaced **_globally:_** all other pages will also show the new image.
| **Image removal** | Possible by design, but see side effects above.| Using a new image with 100% transparency and arbitrary dimensions will do a similar, but **_not the same_** job.|

## Notes on Image Removal
When removing an image **_via redactions,_** MuPDF locates the respective display command in the current page's `/Contents` and removes it. The image itself is not removed and may still be visible on other pages.

> **Note 1:** If an image is shown by one page only, it will also be completely removed on saves with garbage collection.

> **Note 2:** Using a "hacky" approach, a similar result is also achievable using PyMuPDF. If global removal of an image is no problem, the approach presented here should however be preferred.

## Announcment for Version 1.19.5
The new version will facilitate this process with a new method `Document.xref_copy()`. This will obsolete the respective function ``replace_object()`` in the example scripts.