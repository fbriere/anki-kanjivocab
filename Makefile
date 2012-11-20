#!/usr/bin/make -f

.DEFAULT_GOAL := all

%:
	$(MAKE) -C kanjivocab $@

