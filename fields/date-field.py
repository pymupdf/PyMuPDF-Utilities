"""
How to insert a text field in DATE format
"""
import fitz

doc = fitz.open()
page = doc.new_page()
w = fitz.Widget()
w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
w.rect = fitz.Rect(20, 20, 160, 80)
w.field_name = "Date"
w.field_value = "12/12/2022"

"""
JavaScripts to make a "date" field and handle user keystrokes.
See this manual for more information, including JavaScripts for other fields:
https://experienceleague.adobe.com/docs/experience-manager-learn/assets/FormsAPIReference.pdf?lang=en
"""
jsf = 'AFDate_FormatEx("mm/dd/yyyy");'  # JS to define the format
jsk = 'AFDate_KeystrokeEx("mm/dd/yyyy");'  # JS to handle keystrokes

# insert the scripts above in the widget:
w.script_format = jsf  # defines the format
w.script_stroke = jsk  # handles keystrokes

annot = page.add_widget(w)
doc.save(__file__.replace(".py", ".pdf"), pretty=True)
