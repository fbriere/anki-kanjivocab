#!/usr/bin/make -f

NAME = KanjiVocab
SUBDIR = kanjivocab

ZIP = zip
PYUIC4 = pyuic4

BUILD_DIR = build
BUILD_SUBDIR = $(BUILD_DIR)/$(SUBDIR)

ZIPFILE = $(NAME).zip

UI_SRCS = dialog.ui help.ui
UI_OBJS = $(addprefix $(BUILD_SUBDIR)/,$(UI_SRCS:%.ui=ui_%.py))


build: $(UI_OBJS) | $(BUILD_SUBDIR)
	cp -f $(NAME).py $(BUILD_DIR)/
	cp -f $(SUBDIR)/*.py $(BUILD_SUBDIR)/

$(BUILD_SUBDIR)/ui_%.py: $(SUBDIR)/%.ui | $(BUILD_SUBDIR)
	$(PYUIC4) $< -o $@

$(BUILD_SUBDIR):
	mkdir -p $(BUILD_SUBDIR)

$(ZIPFILE): build
	cd $(BUILD_DIR) && $(ZIP) ../$(ZIPFILE) --recurse-paths *

zip: $(ZIPFILE)

clean:
	rm -rf $(ZIPFILE) $(BUILD_DIR)


.PHONY: build zip clean

