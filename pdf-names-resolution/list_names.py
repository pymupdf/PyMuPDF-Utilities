import fitz_new as fitz


def resolve_names(doc):
    """Convert the PDF's destination names into a Python dict.

    This function must be used with PyMuPDF's new, "rebased" architecture -
    see the above import statement.

    The only parameter is the fitz.Document.
    All names found in the catalog under keys "/Dests" and "/Names/Dests" are
    being included.

    Returns:
        A dcitionary with the following layout:
        - key: (str) the name
        - value: (dict) with the following layout:
           * "page":  target page number (0-based). If no page number found -1.
           * "to": (x, y) target point on page - currently in PDF coordinates!
           * "zoom": (float) the zoom factor
           * "dest": (str) only occurs if the target location on the page has
                     not been provided as "/XYZ" or if no page number was found.
        Examples:
        {'__bookmark_1': {'page': 0, 'to': (0.0, 541.0), 'zoom': 0.0},
         '__bookmark_2': {'page': 0, 'to': (0.0, 481.45), 'zoom': 0.0}}

        '21154a7c20684ceb91f9c9adc3b677c40': {'page': -1, 'dest': '/XYZ 15.75 1486 0'}, ...
    """
    page_xrefs = {doc.page_xref(i): i for i in range(doc.page_count)}

    def get_array(val):
        templ_dict = {"page": -1, "dest": ""}
        xref = val.pdf_to_num()

        if val.pdf_is_array():
            array = doc.xref_object(xref, compressed=True)
        elif val.pdf_is_dict():
            array = doc.xref_get_key(xref, "D")[1]
        else:
            return templ_dict
        array = array.replace("null", "0")[1:-1]
        idx = array.find("/")
        if idx < 1:
            templ_dict["dest"] = array
            return templ_dict
        subval = array[:idx]
        array = array[idx:]
        templ_dict["dest"] = array[idx:]
        if array.startswith("/XYZ"):
            arr_t = array.split()[1:]
            x, y, z = tuple(map(float, arr_t))
            templ_dict["to"] = (x, y)
            templ_dict["zoom"] = z
            del templ_dict["dest"]

        if "0 R" in subval:
            templ_dict["page"] = page_xrefs[int(subval.split()[0])]
        else:
            templ_dict["page"] = int(subval)
        return templ_dict

    def fill_dict(dest_dict, pdf_dict):
        name_count = fitz.mupdf.pdf_dict_len(pdf_dict)
        for i in range(name_count):
            key = fitz.mupdf.pdf_dict_get_key(pdf_dict, i)
            val = fitz.mupdf.pdf_dict_get_val(pdf_dict, i)
            if key.pdf_is_name():
                dict_key = key.pdf_to_name()
            else:
                print(f"key {i} is no /Name")
                dict_key = None
            dict_val = get_array(val)
            if dict_key:
                dest_dict[dict_key] = dict_val

    pdf = fitz.mupdf.pdf_document_from_fz_document(doc)
    trailer = fitz.mupdf.pdf_trailer(pdf)
    root = fitz.mupdf.pdf_new_name("Root")
    catalog = fitz.mupdf.pdf_dict_get(trailer, root)
    dest_dict = {}

    dests = fitz.mupdf.pdf_new_name("Dests")
    old_dests = fitz.mupdf.pdf_dict_get(catalog, dests)
    if old_dests.pdf_is_dict():
        fill_dict(dest_dict, old_dests)

    tree = fitz.mupdf.pdf_load_name_tree(pdf, dests)
    if not tree.pdf_is_dict():
        return dest_dict
    fill_dict(dest_dict, tree)

    return dest_dict
