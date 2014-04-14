BUILD_DIR = build/
SYMBOLS_PATH = build/symbols.lex

ATIS = atis/atis.hlti.100.train


.PHONY: default simple clean parser

default: parser

atis: clean parser
	farcompilestrings -u "<unk>" -i $(SYMBOLS_PATH) $(ATIS) > $(BUILD_DIR)/input.far
	cp atis/atis.hlti.100.dev $(BUILD_DIR)/golden.txt

test:
	cd $(BUILD_DIR); \
	farfilter "fsmcompose - tagger.fst | fsmbestpath | fsmrmepsilon" < input.far > output.far; \
	farfilter "fsmprint -i symbols.lex -o symbols.lex - | cut -f 3,4" <output.far > tagged.txt
	./compare_outputs.py $(BUILD_DIR)/tagged.txt $(BUILD_DIR)/golden.txt > $(BUILD_DIR)/comparison.txt


parser: clean
	./build_parser.py

clean:
	rm -rf $(BUILD_DIR)/*