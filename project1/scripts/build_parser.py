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


def init_symbols():
    r = OrderedSet()
    read = PATHS['symbols'] if path.exists(PATHS['symbols']) else PATHS['base']
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
    # for k in c:
    #     if len(c[k]) > 1 and k in c[k]:
    #         c[k].remove(k)
    return c


def fetch_symbols(filepath, grammar=False):
    ret = set()
    with open(filepath, 'r') as f:
        for line in f:
            words = line.split()
            if grammar:
                symbols.add(words[0])
                ret.add(words[0])
            else:
                for word in words:
                    symbols.add(word)
                    ret.add(word)
    flush_symbols()
    return ret


def flush_symbols():
    with open(PATHS['symbols'], "w") as out:
        for c, v in enumerate(symbols):
            out.write("{term}\t{index}\n".format(term=v, index=c))


def nullifier(nullifier_path):
    c = fetch_symbols(PATHS['concepts'])
    with open(nullifier_path, 'w') as out:
        for word in symbols - {'<eps>'}:
            outword = word if word in c else "null"
            out.write("0\t0\t{input}\t{output}\n".format(input=word, output=outword))
        out.write("0\n")


# this is the main function that build the w2c parser
def words2concepts(conceptsdir_path, basic_words, w2c_path):
    # define weights
    w= {
        'unk2concepts': 4,
        'unk2null': 2,
        'basic2null': 5,
        'concepts2null': 4,
    }

    # adds/updates a line in the w2c.txt
    def update(buf, inp, out, weight=0):
        if inp not in buf:
            buf[inp] = {out: weight}
        elif out in buf[inp]:
            m = min(buf[inp][out], weight)
            buf[inp][out] = m
        else:
            buf[inp].update({out: weight})


    buf = dict()
    seen = set()

    # take every file that doesn't end with '.ignore' in the given path
    files = os.listdir(conceptsdir_path)
    for f in files:
        concept_name = path.splitext(path.basename(f))[0]
        ext = path.splitext(path.basename(f))[1]
        if ext == '.ignore':
            continue
        dictionary_path = path.join(conceptsdir_path, f)

        with open(dictionary_path, 'r') as dictionary:
            for line in dictionary:
                l = line.rstrip()

                if len(l) == 0:
                    continue

                symbols.add(l)
                seen.add(l)

                for spec_concept in concepts[concept_name]:
                    symbols.add(spec_concept)
                    update(buf, l, spec_concept)
                update(buf, l, l)
                update(buf, l, "null", w['concepts2null'])

    for l in basic_words:
        seen.add(l)
        update(buf, l, l)
        update(buf, l, "null", w['basic2null'])

    for c in concepts.values():
        for sc in c:
            weight = w['unk2null'] if sc == 'null' else w['unk2concepts']
            for unk in symbols - seen - {'<eps>'}:
                update(buf, unk, sc, weight)

    with open(w2c_path, 'w') as output:
        for inp in buf:
            for out, weight in buf[inp].iteritems():
                output.write("0\t0\t{input}\t{output}\t{weight}\n".format(input=inp, output=out, weight=weight))
        output.write("0\n")

    flush_symbols()

if __name__ == '__main__':
    try:
        os.makedirs('build/tmp')
    except OSError:
        pass

    symbols = init_symbols()
    concepts = init_concepts()

    basic_words = fetch_symbols(PATHS['basic_words'])
    fetch_symbols(PATHS['concepts'])

    words2concepts(PATHS['concepts_dir'], basic_words, 'build/w2c.txt')

    nullifier('build/null.txt')

    fetch_symbols(PATHS['slu'], grammar=True)
    flush_symbols()
