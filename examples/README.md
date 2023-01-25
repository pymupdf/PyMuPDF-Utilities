# PyMuPDF Examples

This directory contains example programs for using PyMuPDF.

The scope of these examples should clearly exceed the category "demo". Instead it should contain complete, working programs, or at least snippets of working code.

## Licensing

See the COPYING file.

## Disclaimer

These are quite a number of examples by now. Many of them have originated in early times of the package. Therefore discrepancies may have occurred with any API changes implemented over time. We we will not scan through these scripts for every release, so please regard them as what they are intended for: **examples** which should give you a start - there is no guaranty that everything here works unchanged for all times.

If you find an issue, please fix it and submit a PR, and we will gladly incorporate it.

## Conventions

At the moment the `examples` folder is being restructured by using a self-explanatory naming convention.

As a rule of thumb, subfolders are named `<action-object>` as if pointing out an action to be performed on an object, e.g. `attach-images`. Python scripts are then named `<action.py>`, e.g. `attach.py`. Thus, the `attach.py` script in the `attach-images` folder is meant to attach all images found in the `attach-images/input` directory. Input files and folders are provided to run the examples. Input filenames are called `input`, e.g. `input.pdf`. Output filenames are called `output`, e.g. `output.pdf`.

The input files are distributed under either a [Creative Commons](https://creativecommons.org/licenses/) license or a [GNU Free Documentation License](https://www.gnu.org/licenses/fdl-1.3.html) (GFDL) while images are shared under the [Unsplash](https://unsplash.com/license) license.

For further information on how a particular example is to be run please read the documentation section at the beginning of each script.

## Some Files in This Directory

File | Purpose
-----| -------
`csv2meta.py` | Load a PDF metadata dictionary from a CSV file's contents
`csv2toc.py` | Load a PDF TOC (table of contents) from a CSV file's contents
`embedded-copy.py` | Copies embedded files between source and target PDF
`embedded-export.py` | Exports an embedded file from a PDF
`embedded-import.py` | Embeds a new file into a PDF
`embedded-list.py` | Lists embedded file infos of a PDF
`ParseTab.py` | A function to parse tables within documents
`posterize.py` | Splits up input PDF pages
`TableExtract.py` | Example CLI program using ParseTab
`wxTableExtract.py` | Full-featured GUI using ParseTab. Supports automatic and manual column definitions
