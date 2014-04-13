BUILD_DIR = build/
SYMBOLS_PATH = build/symbols.lex

SIMPLE = simple/simple.train
ATIS = atis/atis.hlti.100.train


.PHONY: default simple clean parser

default: parser

atis: clean parser
	farcompilestrings -u "<unk>" -i $(SYMBOLS_PATH) $(ATIS) > $(BUILD_DIR)/input.far

simple: clean parser
	farcompilestrings -u "<unk>" -i $(SYMBOLS_PATH) $(SIMPLE) > $(BUILD_DIR)/input.far
test:
	cd build; \
	farfilter "fsmcompose - tagger.fst | fsmrmepsilon | fsmbestpath" < input.far > output.far; \
	farfilter "fsmprint -i symbols.lex -o symbols.lex - | cut -f 3,4" <output.far > tagged.txt


parser: clean
	./build_parser.py

clean:
	rm -rf build/*