# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'Conway’s Game of Life'
copyright = '2025, Shehab and Darya'
author = 'Shehab and Darya'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.napoleon','sphinx.ext.autodoc','sphinx.ext.viewcode']

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']


latex_documents = [
    ('index', 'Conway.tex', 'Conway\'s Game of Life Documentation',
     'Shehab and Darya', 'howto'),
]

# Optional to reduce whitespace
latex_elements = {
    'preamble': r'''
        \usepackage{parskip}
        \setlength{\parskip}{0.5em}
        \setlength{\parindent}{0pt}
    ''',
    'classoptions': ',oneside',  # avoid blank left pages in two-sided layout
}
latex_logo = "game_window-of-life.png"