#!/usr/bin/make -f

NAME = KanjiVocab
SUBDIR = kanjivocab

ZIP = zip
ZIPFILE = $(NAME).zip


$(ZIPFILE): all
	$(ZIP) $(ZIPFILE) $(NAME).py $(SUBDIR)/*.py

zip: $(ZIPFILE)

all clean:
	$(MAKE) -C $(SUBDIR) $@


.PHONY: all clean zip
.DEFAULT_GOAL := all

