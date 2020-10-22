import fitz

doc = fitz.open("search.pdf")
page = doc[0]
rl = page.searchFor("im vorfeld solch ")
start = rl[0].tl
rl = page.searchFor("stark aus.")
stop = rl[0].br
clip = page.rect
width = clip.width
clip.x1 = width * 0.35

page.addHighlightAnnot(start=start, stop=stop, clip=clip)
doc.save(__file__.replace(".py", ".pdf"))
