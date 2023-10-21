def resolve_names(doc):
    """Determine target pages of destination names.

    Returns a dictionary whose keys are destination names and whose values
    are dictionaries with key "page" (0-based number), "to" (target point on
    the page as a  tuple of floats (x, y)) and "zoom" (float zoom factor
    or None).

    Args:
        doc: (fitz.Document) a PDF document.

    Returns:
        A dictionary of the form
        dest_names["dest-name"] = {"page": 314, "to": (72, 211), "zoom": None}.
    """

    def get_names(xref, destinations):
        def split_destinations(names):
            rc = []
            names = names.replace(" 0 R", ",")
            names = names.split(",")
            for name in names[:-1]:
                idx = name.find(")")
                dest = name[1:idx]
                xref = int(name[idx + 1 :])
                rc.append((dest, xref))
            return rc

        kids = doc.xref_get_key(xref, "Kids")
        if kids[0] == "array":
            kids = list(map(int, kids[1][1:-1].replace("0 R", "").split()))
            for kid_xref in kids:
                destinations = get_names(kid_xref, destinations)

        names = doc.xref_get_key(xref, "Names")
        names = names[1][1:-1]
        if names is not None:
            destinations.extend(split_destinations(names))
        return destinations

    def make_dest_dict(xref_to_page, dest):
        dest = dest[1:-1]
        pxref = int(dest.split()[0])
        idx = dest.find("0 R")
        dest_dict = {"page": xref_to_page[pxref], "to": None, "zoom": 0}
        dest_arr = dest[idx + 3 :].split()
        if dest_arr[0] == "/XYZ":
            dest_dict["to"] = (float(dest_arr[1]), float(dest_arr[2]))
            try:
                dest_dict["zoom"] = float(dest_arr[-1])
            except ValueError:
                pass
        return dest_dict

    obj_type, dests_xref = doc.xref_get_key(doc.pdf_catalog(), "Names/Dests")

    if obj_type == "xref":
        dests_xref = int(dests_xref.split()[0])
    else:
        return {}

    destinations = []
    destinations = get_names(dests_xref, destinations)

    xref_to_page = {doc.page_xref(i): i for i in range(doc.page_count)}

    dest_names = {}
    for name, xref in destinations:
        item = doc.xref_get_key(xref, "D")
        if item[0] == "array":
            dest_dict = make_dest_dict(xref_to_page, item[1])
            dest_names[name] = dest_dict
        else:
            item = doc.xref_object(xref, compressed=True)
            if item[0] == "[" and item[-1] == "]":
                dest_dict = make_dest_dict(xref_to_page, item)
                dest_names[name] = dest_dict
            else:
                pass

    return dest_names
