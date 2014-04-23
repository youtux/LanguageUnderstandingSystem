BUILD_DIR = build
SCRIPTS_DIR = scripts
TMP = $(BUILD_DIR)/tmp

SLU_PATH = automatons/slu.txt
W2C_PATH = build/w2c.txt
SYMBOLS_PATH = build/symbols.lex

# Input file path. Feel free to change it
INPUT_WL = atis/custom.wl
INPUT_REFERENCE = atis/custom.tagged


.PHONY: default from_wl from_tagged clean parser build_wl build_far test

default: from_tagged

from_tagged: build_wl from_wl compare_results
from_wl: build_far parser test

# creates the sentences file starting from a tagged sentences file
build_wl:
	$(SCRIPTS_DIR)/build_wordlist_from_tagged.py $(INPUT_REFERENCE) > $(INPUT_WL)

# creates the input fararchive
build_far: parser
	farcompilestrings -u "<unk>" -i $(SYMBOLS_PATH) $(INPUT_WL) > $(BUILD_DIR)/input.far
	cp $(INPUT_REFERENCE) $(BUILD_DIR)/golden.txt

test:
	farfilter "fsmcompose - $(BUILD_DIR)/tagger.fst | fsmbestpath | fsmrmepsilon" < "$(BUILD_DIR)/input.far" > "$(BUILD_DIR)/output.far"
	farfilter "fsmprint -i $(SYMBOLS_PATH) -o $(SYMBOLS_PATH) - | cut -f 3,4" < "$(BUILD_DIR)/output.far" > "$(BUILD_DIR)/tagged.txt"

compare_results:
	$(SCRIPTS_DIR)/compare_outputs.py $(BUILD_DIR)/tagged.txt $(BUILD_DIR)/golden.txt > $(BUILD_DIR)/comparison.txt


parser: clean
	# Build the w2c.txt, null.txt and add all the needed symbols in the symbols file
	$(SCRIPTS_DIR)/build_parser.py

	# First pass compile grammar
	grmread -i $(SYMBOLS_PATH) -c -w $(SLU_PATH) > $(TMP)/slu.fst
	grmcfapproximate -i $(SYMBOLS_PATH) -o $(TMP)/symbols.lex -s S $(TMP)/slu.fst > $(BUILD_DIR)/slu.txt
	mv $(TMP)/symbols.lex $(SYMBOLS_PATH)

	# Convert into a regular grammar
	grmread -i $(SYMBOLS_PATH) -c -w $(BUILD_DIR)/slu.txt > $(BUILD_DIR)/slu.fst
	grmcfcompile -i $(SYMBOLS_PATH) -s S -O 2 $(BUILD_DIR)/slu.fst > $(BUILD_DIR)/slu.fsa

	# Compile the w2c
	fsmcompile -t -i $(SYMBOLS_PATH) -o $(SYMBOLS_PATH) $(BUILD_DIR)/w2c.txt > $(BUILD_DIR)/w2c.fst

	# Compile the nullifier
	fsmcompile -t -i $(SYMBOLS_PATH) -o $(SYMBOLS_PATH) $(BUILD_DIR)/null.txt > $(BUILD_DIR)/null.fst

	# Compose w2c + slu -> tagger
	# fsmcompose $(BUILD_DIR)/w2c.fst $(BUILD_DIR)/slu.fsa > $(BUILD_DIR)/tagger.fst
	fsmcompose $(BUILD_DIR)/w2c.fst $(BUILD_DIR)/slu.fsa $(BUILD_DIR)/null.fst > $(BUILD_DIR)/tagger.fst

	# Just a bit of optimization
	fsmrmepsilon $(BUILD_DIR)/tagger.fst > $(TMP)/tagger.fst
	mv $(TMP)/tagger.fst $(BUILD_DIR)/tagger.fst


clean:
	rm -rf $(BUILD_DIR)/*