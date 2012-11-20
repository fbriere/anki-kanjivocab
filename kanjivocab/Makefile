#!/usr/bin/make -f

PYUIC4 = pyuic4

SRCS = dialog.ui help.ui

OBJS = $(SRCS:%.ui=ui_%.py)

all: $(OBJS)

clean:
	rm -f $(OBJS) *.pyc

ui_%.py: %.ui
	$(PYUIC4) $< -o $@

.PHONY: all clean
