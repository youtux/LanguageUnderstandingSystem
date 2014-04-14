#!/usr/bin/env python
from os import path
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_tagged", help="Input generated from tagger")
parser.add_argument("golden_tagged", help="Input gold")
args = parser.parse_args()

golden_f = open(args.golden_tagged, 'r')
input_f = open(args.input_tagged, 'r')

c = 0

end = False
while not end:
    in1 = golden_f.readline()
    in2 = input_f.readline()

    if (in1 == "") != (in2 == ""):
        c += 1

    in1 = in1.rstrip()
    if in2 not in ["", "\n"]:
        in2 = in2.split()[1]

    if in1 == "" and in2 == "":
        end = True
    print in1 + "\t" + in2

sys.exit(c)
