# PyMuPDF Examples

This directory contains a bunch of examples to help you create PDF, XPS, and eBook applications with PyMuPDF.

## Disclaimer

Some of the examples were initially created in the early days of the package. API changes implemented over time may have caused discrepancies in the scripts. We're not updating them every time an update is released, and there is no guarantee they all will work as originally expected. If you look at the scripts as what they are intended to be, examples, then they will give you a good start.

> At the moment the `examples` folder is being restructured by using the self-explanatory naming conventions described next.

## Conventions

As a rule of thumb, subfolders are named `<action-object>` as if pointing out an action to be performed on an object or set of objects, e.g. `attach-images`. Python scripts are named `<action.py>`, e.g. `attach.py`. Input filenames are called `input`, e.g. `input.pdf` while output filenames are called `output`, e.g. `output.pdf`.

Thus, the `attach.py` script in the `attach-images` folder is meant to attach the images in `attach-images/input` to a new document.

```
cd attach-images
python attach.py
```

For further information on how a particular example is to be run please read the documentation section at the beginning of each script.

Folder | File | Description |
------ | -----| ----------- |
`anonymize-document` | `anonymize.py` | Remove all text from a document. |
`attach-images` | `attach.py` | Attach the images in the input directory to a new document. |
`browse-document` | `browse.py` | Display a document using Tkinter. |
`combine-pages` | `combine.py` | Copy a PDF document combining every 4 pages. |
`copy-embedded` | `copy.py` | Copy the embedded files in the input document to the output document. |
`edit-images` | `edit.py` | Edit images in a PDF document. |
`edit-toc` | `edit.py` | Edit the table of contents (ToC) of a document. |
`embed-images` | `embed.py` | Embed the images found in the input directory. |
`export-embedded` | `export.py` | Extract an embedded file from the input document to the output document. |
`export-metadata` | `export.py` | Export a document metadata dictionary to a CSV file. |
`export-toc` | `export.py` | Export the table of contents (ToC) of a document to a CSV file. |
`extract-images` | `extract-from-pages.py` | Extract the images of a document into the output folder. |
`extract-images` | `extract-from-xref.py` | Extract the images of a document into the output folder. |
`extract-table` | `wx-extract.py` | Browse a document with a wxPython GUI to extract tables. |
`insert-images` | `insert.py` | Create a PDF document by inserting the images found in the input directory. |
`join-documents` | `join.py` | Create a PDF document by inserting the images in the input directory. |
`make-calendar` | `make.py` | Create a calendar with three years in a row. |
`optimize-document` | `optimize.py` | Optimize a PDF document with FileOptimizer. |
`print-hsv` | `print.py` | Create a document showing RGB colors based on hue, saturation and value (HSV). |
`print-page-format` | `print.py` | Print the paper size given a width and height. |
`print-rgb` | `print.py` | Create a document showing RGB colors. |
`sierpinski-fractal` | `carpet.py` | Draw the Sierpinski carpet. |
`sierpinski-fractal` | `punch.py` | Draw the Sierpinski carpet. |
`sierpinski-fractal` | `triangle.py` | Draw the Sierpinski triangle. |
`test-blendmode` | `test.py` | Generate highlight annotations using blend modes. |

## Attributions
So, if you're creating PDF, XPS, and eBook files with PyMuPDF, you may definitely want to check out the input files that have been used in the examples.

Title | Author | Publisher | License |
----- | ------ | --------- | ------- |
[Made with Creative Commons](https://creativecommons.org/use-remix/made-with-cc/) | Paul Stacey and Sarah Hinchliff Pearson | Creative Commons | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |
[Think Python, 2nd ed. for Python 3](https://greenteapress.com/wp/think-python-2e/) | Allen Downey | O'Reilly Media | [CC BY-NC 3.0](https://creativecommons.org/licenses/by-nc/3.0/) |

## Contributing

Contributions are more than welcome. If you find a bug or just want to give some feedback, please let us know by opening an issue or sending a PR. We'll be happy to review the code and merge it into the codebase. Thank you.
