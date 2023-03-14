"""
Demo script for PDF widgets.

Make a PDF with three pages. On each page, two fields are added and the result
is stored in a third field on that page.

Choosing three pages doing essentially the same thing, shall demonstrate,
that field names across the whole PDF must be uniquely named.
"""
import fitz

r1 = fitz.Rect(100, 100, 300, 120)
r2 = fitz.Rect(100, 130, 300, 150)
r3 = fitz.Rect(100, 180, 300, 200)

doc = fitz.open()  # make a new, empty PDF
for i in range(3):  # make three pages in it
    # in essence we are causing the computation NUM1 + NUM2 = RESULT
    page = doc.new_page()  # make the page

    w = fitz.Widget()
    w.field_name = f"NUM1{page.number}"
    w.rect = r1
    w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
    w.field_value = f"{i*100+1}"
    w.field_flags = 2
    page.add_widget(w)

    w = fitz.Widget()
    w.field_name = f"NUM2{page.number}"
    w.rect = r2
    w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
    w.field_value = "200"
    w.field_flags = 2
    page.add_widget(w)

    w = fitz.Widget()  # the result field
    w.field_name = f"RESULT{page.number}"
    w.rect = r3
    w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
    w.field_value = "Resultat?"
    w.script_calc = f'AFSimple_Calculate("SUM", new Array("NUM1{page.number}", "NUM2{page.number}"));'
    page.add_widget(w)

doc.save(__file__.replace(".py", ".pdf"), pretty=True)
