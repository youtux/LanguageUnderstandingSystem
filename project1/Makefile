BUILD_DIR = build
SYMBOLS_PATH = build/symbols.lex

INPUT_WL = atis/custom
INPUT_TAGGED = atis/custom.tagged


.PHONY: default simple clean parser build_wl build_far

default: parser

build_wl:
	./build_wordlist_from_tagged.py $(INPUT_TAGGED) > $(INPUT_WL)

build_far: parser
	farcompilestrings -u "<unk>" -i $(SYMBOLS_PATH) $(INPUT_WL) > $(BUILD_DIR)/input.far
	cp $(INPUT_TAGGED) $(BUILD_DIR)/golden.txt

test:
	farfilter "fsmcompose - $(BUILD_DIR)/tagger.fst | fsmbestpath | fsmrmepsilon" < "$(BUILD_DIR)/input.far" > "$(BUILD_DIR)/output.far"
	farfilter "fsmprint -i $(SYMBOLS_PATH) -o $(SYMBOLS_PATH) - | cut -f 3,4" < "$(BUILD_DIR)/output.far" > "$(BUILD_DIR)/tagged.txt"
	./compare_outputs.py $(BUILD_DIR)/tagged.txt $(BUILD_DIR)/golden.txt > $(BUILD_DIR)/comparison.txt


parser: clean
	./build_parser.py

clean:
	rm -rf $(BUILD_DIR)/*