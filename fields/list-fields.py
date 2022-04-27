from __future__ import print_function

"""
A demo showing all PDF form fields of a document.
"""
import sys
import fitz
import time

print(fitz.__doc__)

t0 = time.perf_counter() if str is bytes else time.process_time()


def flag_values(ff):
    Ff_text = [
        "ReadOnly",  # 0
        "Required",  # 1
        "NoExport",  # 2
        "",  # 3
        "",  # 4
        "",  # 5
        "",  # 6
        "",  # 7
        "",  # 8
        "",  # 9
        "",  # 10
        "",  # 11
        "Multiline",  # 12
        "Password",  # 13
        "NoToggleToOff",  # 14
        "Radio",  # 15
        "Pushbutton",  # 16
        "Combo",  # 17
        "Edit",  # 18
        "Sort",  # 19
        "FileSelect",  # 20
        "MultiSelect",  # 21
        "DoNotSpellCheck",  # 22
        "DoNotScroll",  # 23
        "Comb",  # 24
        "RichText",  # 25
        "CommitOnSelCHange",  # 26
        "",  # 27
        "",  # 28
        "",  # 29
        "",  # 30
        "",  # 31
    ]

    if ff <= 0:
        return "(none)"
    rc = ""
    ffb = bin(ff)[2:]
    l = len(ffb)
    for i in range(l):
        if ffb[i] == "1":
            rc += Ff_text[l - i - 1] + " "
    return "(" + rc.strip().replace(" ", ", ") + ")"


def print_widget(w):
    if not w:
        return
    d = w.__dict__
    print("".ljust(80, "-"))
    for k in d.keys():
        if k.startswith("_"):
            continue
        if k in ("next", "parent"):
            print(k, "=", type(d[k]))
            continue
        if k != "field_flags":
            print(k, "=", repr(d[k]))
        else:
            print(k, "=", d[k], flag_values(d[k]))
    print("")


doc = fitz.open(sys.argv[1])
if not doc.is_form_pdf:
    sys.exit("'%s' has no form fields." % doc.name)
print("".ljust(80, "-"))
print("Form field synopsis of file '%s'" % sys.argv[1])
print("".ljust(80, "-"))
for page in doc:
    header_shown = False
    for w in page.widgets():
        if not header_shown:
            header_shown = True
            print("Fields on page %i" % page.number)
        print_widget(w)
t1 = time.perf_counter() if str is bytes else time.process_time()
print("total CPU time %g" % (t1 - t0))
