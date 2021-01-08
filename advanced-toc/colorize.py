import fitz

doc = fitz.open("example.pdf")
toc = doc.get_toc(False)
for i, item in enumerate(toc):
    lvl, title, pno, ddict = item
    ddict["collapse"] = False
    if lvl == 1:
        ddict["color"] = (1, 0, 0)
        ddict["bold"] = True
        ddict["italic"] = False
    elif lvl == 2:
        ddict["color"] = (0, 0, 1)
        ddict["bold"] = False
        ddict["italic"] = True
    else:
        ddict["color"] = (0, 1, 0)
        ddict["bold"] = ddict["italic"] = False
    doc.set_toc_item(i, dest_dict=ddict)
doc.save("new-toc.pdf")
