# PyMuPDF Examples

This directory contains a bunch of examples to help you create PDF, XPS, and eBook applications with PyMuPDF.

## Disclaimer

Some of the examples were initially created in the early days of the package. API changes implemented over time may have caused discrepancies in the scripts. We're not updating them every time an update is released, and there is no guarantee they all will work as originally expected. If you look at the scripts as what they are intended to be, examples, then they will give you a good start.

> At the moment the `examples` folder is being restructured by using the self-explanatory naming conventions described next.

## Conventions

As a rule of thumb, subfolders are named `<action-object>` as if pointing out an action to be performed on an object or set of objects, e.g. `attach-images`. Python scripts are named `<action.py>`, e.g. `attach.py`. Input filenames are called `input`, e.g. `input.pdf` while output filenames are called `output`, e.g. `output.pdf`.

Thus, the `attach.py` script in the `attach-images` folder is meant to attach all images found in the `attach-images/input` directory.

```
cd attach-images
python attach.py
```

The input files are distributed under either a [Creative Commons](https://creativecommons.org/licenses/) license or a [GNU Free Documentation License](https://www.gnu.org/licenses/fdl-1.3.html) (GFDL) while images are shared under the [Unsplash](https://unsplash.com/license) license.

For further information on how a particular example is to be run please read the documentation section at the beginning of each script.

Folder | Description |
------ | ----------- |
`anonymize-document` | Remove all text from a document. |
`attach-images` | Attach all images found in a directory. |
`browse-document` | Display a PyMuPDF Document using Tkinter. |
`combine-pages` | Copy an input PDF to output combining every 4 pages. |
`edit-images` | Edit images in a PDF document. |
`edit-toc` | Edit the table of contents (ToC) of a document. |
`embed-images` | Embed all images found in a directory. |
`export-metadata` | Export a document metadata dictionary to a CSV file. |
`export-toc` | Export the table of contents (ToC) of a document to a CSV file. |
`extract-images` | Extract images from a PDF document. |

## Contributing

If you find an issue or bug, please let us know or send a PR. We'll be happy to review it and merge it into the codebase. Thank you.
