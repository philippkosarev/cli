# Imports
from copy import deepcopy
import os
import sys
import tomllib
import collections
import platformdirs


def _merge_dicts(src: dict, dst: dict) -> dict:
  """Overlays the `dst` dict on top of the `src` dict."""
  for key, value in src.items():
    if isinstance(value, dict):
      node = dst.setdefault(key, {})
      _merge_dicts(value, node)
    else:
      dst[key] = value
  return dst


class Secretary:
  """Program config file manager.

  This class is functionally a wrapper around the `user_config_dir`
  function of the `platformdirs` module, but with the addition of the
  `file` method.

  The `ensure_exists` option is passed down to `File`s created by the
  `file` method, if not specified otherwise.
  """

  def __init__(
    self,
    program: str,
    author: str = None,
    version: str = None,
    roaming: bool = False,
    ensure_exists: bool = False,
  ):
    self.directory = platformdirs.user_config_dir(
      program, author, version, roaming, ensure_exists,
    )
    self.ensure_exists = ensure_exists
    self.program = program

  def file(
    self,
    name: str,
    defaults: dict = {},
    template: str = '',
    ensure_exists: bool = None,
    exit_on_error: bool = True,
  ) -> File:
    """Creates a new configuration `File`."""
    file = os.path.join(self.directory, name + '.toml')
    if ensure_exists is None:
      ensure_exists = self.ensure_exists
    file = File(file, template, defaults, ensure_exists, exit_on_error)
    return file


class File(collections.UserDict):
  """A program configuration file.

  Derived from the `collections.UserDict` class, so it can be used like
  a regular dictionary.
  """

  def __init__(
    self,
    file,
    template: str,
    defaults: dict,
    ensure_exists: bool,
    exit_on_error: bool,
  ):
    self.file = os.fspath(file)
    self.template = template
    self.defaults = defaults
    self.ensure_exists = ensure_exists
    self.exit_on_error = exit_on_error
    self.reload()

  def reload(self):
    """Updates the config by reading it from the file."""
    if self.exit_on_error:
      try:
        data = self._reload()
      except OSError as e:
        self.error(e.args[1] + '.')
      except tomllib.TOMLDecodeError as e:
        self.error(str(e) + '.')
    else:
      data = self._reload()
    self.data = _merge_dicts(data, deepcopy(self.defaults))

  def _reload(self) -> dict:
    if self.ensure_exists:
      if not os.path.isfile(self.file):
        with open(self.file, 'w') as fp:
          fp.write(self.template)
    if os.path.isfile(self.file):
      with open(self.file, 'rb') as fp:
        return tomllib.load(fp)
    else:
      return {}

  def error(self, *lines: str):
    """Prints an error message to stderr and calls `sys.exit` with an
    appropriate exit code.
    """
    home = os.path.expanduser('~')
    short_path = self.file.replace(home, '~')
    print(
      f'Configuration error in {short_path}:\n' + '\n'.join(lines),
      file=sys.stderr,
    )
    exit_code = getattr(os, 'EX_CONFIG', 78)
    sys.exit(exit_code)
