import fitz

r1 = fitz.Rect(100, 100, 300, 120)
r2 = fitz.Rect(100, 130, 300, 150)
r3 = fitz.Rect(100, 180, 300, 200)

doc = fitz.open()
for i in range(3):
    page = doc.new_page()
    print(f"page {page.number}")
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

    w = fitz.Widget()
    w.field_name = f"RESULT{page.number}"
    w.rect = r3
    w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
    w.field_value = "Resultat?"
    w.script_calc = f'AFSimple_Calculate("SUM", new Array("NUM1{page.number}", "NUM2{page.number}"));'
    page.add_widget(w)

    print("AcroForm/CO =", doc.xref_get_key(doc.pdf_catalog(), "AcroForm/CO"))

doc.save(__file__.replace(".py", ".pdf"), pretty=True)
