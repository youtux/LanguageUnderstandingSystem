#!/usr/bin/env python
import argparse
import subprocess
import os
import os.path as path
from OrderedSet import OrderedSet

PATHS = {
    'base': 'assets/base.txt',  # Base symbols
    'basic_words': 'dictionaries/basic_words.txt',
    'symbols': 'build/symbols.lex',
    'slu': 'automatons/slu.txt',
    'concepts': 'dictionaries/concepts.txt'
}

try:
    os.makedirs('build/tmp')
except OSError:
    pass


def init_symbols():
    r = OrderedSet()
    if path.exists(PATHS['symbols']):
        read = PATHS['symbols']
    else:
        read = PATHS['base']

    with open(read, 'r') as f:
        for line in f:
            r.add(line.split()[0])
    return r


def fetch_symbols(filepath, grammar=False):
    with open(filepath, 'r') as f:
        for line in f:
            words = line.split()
            if grammar:
                symbols.add(words[0])
            else:
                for word in words:
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
    with open(output, 'w') as out:
        subprocess.check_call(["fsmcompose"] + inputs, stdout=out)


def rmepsilon_fsm(fsm):
    tmppath='build/tmp/p1.fsm'
    with open(tmppath, 'w') as tmpwrite:
        subprocess.check_call(["fsmrmepsilon", fsm], stdout=tmpwrite)
    os.rename(tmppath, fsm)


symbols = init_symbols()
fetch_symbols(PATHS['basic_words'])
fetch_symbols(PATHS['concepts'])
fetch_symbols(PATHS['slu'], grammar=True)

dictionaries = {
    'city_name': 'dictionaries/city_name.txt',
    'airport_name': 'dictionaries/airport_name.txt'
}

words2concepts(dictionaries, 'build/w2c.txt')

compile_fsm('build/w2c.txt', 'build/w2c.fst')
compile_fsm('automatons/c2sc.txt', 'build/c2sc.fst')


subprocess.check_call(["grmread", "-i", PATHS['symbols'], '-c', '-w', PATHS['slu'], '-F', 'build/slu.fst'])
subprocess.check_call(['grmcfcompile', '-i', PATHS['symbols'], '-s', 'S', '-O', '2', 'build/slu.fst', '-F', 'build/slu.fsa'])


compose_fsm(['build/w2c.fst', 'build/c2sc.fst'], 'build/w2sc.fst')
compose_fsm(['build/w2c.fst', 'build/c2sc.fst', 'build/slu.fsa'], 'build/tagger.fst')

# TEST!
#compose_fsm(['simple/0001.fsm', 'build/w2sc.fst'], 'build/0001sc.fsm')
#rmepsilon_fsm('build/test0001.fsm')
# Stage 1: w2c_1
