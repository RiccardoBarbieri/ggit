# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('..'))


project = 'ggit'
copyright = '2022, Riccardo Barbieri'
author = 'Riccardo Barbieri'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc', 
    'sphinx.ext.coverage', 
    'sphinx.ext.napoleon', 
    'sphinx_rtd_theme',
    'sphinx.ext.autosummary'
]

autodoc_default_flags = ['members']
autosummary_generate = True


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

master_doc = 'index'


html_theme = 'sphinx_rtd_dark_mode'
default_dark_mode = True
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['']

html_theme_options = {
    'collapse_navigation': False,
    'navigation_depth': -1,
}
