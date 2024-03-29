#!/usr/bin/make -f

NAME = KanjiVocab
SUBDIR = kanjivocab

ZIP = zip
PYUIC4 = pyuic4

BUILD_DIR = build
BUILD_SUBDIR = $(BUILD_DIR)/$(SUBDIR)

GIT_VERSION = $(shell git describe --tags --dirty --always)
GIT_VERSION_FILE = __init__.py

ZIPFILE = $(NAME).zip

UI_SRCS = dialog.ui help.ui
UI_OBJS = $(addprefix $(BUILD_SUBDIR)/,$(UI_SRCS:%.ui=ui_%.py))


build: $(UI_OBJS) | $(BUILD_SUBDIR)
	cp -f $(NAME).py $(BUILD_DIR)/
	cp -f $(SUBDIR)/*.py $(BUILD_SUBDIR)/
	sed -i 's/%GIT_VERSION%/$(GIT_VERSION)/g' $(BUILD_SUBDIR)/$(GIT_VERSION_FILE)

$(BUILD_SUBDIR)/ui_%.py: $(SUBDIR)/%.ui | $(BUILD_SUBDIR)
	$(PYUIC4) $< -o $@

$(BUILD_SUBDIR):
	mkdir -p $(BUILD_SUBDIR)

$(ZIPFILE): build
	cd $(BUILD_DIR) && $(ZIP) ../$(ZIPFILE) $(NAME).py $(SUBDIR)/*.py

zip: $(ZIPFILE)

clean:
	rm -rf $(ZIPFILE) $(BUILD_DIR)


.PHONY: build zip clean

