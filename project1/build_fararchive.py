#!/usr/bin/env python
import argparse
import subprocess
from OrderedSet import OrderedSet
import os.path as path


def read_symbols_file(filepath):
    r = OrderedSet(['<eps>'])
    if not path.exists(filepath):
        return r

    with open(filepath, 'r') as f:
        for line in f:
            r.add(line.split()[0])
    return r

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="Input file containing sentences")
parser.add_argument("output_directory", help="Directory in which symbols and compiled far will be stored")
args = parser.parse_args()

paths = {
    'input': args.input_file,
    'symbols': path.join(args.output_directory, "symbols.lex"),
    'fararchive': path.join(args.output_directory, path.basename(args.input_file) + ".far")
}

# Build the symbols list
syms = read_symbols_file(paths['symbols'])

for line in open(paths['input'], "r"):
    for v in line.split():
        syms.add(v)

# Write symbols.lex
with open(paths['symbols'], "w") as d:
    c = 0
    for v in syms:
        d.write("{term}\t{index}\n".format(term=v, index=c))
        c += 1

# Call farcompilestrings
with open(paths['fararchive'], "w") as f:
    subprocess.check_call(["farcompilestrings", "-i", paths['symbols'], paths['input']], stdout=f)
