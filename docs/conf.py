# Imports
import os
import sys
import pypandoc

# Project information
project = 'libjam'
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
]

# Default autodoc options
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
  'show_nav_level': 0,
  'navigation_depth': 3,
  'collapse_navigation': False,
  'pygments_light_style': 'gruvbox-light',
  'pygments_dark_style': 'zenburn',
  'icon_links': [
    {
      'name': 'GitHub',
      'url': 'https://github.com/philippkosarev/libjam',
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
