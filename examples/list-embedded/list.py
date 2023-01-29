"""
Print a list of embedded files in a document
--------------------------------------------------------------------------------
License: GNU AGPL V3
(c) 2021 Jorj X. McKie

Usage
-----
python list.py input.pdf

Description
-----------
The output.pdf file generated in examples/embed-images is renamed as input.pdf
to be used as the input file in this example.
"""

from __future__ import print_function
import sys
import fitz

fn = sys.argv[1]
doc = fitz.open(fn)

name_len = filename_len = 0
total_len = total_size = 0

ef_list = []

for i in range(doc.embfile_count()):
    info = doc.embfile_info(i)
    ef = (
        info["name"],
        info["filename"],
        info["length"],
        info["size"],
    )
    ef_list.append(ef)
    name_len = max(len(ef[0]), name_len)
    filename_len = max(len(ef[1]), filename_len)
    total_len += ef[2]
    total_size += ef[3]

if len(ef_list) < 1:
    print("no embedded files in", fn)
    exit(1)

ratio = float(total_size) / total_len
saves = 1 - ratio

header = (
    "Name".ljust(name_len + 4)
    + "Filename".ljust(filename_len + 4)
    + "Length".rjust(10)
    + "Size".rjust(11)
)
line = "-".ljust(len(header), "-")
print(line)
print(header)
print(line)
for info in ef_list:
    print(
        info[0].ljust(name_len + 3),
        info[1].ljust(filename_len + 3),
        str(info[2]).rjust(10),
        str(info[3]).rjust(10),
    )
print(line)
print(len(ef_list), "embedded files in '%s'. Totals:" % (fn,))
print(
    "File lengths: %s, compressed: %s, ratio: %s%% (savings: %s%%)."
    % (total_len, total_size, str(round(ratio * 100, 2)), str(round(saves * 100, 2)))
)
print(line)
