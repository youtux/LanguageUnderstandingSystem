#!/usr/bin/env python
import argparse
import subprocess
import os
import sys
import shutil
import pdb
import os.path as path
from OrderedSet import OrderedSet

PATHS = {
    'base': 'assets/base.txt',  # Base symbols
    'basic_words': 'dictionaries/basic_words.txt',
    'symbols': 'build/symbols.lex',
    'slu': 'automatons/slu.txt',
    'concepts': 'dictionaries/concepts.txt',
    'concepts_dir': 'dictionaries/concepts/'
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


"""
concepts = {
    'city_name': {
        'fromloc.city_name',
        'toloc.city_name',
        'stoploc.city_name'
    },
    'flight_number': {'flight_number'},
    ...
}
"""
def init_concepts():
    c = dict()
    with open(PATHS['concepts'], 'r') as f:
        for line in f:
            line = line.rstrip()
            split = line.split('.')

            weak_concept = split[-1]
            value = c.get(weak_concept, set())

            c[weak_concept] = value | {line}
            #print "line={line}, c[{weak_concept}]={value}".format(line=line, weak_concept=weak_concept, value=c[weak_concept])
    for k in c:
        if len(c[k]) > 1 and k in c[k]:
            c[k].remove(k)
    return c


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


def words2concepts(conceptsdir_path, w2c_path):
    w= {
        'unk2concepts': 100,
        'concepts2null': 70,
        'known2null': 10
    }
    seen = set()
    output = open(w2c_path, 'w')

    files = os.listdir(conceptsdir_path)
    for f in files:
        concept_name = path.splitext(path.basename(f))[0]
        dictionary_path = path.join(conceptsdir_path, f)
        
        with open(dictionary_path, 'r') as dictionary:
            for line in dictionary:
                l = line.rstrip()

                if len(l) == 0:
                    continue

                symbols.add(l)
                seen.add(l)

                for spec_concept in concepts[concept_name]:
                    seen.add(spec_concept)
                    output.write("0\t0\t{input}\t{output}\n".format(input=l, output=spec_concept))
                
                output.write("0\t0\t{input}\tnull\t{w}\n".format(input=l, w=w['concepts2null']))

    for l in symbols - seen:
        output.write("0\t0\t{input}\t{input}\n".format(input=l))
        output.write("0\t0\t{input}\tnull\t{w}\n".format(input=l,w=w['known2null']))

    for c in concepts.values():
        for sc in c:
            output.write("0\t0\t<unk>\t{output}\t{w}\n".format(output=sc, w=w['unk2concepts']))

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

def minimize_fsm(fsm):
    tmppath='build/tmp/p1.fsm'
    with open(tmppath, 'w') as tmpwrite:
        subprocess.check_call(["fsmminimize", fsm], stdout=tmpwrite)
    os.rename(tmppath, fsm)


symbols = init_symbols()
concepts = init_concepts()

fetch_symbols(PATHS['basic_words'])
fetch_symbols(PATHS['concepts'])
fetch_symbols(PATHS['slu'], grammar=True)



subprocess.check_call(["grmread", "-i", PATHS['symbols'], '-c', '-w', PATHS['slu'], '-F', 'build/slu.fst'])

subprocess.check_call(["grmcfapproximate", '-i', PATHS['symbols'], '-s', 'S', '-o', 'build/tmp/symbols.lex', 'build/slu.fst', '-F', 'build/tmp/slu.txt'])

os.rename('build/tmp/slu.txt', 'build/slu.txt')
os.rename('build/tmp/symbols.lex', PATHS['symbols'])
# shutil.copy2(PATHS['slu'], 'build/slu.txt')
symbols = init_symbols()

subprocess.check_call(["grmread", "-i", PATHS['symbols'], '-c', '-w', 'build/slu.txt', '-F', 'build/slu.fst'])

subprocess.check_call(['grmcfcompile', '-i', PATHS['symbols'], '-s', 'S', '-O', '2', 'build/slu.fst', '-F', 'build/slu.fsa'])


#rmepsilon_fsm('build/slu.fsa')

words2concepts(PATHS['concepts_dir'], 'build/w2c.txt')

compile_fsm('build/w2c.txt', 'build/w2c.fst')
rmepsilon_fsm('build/w2c.fst')
# compile_fsm('automatons/c2sc.txt', 'build/c2sc.fst')


compose_fsm(['build/w2c.fst', 'build/slu.fsa'], 'build/tagger.fst')

# TEST!
#compose_fsm(['simple/0001.fsm', 'build/w2c.fst'], 'build/0001c.fsm')
#rmepsilon_fsm('build/test0001.fsm')
# Stage 1: w2c_1
