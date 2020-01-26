DIRS := \
	$(shell which cygpath > /dev/null 2>&1 && cygpath "${APPDATA}\\keyhac") \
	$(shell which cygpath > /dev/null 2>&1 && cygpath "\\app\\keyhac")
DIRS := $(foreach dir,$(DIRS),$(shell [ -d $(dir) ] && echo $(dir)))
DIR := $(word 1, $(DIRS))
$(if $(DIR), ,$(error The installation directory is not found))

.PHONY: all install uninstall
all:

install: config.py
	cp $+ $(DIR)

uninstall:
	rm $(DIR)/config.py
