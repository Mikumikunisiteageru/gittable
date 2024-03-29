# gittable.py

import codecs
import os
import shutil
import sys
import pandas as pd

VERSION = "0.0.2"

def encode_string(string, zip=True):
    new_string = string.replace("^", "^^")
    if zip:
        new_string += "^"
    return new_string

def decode_string(string):
    l = len(string)
    i = l - 1
    while i >= 0 and string[i] == '^':
        i -= 1
    j = l - i - 1
    if j & 1 == 1:
        zip = True
        return string[:l-1].replace("^^", "^"), True
    else:
        return string.replace("^^", "^"), False

def push_in(filename):
    subdir = os.path.join(".gittable", encode_string(filename, True))
    if os.path.isdir(subdir):
        shutil.rmtree(subdir)
    os.mkdir(subdir)
    tables = pd.read_excel(io=filename, dtype=str, sheet_name=None)
    for (i, sheet) in enumerate(tables.keys()):
        table = tables[sheet]
        out_file = os.path.join(subdir, f"{i+1}_{sheet}.txt")
        with codecs.open(out_file, "w", "utf-8") as fout:
            print(*table.shape, sep='\n', end='\n', file=fout)
        table.to_csv(out_file, sep='\n', lineterminator='\n', mode="a", 
            header=False, index=False)

def run_git(command):
    if not os.path.isdir(".gittable"):
        assert not os.path.isfile(".gittable")
        os.mkdir(".gittable")
    os.chdir(".gittable")
    os.system(f"git {command}")
    os.chdir("..")

if __name__ == "__main__":
    if len(sys.argv) >= 2: 
        if sys.argv[1] in ["add", "diff"]:
            assert len(sys.argv) >= 3
            filename = sys.argv[2]
            assert os.path.isfile(filename)
            assert os.path.splitext(filename)[1] in [".xlsx", ".xls"]
            push_in(filename)
            sys.argv[2] = "."
        elif sys.argv[1] in []:
            pass
    run_git(' '.join(f'"{s}"' for s in sys.argv[1:]))
