#! /bin/sh

INPUT=toycorpus.txt
CORPUS=toycorpus.lc.txt

LEXICON=lexicon.txt

DEFAULT_DIR=default
SENTENCETAGS_DIR=sentence_tags
NOSTOPWORDS_DIR=no_stopwords

# create count & probabilities files
# count(working_dir)
function count {
	DIR=$1

	mkdir -p "$DIR"
	pushd "$DIR"
	# Create a lexicon file if doesn't exist
	if [ ! -f $LEXICON ]; then
		if [ -f $CORPUS ]; then
			tr " " "\n" < $CORPUS > $LEXICON
		else
			tr " " "\n" < ../$CORPUS > $LEXICON
		fi
	fi
	
	# Count unigrams
	sort $LEXICON | uniq -c | sort -gr > unigrams.count.txt

	# Count bigrams
	cp $LEXICON word1.txt
	tail -n +2 word1.txt > word2.txt
	paste word1.txt word2.txt > tmp.txt
	sed '$ d' < tmp.txt > bigrams.txt # delete the last line
	sort bigrams.txt | uniq -c | sort -gr > bigrams.count.txt

	# Count trigrams
	tail -n +2 word2.txt > word3.txt
	paste word1.txt word2.txt word3.txt > tmp.txt
	sed '$ d' < tmp.txt | sed '$ d' > trigrams.txt # delete the last 2 lines
	sort trigrams.txt | uniq -c | sort -gr > trigrams.count.txt

	rm word1.txt word2.txt word3.txt tmp.txt

	../prob.py
	popd
}


platform='unknown'
unamestr=`uname`
if [[ "$unamestr" == 'Darwin' ]]; then
	echo "You are using Mac OS. Make sure you have GNU grep installed and aliased to \"ggrep\" (e.g. brew install grep)"
	GREP=ggrep
else
	GREP=grep
fi

# To lower case
tr '[:upper:]' '[:lower:]' < $INPUT > $CORPUS

# Default count & probabilities
count $DEFAULT_DIR

# Count & probabilities of unigrams w/o stopwords
mkdir -p "$NOSTOPWORDS_DIR"
$GREP -Fxvf english.stop.txt < $DEFAULT_DIR/$LEXICON > $NOSTOPWORDS_DIR/$LEXICON
count $NOSTOPWORDS_DIR

# Count & probabilities of unigrams w/ sentence tags
mkdir -p "$SENTENCETAGS_DIR"
(while read line ; do echo "<s> ${line} </s>"; done) < $CORPUS > $SENTENCETAGS_DIR/$CORPUS
count $SENTENCETAGS_DIR

