# PyMuPDF Examples

## Conventions

As a rule of thumb, subfolders are named `<action-object>` as if pointing out an action to be performed on an object or set of objects, e.g. `attach-images`. Python scripts are named `<action.py>`, e.g. `attach.py`. Input filenames are called `input`, e.g. `input.pdf` while output filenames are called `output`, e.g. `output.pdf`.

Thus, the `attach.py` script in the `attach-images` folder is meant to attach the images in `attach-images/input` to a new document.

```
cd attach-images
python attach.py
```

## Examples

For further information on how to run a particular example please read the documentation section at the beginning of each script.

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
`extract-table` | `extract.py` | CLI program to extract tables. |
`extract-table` | `wx-extract.py` | Browse a document with a wxPython GUI to extract tables. |
`extract-xobj` | `extract.py` | Scan a document and store the embedded XObjects as pages in a new document. |
`insert-images` | `insert.py` | Create a PDF document by inserting the images found in the input directory. |
`join-documents` | `join.py` | Create a PDF document by inserting the images in the input directory. |
`list-embedded` | `list.py` | Print a list of embedded files in a document. |
`load-metadata` | `load.py` | Load a metadata dictionary from a CSV file into a PDF document. |
`load-toc` | `load.py` | Load a table of contents (ToC) from a CSV file into a PDF document. |
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
Described below are the input files that have been used in the examples to create PDF, XPS files and eBooks with PyMuPDF.

Title | Author | Publisher | License |
----- | ------ | --------- | ------- |
[Fluffy cockapoo having the time of his life at the park](https://unsplash.com/photos/qO-PIF84Vxg) | Joe Caione | Unsplash | [Unsplash](https://unsplash.com/license) |
[Made with Creative Commons](https://creativecommons.org/use-remix/made-with-cc/) | Paul Stacey and Sarah Hinchliff Pearson | Creative Commons | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |
[Silver tabby cat photo](https://unsplash.com/photos/s2mkB4WOl9k) | Erik-Jan Leusink | Unsplash | [Unsplash](https://unsplash.com/license) |
[Think Python, 2nd ed. for Python 3](https://greenteapress.com/wp/think-python-2e/) | Allen Downey | O'Reilly Media | [CC BY-NC 3.0](https://creativecommons.org/licenses/by-nc/3.0/) |

## Contributing

Contributions are more than welcome. If you find a bug or just want to give some feedback, please let us know by opening an issue or sending a PR. We'll be happy to review the code and merge it into the codebase. Thank you.
