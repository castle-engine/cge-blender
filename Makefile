# This Makefile contains a couple of useful commands for developing these
# scripts (esp. on Unix). Normal users don't need this,
# there no need to compile etc. Python scripts --- just copy them
# to your Blender scripts directory.

# Cleans .pyc files, both here and inside ~/.blender/scripts/
# (in case you installed the scripts).
.PHONY: clean
clean:
	rm -f *.pyc
	rm -f ~/.blender/scripts/kambi_vrml97_export.pyc
	rm -f ~/.blender/scripts/kanim_export.pyc
	rm -f ~/.blender/scripts/kambi_vrml97_export_base.pyc

# Install makes symlinks to the current script source (in this dir) from
# ~/.blender/scripts. This is only on Unixes, and is useful for developing
# the scripts.
.PHONY: install
install:
	ln -s $(shell pwd)/kambi_vrml97_export.py       ~/.blender/scripts/kambi_vrml97_export.py
	ln -s $(shell pwd)/kanim_export.py		~/.blender/scripts/kanim_export.py
	ln -s $(shell pwd)/kambi_vrml97_export_base.py	~/.blender/scripts/kambi_vrml97_export_base.py

.PHONY: uninstall
uninstall:
	rm -f ~/.blender/scripts/kambi_vrml97_export.py
	rm -f ~/.blender/scripts/kanim_export.py
	rm -f ~/.blender/scripts/kambi_vrml97_export_base.py
