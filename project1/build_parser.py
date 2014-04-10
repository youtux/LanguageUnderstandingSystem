#!/usr/bin/env python
import argparse
import subprocess
import os
import os.path as path
from OrderedSet import OrderedSet

PATHS = {
    'symbols': 'build/symbols.lex',
    'concepts': 'dictionaries/concepts.txt'
}

try:
    os.makedirs('build/tmp')
except OSError:
    pass


def init_symbols():
    r = OrderedSet(['<eps>'])
    if not path.exists(PATHS['symbols']):
        return r

    with open(PATHS['symbols'], 'r') as f:
        for line in f:
            r.add(line.split()[0])
    return r


def fetch_symbols(filepath):
    with open(filepath, 'r') as f:
        for word in f.read().split():
            symbols.add(word)
    flush_symbols()


def flush_symbols():
    with open(PATHS['symbols'], "w") as out:
        c = 0
        for v in symbols:
            out.write("{term}\t{index}\n".format(term=v, index=c))
            c += 1


def words2concepts(dictionaries, w2c_path):
    seen = set()
    output = open(w2c_path, 'w')

    for dictionary_name, dictionary_path in dictionaries.items():
        with open(dictionary_path, 'r') as dictionary:
            for line in dictionary:
                l = line.rstrip()

                symbols.add(l)
                seen.add(l)

                output.write("0\t0\t{input}\t{output}\n".format(input=l, output=dictionary_name))
    for l in symbols - seen:
        output.write("0\t0\t{input}\t{input}\n".format(input=l))

    output.write("0\n")
    output.close()

    flush_symbols()


def compile_fsm(sourcepath, destpath):
    subprocess.check_call(["fsmcompile", "-t", "-i", PATHS['symbols'], "-o", PATHS['symbols'], "-F", destpath, sourcepath])


def compose_fsm(inputs, output):
    tmppath = {
        'read': 'build/tmp/p1.fsm',
        'write': 'build/tmp/p2.fsm'
    }

    input1 = inputs.pop(0)
    while len(inputs) != 0:
        input2 = inputs.pop(0)

        with open(tmppath['write'], 'w') as tmpwrite:
            subprocess.check_call(["fsmcompose", input1, input2], stdout=tmpwrite)

        os.rename(tmppath['write'], tmppath['read'])

        input1 = tmppath['read']
    os.rename(tmppath['read'], output)


symbols = init_symbols()
fetch_symbols(PATHS['concepts'])

dictionaries = {
    'city_name': 'dictionaries/city_name.txt',
    'airport_name': 'dictionaries/airport_name.txt'
}

words2concepts(dictionaries, 'build/w2c.txt')

compile_fsm('build/w2c.txt', 'build/w2c.fst')
#compile_fsm('automatons/c2sc.txt', 'build/c2sc.fst')

# TEST!
compose_fsm(['simple/0001.fsm', 'build/w2c.fst'], 'build/test0001.fsm')
# Stage 1: w2c_1
