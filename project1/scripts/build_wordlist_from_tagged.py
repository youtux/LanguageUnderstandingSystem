#!/usr/bin/env python
from os import path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="Input TAGGED training set (file.train.tagged)")
args = parser.parse_args()

c = []
buf = ""

with open(args.input_file, 'r') as f:
    for line in f:
        split = line.split()
        if len(split) != 0:
            buf += split[0] + " "
        else:
            print buf
            buf = ""
