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
html_theme = 'shibuya'
html_static_path = ['static']
html_css_files = ['style.css']
html_sidebars = { '**': []}
html_theme_options = {
  'page_layout': 'simple',
  'accent_color': 'blue',
  'nav_socials': [{
      'name': 'GitHub',
      'url': 'https://github.com/philippkosarev/cli',
      'icon': 'simple-icons:github',
  }],
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
