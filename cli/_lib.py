# Imports
from types import FunctionType as function
from dataclasses import dataclass
import os
import sys

# Constants
_DEFAULT_NAME = os.path.basename(sys.argv[0])


def _get_function_args(f: function, /) -> tuple[list, list, str|None]:
  """Gets the function's parameters."""
  code = f.__code__
  varnames = list(code.co_varnames)
  argcount = code.co_argcount
  n_opts = code.co_kwonlyargcount
  n_optional = len(f.__defaults__ or [])
  n_required = argcount - n_optional
  if code.co_flags & 0x08:
    n_optional -= n_opts
    n_required -= n_opts
  required = varnames[:n_required]
  optional = varnames[n_required : n_required+n_optional]
  if code.co_flags & 0x04:
    arbitrary = varnames[argcount + n_opts]
  else:
    arbitrary = None
  return required, optional, arbitrary


def _to_posix_args(
  required: list,
  optional: list|None = None,
  arbitrary: str|None = None,
) -> str:
  """Returns the POSIX-style representation of the given arguments."""
  def fmt(s: str, prefix: str, suffix: str) -> str:
    return prefix + s.replace('_', ' ').upper() + suffix
  formatted = [fmt(arg, '<', '>') for arg in required]
  if optional:
    formatted += [fmt(arg, '[', ']') for arg in optional]
  if arbitrary:
    formatted.append(fmt(arbitrary, '[', ']...'))
  formatted = ' '.join(formatted)
  return formatted


def _classify_args(items: list[str], /) -> tuple[list, list]:
  """Categorises a list of strings into arguments and flags."""
  args = []
  flags = []
  for i, item in enumerate(items):
    if item == '--':
      args += items[i+1 :]
      break
    elif item.startswith('--'):
      flags.append(item)
    elif item == '-':
      flags.append(item)
    elif item.startswith('-'):
      flags += ['-' + i for i in list(item.removeprefix('-'))]
    else:
      args.append(item)
  return args, flags


class _Table:
  """Helps create tables."""

  def __init__(self):
    self.items: list[tuple[str, str|None]] = []

  def add(self, key: str, value: str|None):
    """Adds a value and/or key to the table."""
    item = (key, value)
    self.items.append(item)

  def build(self) -> str:
    """Builds itself and returns a string."""
    max_key_len = max([len(i[0]) for i in self.items])
    lines = []
    for key, value in self.items:
      if value:
        line = f'{key:<{max_key_len}} - {value}'
        lines.append(line)
      else:
        lines.append(key)
    table = '\n'.join(lines)
    return table


class _HelpPage:
  """Helps create help pages."""

  def __init__(self):
    self.sections = []

  def add(self, title: str|None, body: str|None):
    """Adds a section to the help page."""
    items = []
    if not body:
      return
    if title:
      items.append(title + ':')
      indent = ' ' * 3
      body = indent + body.replace('\n', '\n' + indent)
    items.append(body)
    if items:
      self.sections.append('\n'.join(items))

  def build(self, compact: bool) -> str:
    """Builds itself and returns a string."""
    section_separator = '\n' if compact else '\n\n'
    return section_separator.join(self.sections)


@dataclass
class _Option:
  name: str
  description: str|None
  shorthand: str|None
  call: callable|None

  @property
  def flags(self) -> list:
    items = []
    if self.shorthand:
      items.append('-' + self.shorthand)
    items.append('--' + self.name)
    return items


class CLI:
  """Creates a CLI around a given function or class.

  The `target` can be either a function, to make a single-command CLI,
  or a class, to make a multi-command CLI. Its docstring will be used
  as the CLI's description, shown on the help page.

  If the `target` is a function, then its parameters will be used to
  create the CLI's arguments. Supports required, optional and
  arbitrary parameters.

  If the `target` is a class, then its attributes will be used to
  create the CLI's commands. The `target`'s attributes can be either
  other `CLI`s, functions or classes. If the attribute is a function
  or a class, then a new `CLI` will be created using that attribute;
  the name of this new cli will be set to the parent `CLI`'s name
  plus the name of the attribute, as it appears within the class, with
  a space in the middle. For example, if the parent `CLI`'s name is
  "hello" and the function's name, as it appears in the class, is
  "world", then the name for the new `CLI` created from that
  function will be "hello world". However, if the attribute is already
  a `CLI` then it's name will remain unchanged. All new `CLI`s
  created by this `CLI`, will be added to this `CLI`, under the
  name of the attribute, as it appeared in the class, plus "_command".
  This is done to improve ease of access, for example to enabled
  adding options to these created `CLI`s. This is not done for
  attributes which were already `CLI`s.

  If the `name` is not specified, then `sys.argv[0]` will be used to
  determine the name of the program.

  The `compact_help` parameter decides whether the help page sections
  should be separated by one or two newlines. If not specified, then
  it will be set to `False` if the specified `target` is a function,
  and `True` if it's a class.

  The `child_kwargs` dictionary is passed as keyword arguments to
  children `CLI`s created by this `CLI` (only applies if the
  given `target` is a class).

  The `pass_self` parameter can be set to `True` if you want your
  function to get the `CLI` that was created using it as its first
  argument when running.

  To run the CLI, call it.

  Example single-command CLI:
  ```
  from cli import CLI
  import sys

  def echo(text, **options):
    if options['world']:
      text += ' world!'
    print(echo)

  echo_cli = CLI(echo)
  echo_cli.add_option('world', 'Appends " world!"', 'w')

  if __name__ == '__main__':
    sys.exit(echo_cli())
  ```

  Example multi-command CLI:
  ```
  from cli import CLI
  import sys

  class express:
    def sadness(**opts):
      print("I'm sad")

    def happiness(*, help=False):
      print("I'm happy")

  express_cli = CLI(express)

  if __name__ == '__main__':
    sys.exit(express_cli())
  ```
  """

  def __init__(
    self,
    target: function|type,
    name: str|None = None,
    pass_self: bool = False,
    add_help: bool = True,
    compact_help: bool|None = None,
    child_kwargs: dict|None = None,
  ):
    self.target = target
    self.name = name or _DEFAULT_NAME
    self.description = target.__doc__
    self.pass_self = pass_self
    self.compact_help = compact_help
    self.options = []
    self.add_help = add_help
    self.child_kwargs = child_kwargs or {}
    if add_help:
      self.add_option(
        'help', 'Prints this page.', 'h',
        self.print_help_and_exit,
      )
    if isinstance(target, function):
      self._singlecommand_init()
    elif isinstance(target, type):
      self._multicommand_init()
    else:
      raise TypeError(f'Invalid target type {type(target)}')

  def _singlecommand_init(self):
    self._function_args = _get_function_args(self.target)
    if self.pass_self:
      try:
        self._function_args[0].pop(0)
      except IndexError:
        raise TypeError(f'{self.target} is missing the `self` argument')
    usage = _to_posix_args(*self._function_args)
    self.usage = f'[OPTIONS]... {usage}' if self.options else usage
    self._parse = self._singlecommand_parse
    self._build_help = self._build_singlecommand_help
    if self.compact_help is None:
      self.compact_help = True

  def _multicommand_init(self):
    self.usage = '<COMMAND> ...'
    self._parse = self._multicommand_parse
    self._build_help = self._build_multicommand_help
    if self.compact_help is None:
      self.compact_help = False
    self.commands = {}
    for name, attr in self.target.__dict__.items():
      if name.startswith('_'):
        continue
      command_name = name.replace('_', '-')
      if isinstance(attr, (function, type)):
        command = CLI(
          attr, f'{self.name} {command_name}', **self.child_kwargs,
        )
        setattr(self, name + '_command', command)
        self.commands[command_name] = command
      elif isinstance(attr, CLI):
        self.commands[command_name] = attr
      else:
        raise TypeError(f'Given class has an invalid attribute {attr}')
    if not self.commands:
      raise TypeError('Given class cannot be empty')

  def add_option(
    self,
    name: str,
    description: str|None = None,
    shorthand: str|None = None,
    call: callable|None = None,
  ):
    """Adds an option to the CLI.

    The `name` parameter will used as the key in the `dict` that the
    `parse` method returns and to create the long flag for the CLI.

    The `description` parameter, if specified, will be shown in the
    help page, after the option's flags.

    The `shorthand` parameter, if specified, will be used to create the
    short flag for the CLI. It must be 1 a character-long string.

    The `call` parameter, if specified, will be called during parsing.
    If the option was set by the user. The default help option sets it
    to the `print_help_and_exit` method of the `CLI`.

    When running the CLI, the option will be passed as a keyword
    argument to the appropriate function, if it can accept it.
    """
    if len(name) < 2:
      raise TypeError('Option name must contain at least 2 characters')
    if shorthand:
      if len(shorthand) > 1:
        raise TypeError('Option shorthand must be 1 character long')
    option = _Option(name, description, shorthand, call)
    if self.add_help:
      self.options.insert(-1, option)
    else:
      self.options.append(option)

  def _parse_flags(self, flags: list[str]) -> dict[str: bool]:
    parsed = {}
    flag_to_option = {}
    for option in self.options:
      parsed[option.name] = False
      for f in option.flags:
        flag_to_option[f] = option
    for flag in flags:
      option = flag_to_option.get(flag)
      if not option:
        self.usage_error(f"unknown option '{flag}'")
      parsed[option.name] = True
      if option.call:
        option.call()
    return parsed

  def _singlecommand_parse(self, args: list[str]):
    args, flags = _classify_args(args)
    opts = self._parse_flags(flags)
    required, optional, arbitrary = self._function_args
    n_required = len(required)
    n_optional = len(optional)
    n_args = len(args)
    if n_args < n_required:
      missing_args = required[n_args:]
      missing_args = _to_posix_args(missing_args)
      self.usage_error('missing arguments ' + missing_args)
    if n_args > n_required + n_optional and not arbitrary:
      self.usage_error('too many arguments.')
    return self, args, opts

  def _multicommand_parse(self, args: list[str]):
    flags = []
    for i, arg in enumerate(args):
      if arg.startswith('-'):
        flags.append(arg)
      else:
        command_name = arg
        args = args[i+1 :]
        break
    else:
      command_name = None
      args = []
    local_opts = self._parse_flags(flags)
    if not command_name:
      self.usage_error('no command specified.')
    command = self.commands.get(command_name)
    if not command:
      self.usage_error(f"unknown command '{command_name}'")
    command, args, opts = command._parse(args)
    for key, value in local_opts.items():
      opts.setdefault(key, value)
    return (command, args, opts)

  def __call__(self, args: list[str] = None) -> any:
    """Runs the CLI.

    If `args` is not specified, then `sys.argv[1:]` will be used.
    """
    try:
      if args is None:
        args = sys.argv[1:]
      command, args, opts = self._parse(args)
      accepts_arbitrary_kwargs = command.target.__code__.co_flags & 0x08
      if not accepts_arbitrary_kwargs:
        kwargs = command._function_args[1]
        opts = {k: v for k, v in opts.items() if k in kwargs}
      if command.pass_self:
        args.insert(0, command)
      return command.target(*args, **opts)
    except KeyboardInterrupt:
      print('^C', file=sys.stderr)
      sys.exit(130)

  def warn(self, *lines: str):
    """Prints an error message to stderr."""
    text = f'{self.name}: ' + '\n'.join(lines)
    print(text, file=sys.stderr)

  def error(self, exit_code: int, *lines: str):
    """Prints an error message to stderr and calls `sys.exit` with the
    given exit code.
    """
    self.warn(*lines)
    sys.exit(exit_code)

  def usage_error(self, *lines: str):
    """Prints an error message to stderr and calls `sys.exit` with an
    appropriate exit code.
    """
    lines += (f"Try '{self.name} --help' for more information.",)
    exit_code = getattr(os, 'EX_USAGE', 64)
    self.error(exit_code, *lines)

  def _add_options_to_help_page(self, help_page: _HelpPage):
    table = _Table()
    for option in self.options:
      flags = option.flags
      if len(flags) > 1:
        flags = ', '.join(flags)
      else:
        flags = '    ' + flags[0]
      table.add(flags, option.description)
    text = table.build()
    help_page.add('Options', text)

  def _build_singlecommand_help(self) -> str:
    help_page = _HelpPage()
    # Usage
    help_page.add('Usage', f'{self.name} {self.usage}')
    # Description
    if self.description:
      help_page.add('Description', self.description)
    # Options
    self._add_options_to_help_page(help_page)
    return help_page.build(self.compact_help)

  def _build_multicommand_help(self) -> str:
    help_page = _HelpPage()
    # Description
    if self.description:
      help_page.add(None, self.description)
    # Synopsis
    help_page.add('Synopsis', f'{self.name} {self.usage}')
    # Commands
    commands = _Table()
    for name, command in self.commands.items():
      commands.add(name, command.description)
    commands = commands.build()
    help_page.add('Commands', commands)
    # Usage
    usage = {k: v.usage for k, v in self.commands.items()}
    if any(usage.values()):
      usage = '\n'.join([f'{k} {v}' for k, v in usage.items()])
      help_page.add('Usage', usage)
    # Options
    self._add_options_to_help_page(help_page)
    return help_page.build(self.compact_help)

  def build_help(self) -> str:
    """Builds the help page."""
    return self._build_help()

  def print_help(self):
    """Prints the help page."""
    print(self.build_help())

  def print_help_and_exit(self):
    """Prints the help page and calls `sys.exit` with the appropriate
    exit code.
    """
    self.print_help()
    exit_code = getattr(os, 'EX_OK', 0)
    sys.exit(exit_code)


def cli(
  name: str|None = None,
  pass_self: bool = False,
  add_help: bool = True,
  compact_help: bool|None = None,
  child_kwargs: dict|None = None,
) -> callable:
  """Returns a decorator that takes either a function or a class and
  returns a `CLI`.

  Example usage:
  ```
  @cli
  def echo(text):
    print(text)
  ```

  or
  ```
  @cli(name='echo')
  def main(text):
    print(text)
  ```
  """
  name_is_target = isinstance(name, (function, type))
  if name_is_target:
    target = name
  if not name or name_is_target:
    name = _DEFAULT_NAME
  def decorator(target) -> CLI:
    return CLI(
      target, name, pass_self, add_help, compact_help, child_kwargs,
    )
  if name_is_target:
    return decorator(target)
  return decorator
