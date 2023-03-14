"""
Demo script for PDF form fields / widgets

Depending on whether some checkbox is being checked, show or hide
a text widget.
"""
import fitz

doc = fitz.open()
page = doc.new_page()

# This JavaScript will be executed if the checkbox value changes
text_js = """if (this.getField("my-checkbox").value == "Yes")
    this.getField("my-text").display = display.visible;
else
    this.getField("my-text").display = display.hidden;"""

text = fitz.Widget()
text.rect = fitz.Rect(100, 150, 300, 170)
text.field_type = fitz.PDF_WIDGET_TYPE_TEXT
text.field_name = "my-text"
text.field_value = "Will be shown if checkbox is checked."
text.script_calc = text_js  # use this property for inter-field actions
page.add_widget(text)

cbox = fitz.Widget()
cbox.rect = fitz.Rect(100, 100, 120, 120)
cbox.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
cbox.field_name = "my-checkbox"
cbox.field_value = True
page.add_widget(cbox)

doc.save(__file__.replace(".py", ".pdf"), deflate=False, pretty=True)
