from importlib.metadata import version as _version

project = "SchemaScribe"
author = "Friedrich Urban, Julian Wirtz, Julius Halank, Moritz Rätz"
release = _version("schema-scribe")
version = release

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
]

autodoc_member_order = "bysource"
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

html_theme = "furo"
html_title = "SchemaScribe"
html_theme_options = {
    "source_repository": "https://github.com/EcoWeaver/SchemaScribe/",
    "source_branch": "main",
    "source_directory": "docs/",
}