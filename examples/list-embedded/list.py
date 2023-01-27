"""
Return a list of embedded files in a document
-------------------------------------------------------------------------------
License: GNU AGPL V3
(c) 2021 Jorj X. McKie

Usage
-----
python list.py input.pdf

Notes
-----
The output.pdf file generated in examples/embed-images is renamed as input.pdf
to be used as the input file in this example.

Dependencies
------------
PyMuPDF
"""

from __future__ import print_function
import sys
import fitz

fn = sys.argv[1]
doc = fitz.open(fn)  # oprn input

name_len = fname_len = 0  # some fields of interest
tlength = tsize = 0  # total length and compressed sizes

ef_list = []  # store file infos here, because I wanted
# to adjust column widths of the report to actually occurring data ...
# Of yourse, a direct print is perfectly possible.

for i in range(doc.embfile_count()):  # number of embedded files
    info = doc.embfile_info(i)  # get one info dict
    ef = (
        info["name"],
        info["filename"],
        info["length"],
        info["size"],
    )
    ef_list.append(ef)  # save in the info list
    name_len = max(len(ef[0]), name_len)  # column width of 'name'
    fname_len = max(len(ef[1]), fname_len)  # column width of 'filename'
    tlength += ef[2]  # add to total orignal file size
    tsize += ef[3]  # add to total compressed file size

if len(ef_list) < 1:  # are we being fooled?
    print("no embedded files in", fn)
    exit(1)

ratio = float(tsize) / tlength  # compression ration
saves = 1 - ratio  # savings percentage
# define header line
header = (
    "Name".ljust(name_len + 4)
    + "Filename".ljust(fname_len + 4)
    + "Length".rjust(10)
    + "Size".rjust(11)
)
line = "-".ljust(len(header), "-")  # horizontal line
print(line)  # print header
print(header)  # ...
print(line)  # ...
# now print each file info ...
for info in ef_list:
    print(
        info[0].ljust(name_len + 3),
        info[1].ljust(fname_len + 3),
        str(info[2]).rjust(10),
        str(info[3]).rjust(10),
    )
# print some wrap up information
print(line)
print(len(ef_list), "embedded files in '%s'. Totals:" % (fn,))
print(
    "File lengths: %s, compressed: %s, ratio: %s%% (savings: %s%%)."
    % (tlength, tsize, str(round(ratio * 100, 2)), str(round(saves * 100, 2)))
)
print(line)
