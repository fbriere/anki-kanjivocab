#!/usr/bin/make -f

NAME = KanjiVocab
SUBDIR = kanjivocab

ZIP = zip
ZIPFILE = $(NAME).zip


$(ZIPFILE): all
	$(ZIP) $(ZIPFILE) $(NAME).py $(SUBDIR)/*.py

zip: $(ZIPFILE)

all clean::
	$(MAKE) -C $(SUBDIR) $@

clean::
	rm -f $(ZIPFILE) *.pyc


.PHONY: all clean zip
.DEFAULT_GOAL := all

