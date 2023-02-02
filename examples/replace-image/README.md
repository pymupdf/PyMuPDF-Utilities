# Replacing an Image in a PDF


----------

> Note: The features described here are now (version 1.21.1) **_official methods_** of PyMuPDF's `Page` class, please consult the documentation [here](https://pymupdf.readthedocs.io/en/latest/page.html#Page.replace_image) and [here](https://pymupdf.readthedocs.io/en/latest/page.html#Page.delete_image).

----------

Occasionally it is desireable to replace an image by another one. Reasons may include:

* switch to an image version with higher or lower resolution
* different colorspace (grayscale instead of colored) or alpha value
* etc.

The example script in this folder makes this possible.

The new image will be displayed exactly with the same commands like the old one. This includes any Optional Content conditions, image rotation and being in foreground or background.

The demo script `replacer.py` replaces the PNG background image on page 1 of the example file by its JPG equivalent, which is 80% smaller than the original's size.

The demo script `remover.py` replaces that PNG image by a small empty, fully transparent pixmap. The visual effect is **_like removing_** the image. If inspecting a page's images by methods like `Page.get_images()` that small pixmap will appear like so: `(xref, smask, 1, 1, 8, 'DeviceGray', '', 'Im1', 'FlateDecode')`. Again, this "virtual" deletion happens throughout the file.

## Replacement Approach

* Clean page `/Contents` so that only one contents object exists.
* Get to know the original image's xref.
* Insert new image on the page - just anywhere: location irrelevant. Returns xref of new image.
* Take new image's xref and copy it to the old xref number.
* Remove the new `/Contents` object created by the image insertion.

## Comparing with Redaction Annotations

An image can be removed using redaction annotations. The vacant rectangle can then be filled with another image. This approach may therefore lead to a similar result as the one presented here. The following table compares the two options:

| Criteria | Redaction | XREF copy |
|---------|-----------|-------------------|
| **Specificity** | Removes **everything** inside and intersecting the bbox - which may be undesireable.| Nothing exept the image itself is touched.|
| **Visibility** | Original image visibility is unknown. For the new one you can only decide whether foreground or background.| Original visibility is maintained, including any optional content.|
| **Flexibility** | No restrictions for new image.| Page will use same commands for displaying new image.|
| **Locality** | Affects **the current page only.**| Image will be **_replaced globally:_** the new image will be shown at every place where the old one was displayed.
| **Image removal** | Possible by design, but see side effects mentioned in top line.| Using a new image with 100% transparency and arbitrary dimensions will do a similar, but **_not the same_** job.|

## Notes on Image Removal
When removing an image **_via redactions,_** MuPDF locates the respective display command in the page's `/Contents` and removes it. The image itself is **_not removed_** and may still be visible on other places.

> **Note 1:** If an image is shown by one page only, it **_will_** be completely removed on saves with proper garbage collection.

> **Note 2:** Using a "hacky" approach, locating and removing the display command is also possible with PyMuPDF. But if the global removal of an image is no problem (or even is your intention), do choose the approach presented here.
