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
           * "to": (x, y) target point on page - currently in PDF coordinates,
                   i.e. point (0,0) is the bottom-left of the page.
           * "zoom": (float) the zoom factor
           * "dest": (str) only occurs if the target location on the page has
                     not been provided as "/XYZ" or if no page number was found.
        Examples:
        {'__bookmark_1': {'page': 0, 'to': (0.0, 541.0), 'zoom': 0.0},
         '__bookmark_2': {'page': 0, 'to': (0.0, 481.45), 'zoom': 0.0}}

        '21154a7c20684ceb91f9c9adc3b677c40': {'page': -1, 'dest': '/XYZ 15.75 1486 0'}, ...
    """
    # this is a backward listing of xref to page number
    page_xrefs = {doc.page_xref(i): i for i in range(doc.page_count)}

    def obj_string(obj):
        """Return string version of an object that has no xref."""
        buffer = fitz.mupdf.fz_new_buffer(512)
        output = fitz.mupdf.ll_fz_new_output_with_buffer(buffer.m_internal)
        fitz.mupdf.ll_pdf_print_obj(output, obj.m_internal, 1, 0)
        printed = fitz.JM_UnicodeFromBuffer(buffer)
        fitz.mupdf.ll_fz_drop_output(output)
        fitz.mupdf.ll_fz_drop_buffer(buffer.m_internal)
        return printed

    def get_array(val):
        """Generate one item of the names dictionary."""
        templ_dict = {"page": -1, "dest": ""}  # value template
        xref = val.pdf_to_num()  # xref number of the destination target

        # we strive to extract the array of the dest target
        if val.pdf_is_array():  # already an array
            if xref:
                array = doc.xref_object(xref, compressed=True)
            else:
                array = obj_string(val)

        elif val.pdf_is_dict():  # check if dictionary
            # then there must exist a "D" key with the array as value
            array = doc.xref_get_key(xref, "D")[1]

        else:  # if all fails return the empty template
            return templ_dict

        # replace PDF "null" by zero, omit square brackets
        array = array.replace("null", "0")[1:-1]

        # find stuff before first "/"
        idx = array.find("/")
        if idx < 1:  # this has no target page spec
            templ_dict["dest"] = array  # return the orig. string
            return templ_dict

        subval = array[:idx]  # stuff before "/"
        array = array[idx:]  # stuff after "/"
        templ_dict["dest"] = array

        # if we start with /XYZ: extract x, y, zoom
        if array.startswith("/XYZ"):
            arr_t = array.split()[1:]
            x, y, z = tuple(map(float, arr_t))
            templ_dict["to"] = (x, y)
            templ_dict["zoom"] = z
            del templ_dict["dest"]  # we don't return orig string anymore

        # extract page number
        if "0 R" in subval:  # page xref given?
            templ_dict["page"] = page_xrefs[int(subval.split()[0])]
        else:  # naked page number given
            templ_dict["page"] = int(subval)
        return templ_dict

    def fill_dict(dest_dict, pdf_dict):
        """Generate name resolution items for pdf_dict.

        This may be either "/Names/Dests" or just "/Dests"
        """
        # length of the PDF dictionary
        name_count = fitz.mupdf.pdf_dict_len(pdf_dict)

        # extract key-val of each dict item
        for i in range(name_count):
            key = fitz.mupdf.pdf_dict_get_key(pdf_dict, i)
            val = fitz.mupdf.pdf_dict_get_val(pdf_dict, i)
            if key.pdf_is_name():  # this should always be true!
                dict_key = key.pdf_to_name()
            else:
                print(f"key {i} is no /Name")
                dict_key = None

            if dict_key:
                dest_dict[dict_key] = get_array(val)  # store key/value in dict

    # access underlying PDF document of fz Document
    pdf = fitz.mupdf.pdf_document_from_fz_document(doc)

    # access PDF trailer
    trailer = fitz.mupdf.pdf_trailer(pdf)

    # PDF_NAME(Root) = PDF catalog
    root = fitz.mupdf.pdf_new_name("Root")

    # access catalog
    catalog = fitz.mupdf.pdf_dict_get(trailer, root)
    dest_dict = {}

    # make PDF_NAME(Dests)
    dests = fitz.mupdf.pdf_new_name("Dests")

    # extract destinations old style (PDF 1.1)
    old_dests = fitz.mupdf.pdf_dict_get(catalog, dests)
    if old_dests.pdf_is_dict():
        fill_dict(dest_dict, old_dests)

    # extract destinations new style (PDF 1.2+)
    tree = fitz.mupdf.pdf_load_name_tree(pdf, dests)
    if tree.pdf_is_dict():
        fill_dict(dest_dict, tree)

    return dest_dict
