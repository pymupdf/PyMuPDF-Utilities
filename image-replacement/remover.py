import fitz


def replace_object(doc, target: int, source: int, *, keep: list = []) -> None:
    """Makes the old xref a duplicate of new xref.

    Notes:
        Also supports cases where new xref is a stream object.
    Args:
        target: target xref
        source: source xref
        keep: do not remove these keys in target xref
    """
    if doc.xref_is_stream(source):
        # read new xref stream maintaining compression
        stream = doc.xref_stream_raw(source)
        doc.update_stream(
            target,
            stream,
            compress=False,  # keeps source compression
            new=True,  # in case target is no stream
        )

    # empty target completely, except optional content definition
    for key in doc.xref_get_keys(target):
        if key in keep:
            continue
        doc.xref_set_key(target, key, "null")
    # copy over all source dict items
    for key in doc.xref_get_keys(source):
        item = doc.xref_get_key(source, key)
        doc.xref_set_key(target, key, item[1])
    return None


# This script variant does a pseudo-removal:
# replace image by a fully transparent pixmap with same dimensions
doc = fitz.open("original.pdf")

page = doc[0]
page.clean_contents()  # unify page's /Contents into one
images = page.get_images()  # we only are interested in first image here
item = images[0]
old_xref = item[0]  # old image xref

# make pixmap of just any dimension
pix = fitz.Pixmap(fitz.csGRAY, (0, 0, 5, 5), 1)
pix.clear_with()  # clear all samples bytes to 0x00

# insert new image just anywhere
new_xref = page.insert_image(page.rect, pixmap=pix)

# copy over definition and stream of new image
replace_object(doc, old_xref, new_xref, keep=["OC"])

# there now is a second /Contents object, showing new image
cont_xrefs = page.get_contents()

# make sure that new /Contents is forgotten again
page.set_contents(cont_xrefs[0])

doc.ez_save("no-image.pdf", garbage=4)
