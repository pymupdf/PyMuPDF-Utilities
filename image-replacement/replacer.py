import fitz

if tuple(map(int, fitz.VersionBind.split("."))) < (1, 19, 5):
    raise ValueError("Need v1.19.5+")


def img_replace(page, xref, filename=None, stream=None, pixmap=None):
    """Replace image identified by xref.

    Args:
        page: a fitz.Page object
        xref: cross reference number of image to replace
        filename, stream, pixmap: must be given as for
        page.insert_image().

    """
    if bool(filename) + bool(stream) + bool(pixmap) != 1:
        raise ValueError("Exactly one of filename/stream/pixmap must be given")
    doc = page.parent  # the owning document
    # insert new image anywhere in page
    new_xref = page.insert_image(
        page.rect, filename=filename, stream=stream, pixmap=pixmap
    )
    doc.xref_copy(new_xref, xref)  # copy over new to old
    last_contents_xref = page.get_contents()[-1]
    # new image insertion has created a new /Contents source,
    # which we will set to spaces now
    doc.update_stream(last_contents_xref, b" ")


if __name__ == "__main__":
    doc = fitz.open("original.pdf")
    img_file = "nur-ruhig.jpg"  # the new image
    page = doc[0]
    images = page.get_images()  # we only are interested in first image here
    item = images[0]
    old_xref = item[0]  # old image xref
    img_replace(page, old_xref, filename=img_file)
    doc.ez_save("new-image.pdf", garbage=4, pretty=True)
