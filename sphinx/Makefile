# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: sphinx-apidoc
sphinx-apidoc:
	sphinx-apidoc -f -o . -M ../modules/
	# glob でインポートする時に邪魔なので削除
	rm modules.rst
	# rm sandbox.rst

.PHONY: html
# html:
html: sphinx-apidoc # これを追加
	$(SPHINXBUILD) -b html . ../docs/