# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
import cloud_sptheme as csp


# -- Project information -----------------------------------------------------

project = 'iMath'
copyright = '2023, Roie R. Black'
author = 'Roie R. Black'

release = '0.1.0'


# -- General configuration ---------------------------------------------------

extensions = [
        'sphinx_ext.wordcount',
        'sphinx.ext.autodoc',
        'sphinx.ext.viewcode',
        'sphinx.ext.autosummary',
        'sphinx_ext.tikzimage',
        'sphinx_ext.pylit',
]

# Sphinx_ext.tikzimage extension
# needs brew install poppler
tikz_proc_suite = 'ImageMagick'
tikz_latex_preamble = r"""
\usepackage{amsmath}
"""

autodoc_member_order = "bysource"
autodoc_default_options = {
        "members": True,
        "show_inheritance": True
        }
autosummary_generate = True

linkcheck_timeout = 3
linkcheck_retries = 2
spelling_list_filename = ['spelling_wordlist.txt']
spelling_lang='en_US'

master_doc = 'index'
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

rst_prolog = """
..  include::   /header.inc
"""


# -- Options for HTML output -------------------------------------------------

html_theme = 'cloud'
html_theme_path = [csp.get_theme_dir()]
html_theme_options = { "roottarget": "index" }


html_static_path = ['_static']

