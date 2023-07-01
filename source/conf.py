# Configuration file for the Sphinx documentation builder.
#
import os
import sys
sys.path.insert(0, os.path.abspath("../"))
sys.path.insert(0, os.path.abspath("../other_code"))
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Projet_Final'
copyright = '2023, Group_L'
author = 'Group_L'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions =  ["sphinx.ext.autodoc"]


templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
