#! /usr/bin/env python

import pdb

f = open('unigrams.count.txt', 'r')


cont = f.readlines()
l = len(cont)

unigrams = {}
for line in cont:
	count, word = line.split()
	unigrams[word] = int(count)

prob_unigrams = {}
for w in unigrams:
	prob_unigrams[w] = float(unigrams[w]) / len(unigrams)

with open('unigrams.prob.txt', 'w') as o:
	for k in unigrams:
		o.write("{}\t{}\n".format(k, prob_unigrams[k]))

bigrams = {}

bigrams_raw = open('bigrams.count.txt', 'r').readlines()

for line in bigrams_raw:
	count, w1, w2 = line.split()
	bigrams[w1] = bigrams.get(w1, {})
	bigrams[w1][w2] = count
	

prob_bigrams = {}

for w1 in bigrams:
	for w2 in bigrams[w1]:
		prob_bigrams[w1] = prob_bigrams.get(w1, {})
		prob_bigrams[w1][w2] = float(bigrams[w1][w2]) / unigrams[w1]

with open('bigrams.prob.txt', 'w') as o:
	for w1 in prob_bigrams:
		for w2 in prob_bigrams[w1]:
			o.write("{}\t{}\t{}\n".format(w1, w2, prob_bigrams[w1][w2]))

# print "p(the | of) = {}".format(prob_bigrams["of"]["the"])
# print "p(the | .) = {}".format(prob_bigrams["."]["the"])
# print "p(general | the) = {}".format(prob_bigrams["the"]["general"])
# print "p(* | right) = {}".format(
# 	reduce(lambda acc, x: acc + x,
# 		prob_bigrams["right"].values()
# 	)
# )