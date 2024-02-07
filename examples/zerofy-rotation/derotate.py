import sys
import fitz


def page_rotation_set0(page):
    """Nullify page rotation."""

    rot = page.rotation  # contains normalized rotation value
    if rot == 0:
        return page  # nothing to do
    # need to derotate the page's content
    mb = page.mediabox  # current mediabox

    if rot == 90:
        # before derotation, shift content horizontally
        mat0 = fitz.Matrix(1, 0, 0, 1, mb.y1 - mb.x1 - mb.x0 - mb.y0, 0)
    elif rot == 270:
        # before derotation, shift content vertically
        mat0 = fitz.Matrix(1, 0, 0, 1, 0, mb.x1 - mb.y1 - mb.y0 - mb.x0)
    else:
        mat0 = fitz.Matrix(1, 0, 0, 1, -2 * mb.x0, -2 * mb.y0)

    # prefix with derotation matrix
    mat = mat0 * page.derotation_matrix
    cmd = b"%g %g %g %g %g %g cm " % tuple(mat)
    xref = fitz.TOOLS._insert_contents(page, cmd, 0)

    # swap x- and y-coordinates
    if rot in (90, 270):
        x0, y0, x1, y1 = mb
        mb.x0 = y0
        mb.y0 = x0
        mb.x1 = y1
        mb.y1 = x1
        page.set_mediabox(mb)

    page.set_rotation(0)

    # refresh the page to apply these changes
    doc = page.parent
    pno = page.number
    page = doc[pno]
    page.clean_contents()
    return page


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except:
        sys.exit("Usage: python derotate.py input.pdf")
    doc = fitz.open(filename)
    for pno in range(len(doc)):
        page_rotation_set0(doc[pno])
    doc.ez_save(filename.replace(".pdf", "-rot0.pdf"), clean=True)
