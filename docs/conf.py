"""Sphinx configuration."""
project = "Zeigen"
author = "Joel Berendzen"
copyright = "2022, Joel Berendzen"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
