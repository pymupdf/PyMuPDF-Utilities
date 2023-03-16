"""
Demo Script: How to insert a text field in DATE format.

This script insert a DATE field on some PDF page using JavaScript for
formatting and field validation.

Note:
-----
This is an example for how to employ JavaScript for field formatting and
validation. Consult this reference for other field types and situations,
like inter-field validation and more:
http://www.adobe.com/content/dam/Adobe/en/devnet/acrobat/pdfs/Acro6JSGuide.pdf
"""
import fitz

# JavaScripts for defining a "date" field format and handling user keystrokes.
JSF = 'AFDate_FormatEx("mm/dd/yyyy");'  # JS to define the format
JSK = 'AFDate_KeystrokeEx("mm/dd/yyyy");'  # JS to handle keystrokes

doc = fitz.open()
page = doc.new_page()
w = fitz.Widget()  # create a skeleton Widget object
w.field_type = fitz.PDF_WIDGET_TYPE_TEXT  # DATE fields are subtypes of TEXT
w.rect = fitz.Rect(20, 20, 160, 80)  # where the date field appears on page
w.field_name = "Date"  # give it a unique name
w.field_value = "12/12/2022"  # field value

# insert JavaScripts in the widget
w.script_format = JSF  # defines the format
w.script_stroke = JSK  # handles keystrokes

annot = page.add_widget(w)  # insert the field in the page

doc.save(__file__.replace(".py", ".pdf"))
