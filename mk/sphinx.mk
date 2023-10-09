.PHONY:	docs
docs:	changes  ## run Sphinx to build html pages
	cd rst && \
	sphinx-build -b html -d _build/doctrees . ../docs

