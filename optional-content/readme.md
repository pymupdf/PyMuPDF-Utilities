# PDF Optional Content Support
Optional content support for PDF document was introduced with v1.18.3.
This includes the following features.

## Features included in v1.18.3

* Associate annotations, images and Form XObjects with any existing OCG (optional content group). This will cause those objects to be shown or hidden whenever their OCG is set to ON or OFF.
* Create OCGs. This method will return the PDF cross reference number (xref),which can then be used as the vehicle for object association. If the PDF document did not previously have OC support, the required entries will be created automatically (i.e. the `/OCProperties` dictionary in the PDF catalog).
* Details of all OCGs can be retrieved as a list of one dictionary per OCG.
* User interaction with the optional content of a PDF, which is offered by many PDF viewers, can be simulated programmatically, i.e. temporarily showing or hiding optional content can be triggered by the Python script based on whatever condition.
* Permanent changes to optional content specifications are also possible:
    - Setting individual OCGs ON or OFF.
    - Creating and maintaining OCG radio button groups (`/RBGroups`): these are collections (lists) of OCGs, which allow only one of its members being ON at a time.
    - Document view layers can be created and fully maintained just like the default layer.

## Unsupported / Missing Features
The following features are missing yet and may be included in future versions:
* Add or maintain OC support to **_existing_** images and XObjects. Currently OC support can be **_added_** only at creation time of the object and not be added / changed afterwards. Full support in that sense already exists for annotations (`Annot.setOC(xref)`).
* In PDF, text and drawings may also be put under OC control. This features is currently not supported.
* The `/Order` array in an OC configuration is currently automatically maintained (extended with the xref of every created OCG). It may however be used to establish an advanced, hierarchical structure of a document's optional content. We might consider offering an interface to editing this information.
* In PDF, not OCGs may be associated with the display of an object, but also an **OCMD** ("optional content membership dictionary"). This is an array of OCGs linked via a logical expression (similar to Python's ``any()`` and ``all()`` builtin functions). This feature is not yet implemented.

## Examples
The folder currently contains the example script `radio-ocg.py`. It creates a PDF with one page, which is divided in 2 x 2 equal sized rectangles.

The first 4 pages of a `source.pdf` are displayed in those sub-rectangles, controlled by a group of OCGs which are linked together via a radio button group: whenever one source page is set to be displayed (ON), the other three are switched to OFF.

> Please note, that this effect works for some (e.g. Adobe Acrobat), but not for all PDF viewers.
