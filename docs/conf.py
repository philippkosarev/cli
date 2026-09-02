# Imports
import os
import sys
import pypandoc

# Project information
project = 'CLI'
author = 'Philipp Kosarev'
copyright = f'2026, {author}'
language = 'en'

# Adding module to PATH
script_dir = os.path.dirname(__file__)
module_dir = os.path.dirname(script_dir)
sys.path.append(module_dir)

# Paths
templates_path = ['templates']
exclude_patterns = ['build']

# Extensions
extensions = [
  'sphinx.ext.autodoc',
  'sphinx_copybutton',
  'sphinx_toolbox.more_autodoc.variables',
  'sphinxcontrib.programoutput',
]

# Defaults
autodoc_default_options = {
  'members': True,
  'member-order': 'bysource',
}

# HTML theme options
html_theme = 'pydata_sphinx_theme'
html_static_path = ['static']
html_css_files = ['style.css']
html_sidebars = { '**': []}
html_theme_options = {
  'secondary_sidebar_items': [],
  'pygments_light_style': 'tango',
  'pygments_dark_style': 'monokai',
  'icon_links': [
    {
      'name': 'GitHub',
      'url': 'https://github.com/philippkosarev/cli',
      'icon': 'fa-brands fa-github',
      'type': 'fontawesome',
    },
  ]
}

# Hooks and directives
def process_docstring(app, what, name, obj, options, lines):
  """Converts markdown docstrings to ReST."""
  md  = '\n'.join(lines)
  rst = pypandoc.convert_text(md, 'rst', 'markdown')
  lines[:] = rst.splitlines()

# Connecting hooks
def setup(app):
  app.connect('autodoc-process-docstring', process_docstring)
