# PDF Optional Content Support
Optional content support for PDF document was introduced with v1.18.3.
This includes the following features.

## Features in v1.18.3

* Create OCGs. This method will return the PDF cross reference number (xref),which can then be used as the vehicle for object association. If the PDF document did not previously have OC support, the required entries will be created (i.e. the `/OCProperties` dictionary in the PDF catalog).
* Associate annotations, image and form XObject with an existing OCG (optional content group). This will cause those objects to be shown or hidden whenever their OCG is set to ON or OFF.
* Details of all of the PDF's OCGs can be retrieved as a list of one dictionary per OCG.
* User interaction with the optional content of a PDF is offered by many PDF viewers. This can be simulated programmatically. This entails temporarily showing or hiding optional content, triggered by the Python script based on whatever condition.
* Permanent changes to optional content specifications are also possible:
    - Set individual OCGs ON or OFF in a specified PDF configuration layer.
    - Create and maintain OCG radio button groups (`/RBGroups`): these are collections (lists) of OCGs, which allow only one of its members being ON at a time.
    - Document configuration layers can be created and fully maintained just like the default layer.

## Features in v1.18.4

* Like with annotations, optional content references in image and form XObjects can now also be maintained (added, changed or removed).
* Text insertions and drawings can now also be marked as optional content. This pertains to the draw methods and insert text or textbox methods of the `Page` and `Shape` classes.
* `TextWriter` can now also be marked as optional content.
* PDF object type OCMD (Optional Content Membership Dictionary) is now supported. This allows to set object visibility based on logical expressions involving the status of one or more OCGs.


## Unsupported / Missing Features
The following features are missing yet and may be included in future versions:
* The `/Order` array in an OC configuration is currently automatically maintained by adding the xref of every created OCG. According to PDF specifications, this array may however be used to establish an advanced, hierarchical structure of a document's optional content. We may consider offering an interface to edit this object.

## Examples
### `source-radio.py`
Creates a PDF with one page, which is divided in 2 x 2 equal sized rectangles.

The first 4 pages of a `source.pdf` are displayed in those sub-rectangles, each associated with its own OCG. These 4 OCGs are linked together via a radio button group: whenever one source page is set to be displayed (ON), the other three are switched to OFF.

> Please note, that this effect is supported by some (e.g. Adobe Acrobat and Nitro 5), but not all PDF viewers.

### `source-ocmd.py`
**_Requires v1.18.4._**
Creates two objects on a PDF page, which are displayed exactly one at a time.
