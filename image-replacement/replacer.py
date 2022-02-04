import fitz

if tuple(map(int, fitz.VersionBind.split("."))) < (1, 19, 5):
    raise ValueError("Need v1.19.5+")

doc = fitz.open("original.pdf")
img_file = "nur-ruhig.jpg"  # the new image
page = doc[0]
page.clean_contents()  # unify page's /Contents into one
images = page.get_images()  # we only are interested in first image here
item = images[0]
old_xref = item[0]  # old image xref

# insert new image just anywhere
new_xref = page.insert_image(page.rect, filename=img_file)

# copy over definition and stream of new image
doc.xref_copy(new_xref, old_xref)

# there now is a second /Contents object, showing new image
cont_xrefs = page.get_contents()

# make sure that new /Contents is forgotten
page.set_contents(cont_xrefs[0])
page.clean_contents()
doc.ez_save("new-image.pdf", garbage=4, pretty=True)
