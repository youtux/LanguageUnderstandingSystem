#! /usr/bin/env python

import pdb

f = open('unigrams.count.txt', 'r')


cont = f.readlines()
l = len(cont)

unigrams = {}
for line in cont:
	count, word = line.split()
	unigrams[word] = int(count)

prob_unigrams = {w: float(unigrams[w]) / len(unigrams) for w in unigrams}
with open('unigrams.prob.txt', 'w') as o:
	for k in unigrams:
		o.write(f"{k}\t{prob_unigrams[k]}\n")

bigrams = {}

bigrams_raw = open('bigrams.count.txt', 'r').readlines()

for line in bigrams_raw:
	count, w1, w2 = line.split()
	bigrams[w1] = bigrams.get(w1, {})
	bigrams[w1][w2] = count


prob_bigrams = {}

for w1, value in bigrams.items():
	for w2 in value:
		prob_bigrams[w1] = prob_bigrams.get(w1, {})
		prob_bigrams[w1][w2] = float(bigrams[w1][w2]) / unigrams[w1]

with open('bigrams.prob.txt', 'w') as o:
	for w1, value_ in prob_bigrams.items():
		for w2 in value_:
			o.write(f"{w1}\t{w2}\t{prob_bigrams[w1][w2]}\n")

# print "p(the | of) = {}".format(prob_bigrams["of"]["the"])
# print "p(the | .) = {}".format(prob_bigrams["."]["the"])
# print "p(general | the) = {}".format(prob_bigrams["the"]["general"])
# print "p(* | right) = {}".format(
# 	reduce(lambda acc, x: acc + x,
# 		prob_bigrams["right"].values()
# 	)
# )