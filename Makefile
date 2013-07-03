#!/usr/bin/make -f

.DEFAULT_GOAL := all

zip:
	zip KanjiVocab KanjiVocab.py kanjivocab/*.py

%:
	$(MAKE) -C kanjivocab $@

