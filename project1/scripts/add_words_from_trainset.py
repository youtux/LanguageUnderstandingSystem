#!/usr/bin/env python
from os import path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="Input tagged training set")
parser.add_argument("output_directory", help="Dictionaries output")
args = parser.parse_args()

c = dict()

with open(args.input_file, 'r') as f:
    for line in f:
        split = line.split()
        if len(split) == 0:
            continue
        if split[1] != 'null':
            word = split[0]
            concept = split[1].split('.')[-1]

            #print split[0] + "=>" + str(concept)

            c[concept] = c.get(concept, set()) | {word}
#print c
for concept in c:
    out_path = path.join(args.output_directory, concept + '.txt')

    with open(out_path, 'a+') as out:
        for line in out:
            line = line.rstrip()
            c[concept].discard(line)
        out.write('\n'.join(c[concept]))
        out.write('\n')
        print "Wrote {c} concepts in {path}\n".format(c=len(c[concept]), path=out_path)
