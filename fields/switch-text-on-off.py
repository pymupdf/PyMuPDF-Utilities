"""
Demo script: How to show or hide fields based on checkbox content.

Depending on whether some checkbox is being checked, show or hide
a text widget.

Note:
-----
This is an example for how to employ JavaScript for field formatting and
validation. Consult this reference for other field types and situations,
like inter-field validation and more:
http://www.adobe.com/content/dam/Adobe/en/devnet/acrobat/pdfs/Acro6JSGuide.pdf

Dependencies
------------
PyMuPDF version 1.22.0 or later
"""
import fitz

if not tuple(map(int, fitz.VersionBind.split("."))) > (1, 21, 1):
    raise AssertionError("need PyMuPDF version > 1.21.1")

# This JavaScript will be executed if the checkbox value changes
JSCRIPT = """if (this.getField("my-checkbox").value == "Yes")
    this.getField("my-text").display = display.visible;
else
    this.getField("my-text").display = display.hidden;"""

doc = fitz.open()
page = doc.new_page()

w = fitz.Widget()  # define a field skeleton object for the text
w.rect = fitz.Rect(100, 150, 300, 170)
w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
w.field_name = "my-text"  # use this to identify the field document-wide
w.field_value = "Will be shown if checkbox is checked."
w.script_calc = JSCRIPT  # use this property for inter-field actions
page.add_widget(w)

w = fitz.Widget()  # define field skeleton for the checkbox
w.rect = fitz.Rect(100, 100, 120, 120)
w.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
w.field_name = "my-checkbox"  # use this to identify the field document-wide
w.border_color = fitz.pdfcolor["red"]
w.field_label = "click to show or hide text"  # show this on mouse hovering
w.field_value = True
page.add_widget(w)

doc.save(__file__.replace(".py", ".pdf"))
