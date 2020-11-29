# PDF Optional Content Support
PyMuPDF has introduced PDF Optional Content (OC) support with v1.18.3 and significantly extended this in v1.18.4.

We believe that we are covering now the most frequently used features, but do expect to see improvements going forward.

The last section of this README is a synopsis of optional content related methods in PyMuPDF.

Our support includes the following features.

## Features Supported

* Create, update and remove OC layers - so-called Optional Content Configurations or OCCDs.
* Create OCGs and use the resulting xref as the vehicle for object association. If the PDF document did not previously have OC support, the required entries will be created (i.e. the `/OCProperties` dictionary in the PDF catalog).
* Associate annotations, images, Form XObject, drawings and text with an existing OCG (optional content group). This will cause those objects to be shown or hidden whenever their OCG is set to ON or OFF.
* Optional content attachments can also be removed for annotations, images and Form XObjects (but nor for drawings and text).
* Details of all of the PDF's OCG, OC layers and temporary visibility status can be retrieved and modified.
* PDF object type OCMD (Optional Content Membership Dictionary) is also supported. OCMDs allow to set object visibility based on logical expressions involving the status of one or more OCGs.


## Unsupported / Missing Features
The following features are missing yet but may be included in future versions:
* The `/Order` array in an OC configuration is currently automatically maintained by adding the xref of every created OCG. According to PDF specifications, this array may however be used to establish an advanced, hierarchical structure of a document's optional content. We may consider offering an interface to edit this object.

## Examples
### `source-radio.py`
Creates a PDF with one page, which is divided in 2 x 2 equal sized rectangles.

The first 4 pages of a `source.pdf` are displayed in those sub-rectangles, each associated with its own OCG. These 4 OCGs are linked together via a radio button group: whenever one source page is set to be displayed (ON), the other three are switched to OFF.

> Please note, that this effect is supported by some (e.g. Adobe Acrobat and Nitro 5), but not all PDF viewers.

### `source-ocmd.py`
**_Requires v1.18.4._**
Creates two objects on a PDF page, which are displayed exactly one at a time.

## PyMuPDF Optional Content Methods

First of all, here is a list of abbreviations and original PDF technical terms used throughout this section:

* **_xref:_** just an abbreviation of "PDF cross reference number".
* **_OC:_** just an abbreviation of "optional content".
* **_OCCD:_** OC configuration dictionary. This object type is used to quickly establish a document-wide setting of all ON/OFF states. There always is a base or default OCCD stored under key `/D` in the `/OCProperties` dictionary of the PDF catalog. Optional additional OCCDs are stored in the `/Configs` array of `/OCProperties`. In PDF viewers (Adobe Acrobat, etc.) you will find terms like "layer" for this notion.
* **_OCG:_** OC group. This PDF object serves as an attribute for other PDF objects, which should have the same visibility status (ON or OFF) at all times. Every PDF supporting OC must have at least one OCG, and all valid OCGs must occur in the central `/OCGs` array of the `/OCProperties` dictionary.
* **_OCMD:_** OC membership dictionary. This PDF object represents a logical expression about the state of one or more OCGs. The boolean value of the expression is in turn interpreted as ON (true) or OFF (false). Instead of an OCG, an OCMD can also be used to control the visibility of PDF objects.

-----
Please note, that this section lists the method **names as defined in v1.18.5.** The following renames have occurred compared to v1.18.4:

|new name|old names|
|---------|----------|
| add_layer |add_layer_config, addLayerConfig|
| get_layers |layer_configs|
| get_layer |get_oc_states|
| set_layer |set_oc_states|
| add_ocg |addOCG|
| get_ocgs |getOCGs|

-----

### `Document.add_ocg`
Add a new OCG to the PDF and return its xref (cross reference number). If the PDF did not previously support OC at all, the required changes to the PDF catalog are made automatically. Please note that, once created, **_an OCG can neither be deleted nor modified_**. Its visibility - which **_can_** be set both, permanently or temporarily - is **_not_** an attribute of the OCG object itself, but stored in other places.

### `Document.get_ocgs`
Return a dictionary of all existing OCGs across all OCCDs. The dictionary key is the OCG xref. An empty dictionary indicates missing OC support in this PDF.

### `Document.get_layers`
Synopsis of all defined optional OC configurations. This is an overview report of the entries in the `/Configs` array. The `/D` layer is not included.

### `Document.get_layer`
List the detail content of the specified OCCD (default or optional OCCD). This is a dictionary with lists of cross reference numbers for OCGs contained in the arrays `/ON`, `/OFF` or radio button groups (`/RBGroups`).

### `Document.set_layer`
Set the content of a given OCCD. This is a **permanent visibility status change** of OCGs under this configuration.

### `Document.add_layer`
Add a new OCCD. This always is a new entry in the `/Configs` array of `/OCProperties`.

### `Document.switch_layer`
Activate the specified OCCD. This causes the visibility state of all OCGs it mentions to be set accordingly. Optionally, this OCCD can be made the default configuration. In this case all `/Configs` entries will be deleted - so the PDF will end up just having the default (`/D`) layer.

### `Document.get_oc`
Return the xref of the OCG or OCMD attached to an image or form XObject. Returns 0 if the object is independent from OC handling. Parameter is the image's xref.

### `Document.set_oc`
Attach an OCG / OCMD to an image or form XObject to control its OC-related visibility. Parameters are the image xref and the OC xref. Replaces any previous value or removes OC support if 0 is used instead of an OC xref.

### `Document.layer_ui_configs`
Show the **_current_** visibility status of all active OCGs. This information is the same as offered by the user interface of PDF viewers. 

### `Document.set_layer_ui_config`
Modify the visibility status of an OCG. This is the same function as offered by the user interface of PDF viewers.

### `Annot.set_oc`
Attach an OCG or OCMD to the annotation. Parameter is the OC xref. Any previous value wil be overwritten. A zero will remove the previous value.

### `Annot.get_oc`
Retrieve the xref of the attached OC entry. A zero indicates, that it is not subject to OC.

### Parameter `oc=xref` for several methods
Methods `Page.insertImage`, `Page.showPDFpage`, `Page.insertText`, `Page.insertTextbox`, `Shape.insertText`, `Shape.insertTextbox`, and `Shape.finish` support the ``oc`` parameter, which accepts the xref of an OCG or OCMD.

### `Page.get_oc_items` (new in v1.18.5)
Returns a list of items `(name, xref, type)`, where _type_ is one of "ocg" / "ocmd", _xref_ the cross reference number of the object and _name_ is the property name. These items represent objects referenced in the page's `/Contents` object. E.g. for the following PDF definitions, this method would return `[("MC0", 7, "ocg")]`.

```
5 0 obj
<<
/Type /Page
...
/Resources<< ... /Properties<<... /MC0 7 0 R>> ... >>
/Contents 6 0 R
...
>>
endobj

6 0 obj
<< ... >>
stream
...
/OC /MC0 BDC
... text or drawing commands
EMC
...
endstream
endobj

7 0 obj
<</Type/OCG ...>>
endobj
```
This shows (relevant parts of) a page definition (xref 5), its content definition (xref 6), and an OCG object definition (xref 7).

The basic takeaway is the relationship between the reference name `/MC0` in the `/Resources/Properties` dictionary, the reference syntax in the contents source and the relationship to the OCG's xref.

If the OCG is OFF, then everything between statements `/OC /MC0 BDC` and `EMC` is ignored: the respective text or graphics are not displayed.
