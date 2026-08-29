"""Provides functionality for making fancy terminal output."""

# Imports
import os
import sys
import contextlib
import collections

# Constants
ESC = chr(0x1B)
CSI = ESC + '['


# Making more verbose print functions
_print = print


def print(text: str, flush: bool = False):
  """Prints `text` to stdout, without a newline."""
  _print(text, file=sys.stdout, end='', flush=flush)


def println(text: str = '', flush: bool = False):
  """Prints `text` to stdout, with a newline."""
  _print(text, file=sys.stdout, end='\n', flush=flush)


def eprint(text: str, flush: bool = False):
  """Prints `text` to stderr, without a newline."""
  _print(text, file=sys.stderr, end='', flush=flush)


def eprintln(text: str = '', flush: bool = False):
  """Prints `text` to stderr, with a newline."""
  _print(text, file=sys.stderr, end='\n', flush=flush)


def indent(string: str, prefix: str = '  ') -> str:
  """Indents the given string using the given prefix."""
  return prefix + string.replace('\n', '\n' + prefix)


def to_columns(
  items: list[str],
  n_columns: int = 0,
  column_sep: str = '  ',
  prefix: str = '  ',
) -> str:
  """Arranges a list of strings in columns.

  If `n_columns` is not set, it will be calculated based on the size
  of the terminal.
  """
  items = [str(item) for item in items]
  items_by_len = sorted(items, key=len, reverse=True)
  n_items = len(items)
  # Calculating n_columns
  if not n_columns:
    try:
      term_width = os.get_terminal_size()[0]
    except OSError:
      return '\n'.join(items)
    available_width = term_width - len(prefix)
    n_columns = 1
    for i in range(2, n_items + 2):
      selected_items = items_by_len[:i]
      text = column_sep.join(selected_items)
      if len(text) > available_width:
        n_columns = i - 1
        break
    else:
      n_columns = n_items
  # Making a list of columns, equalising string length in each column
  # and adding a separator between columns
  columns = [items[i::n_columns] for i in range(n_columns)]
  for i, column in enumerate(columns[:n_columns - 1]):
    column_width = len(max(column, key=len))
    for j, item in enumerate(column):
      columns[i][j] = item + ' ' * (column_width - len(item)) + column_sep
  # Adding the prefix to the first column
  for i, item in enumerate(columns[0] if columns else []):
    columns[0][i] = prefix + item
  # Combining into a string
  n_rows = len(columns[0]) if columns else 0
  lines = []
  for i in range(n_rows):
    line = []
    for column in columns:
      if i < len(column):
        line.append(column[i])
    line = ''.join(line)
    lines.append(line)
  return '\n'.join(lines)


# CSI strings
class CSICommand(collections.UserString):
  """A Control Sequence Introducer (CSI) command string."""

  def __init__(self, s: str):
    self.data = f'{CSI}{s}'

  def __add__(self, other) -> str:
    return self.data + other


hide_cursor = CSICommand('?25l')
"""Hides the cursor."""
show_cursor = CSICommand('?25h')
"""Reveals the cursor."""


@contextlib.contextmanager
def hidden_cursor(flush: bool = False):
  """A context manager that hides the cursor."""
  try:
    eprint(hide_cursor, flush=flush)
    yield
  finally:
    eprint(show_cursor, flush=flush)


try:
  import termios

  def hide_input():
    """Hides what the user is typing.

    Only works on systems where termios is available.
    """
    stdin_fileno = sys.stdin.fileno()
    attributes = termios.tcgetattr(stdin_fileno)
    attributes[3] &= ~termios.ECHO
    attributes[3] &= ~termios.ICANON
    termios.tcsetattr(stdin_fileno, termios.TCSANOW, attributes)

  def show_input():
    """Reveals what the user is typing.

    Only works on systems where termios is available.
    """
    stdin_fileno = sys.stdin.fileno()
    attributes = termios.tcgetattr(stdin_fileno)
    attributes[3] |= termios.ECHO
    attributes[3] |= termios.ICANON
    termios.tcsetattr(stdin_fileno, termios.TCSANOW, attributes)

except ModuleNotFoundError:
  def hide_input():
    """Hides what the user is typing.

    Only works on systems where termios is available.
    """
    pass

  def show_input():
    """Reveals what the user is typing.

    Only works on systems where termios is available.
    """
    pass


@contextlib.contextmanager
def hidden_input():
  """A context manager that hides user input."""
  try:
    hide_input()
    yield
  finally:
    show_input()


# Clear sequences
class ClearSequence(CSICommand):
  """A CSI command that clears some part of the screen when printed."""

  def __init__(self, char: str, n: int):
    super().__init__(f'{n}{char}')


clear_line = ClearSequence('K', 2)
"""Clears the whole line."""
clear_line_from_cursor = ClearSequence('K', 0)
"""Clears the line starting from the cursor."""
clear_line_before_cursor = ClearSequence('K', 1)
"""Clears the line up to the cursor."""
clear_page = ClearSequence('J', 2)
"""Clears the whole page."""
clear_page_from_cursor = ClearSequence('J', 0)
"""Clears the page starting from the cursor."""
clear_page_before_cursor = ClearSequence('J', 1)
"""Clears the page up to the cursor."""
clear_history = ClearSequence('J', 3)
"""Clears the scrollback buffer."""


class StatusBar:
  """A context manager that prints the `status` to stderr on entry and
  clears it on exit.

  If the `status` message is bigger than the user's terminal, then only
  a part of it will be printed, so that it fits cleanly onto one line
  in the user's terminal, maintaining the appearance of a bar.

  Usage example:
  ```
  with StatusBar('Configuring Foo...') as status:
    configure_foo()
    status.update('Configuring Bar')
    configure_bar()
  ```
  """

  def __init__(self, status: str):
    self.status = status

  def _build(self):
    term_width = os.get_terminal_size(sys.stderr.fileno())[0]
    return clear_page_from_cursor + self.status[:term_width] + '\r'

  def update(self, status: str = None):
    """Updates the status bar."""
    if status is not None:
      self.status = status
    if os.isatty(sys.stderr.fileno()):
      eprint(self._build(), True)

  def __enter__(self):
    if os.isatty(sys.stderr.fileno()):
      hide_input()
      eprint(hide_cursor + self._build(), True)
    return self

  def __exit__(self, *exc):
    if os.isatty(sys.stderr.fileno()):
      eprint(clear_page_from_cursor + show_cursor, True)
      show_input()


class ProgressBar:
  """A context manager that prints a progress bar to stderr on entry
  and clears it on exit.

  If the `status` message is bigger than the user's terminal, then only
  a part of it will be printed, so that it fits cleanly onto one line
  in the user's terminal, maintaining the appearance of a bar.

  Example usage:
  ```
  with ProgressBar('Fooing 3 Bars', 0, 3) as progress_bar:
    for i in range(1, 4):
      foo(bar)
      progress_bar.update(i)
  ```
  """

  def __init__(
    self,
    status: str,
    done: int = 0,
    todo: int = 0,
    symbols: str = '[= ]',
  ):
    self.status = status
    self.symbols = symbols
    self._done = done
    self._todo = todo
    self._bar = StatusBar(self._build())

  def _build(self) -> str:
    available_width = os.get_terminal_size(sys.stderr.fileno())[0]
    # Calculating the progress float
    try:
      progress_float = self._done / self._todo
      progress_float = min(max(progress_float, 0), 1)
    except ZeroDivisionError:
      progress_float = 0
    items = []
    # Printing the status
    items.append(self.status)
    available_width -= len(self.status)
    # Adding the percentage
    if available_width >= 5:
      percentage = str(int(progress_float * 100))
      items.append(f' {percentage:>3}%')
      available_width -= 5
    # Adding the progress bar
    if available_width >= 8:
      bar_width = min(available_width - 3, 30)
      filled = int(progress_float * bar_width)
      empty = bar_width - filled
      bar = (
        ' '
        + self.symbols[0]
        + self.symbols[1] * filled
        + self.symbols[2] * empty
        + self.symbols[3]
      )
      items.append(bar)
      available_width -= bar_width + 3
    # Final formatting
    items[0] += ' ' * available_width
    return ''.join(items)

  def update(self, done: int = None, todo: int = None):
    """Updates the progress bar."""
    if done is not None:
      self._done = done
    if todo is not None:
      self._todo = todo
    if os.isatty(sys.stderr.fileno()):
      self._bar.update(self._build())

  def __enter__(self):
    self._bar.__enter__()
    return self

  def __exit__(self, *exc):
    self._bar.__exit__(*exc)


# Navigation sequences
class NavigationSequence(CSICommand):
  """A CSI command that moves the cursor or view when printed.

  You can call instances of this class to get a modified version. For
  example, to get a string that moves the cursor up by 50 lines,
  instead of doing something like `up * 50`, which would produce this:
  ```
  '\x1b[1\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A'
  ```
  You can simply call `up(50)` to get this:
  ```
  '\x1b[50A'
  ```
  """

  def __init__(self, char: str, n: int = 1):
    super().__init__(f'{n}{char}')
    self._char = char

  def __call__(self, n: int) -> str:
    return f'{CSI}{n}{self._char}'


up = NavigationSequence('A')
"""Moves the cursor up."""
down = NavigationSequence('B')
"""Moves the cursor down."""
left = NavigationSequence('D')
"""Moves the cursor left."""
right = NavigationSequence('C')
"""Moves the cursor right."""
prev_line = NavigationSequence('F')
"""Moves the cursor to the previous line."""
next_line = NavigationSequence('E')
"""Moves the cursor to the next line."""
view_up = NavigationSequence('S')
"""Scrolls the view up."""
view_down = NavigationSequence('T')
"""Scrolls the view down."""


# SGR sequences
class Style(collections.UserString):
  """A CSI command that selects the grahpic rendition (SGR).

  Example usage:
  ```
  bold = Style(1, 22)
  print(bold('This text is bold!'))

  underline = Style(4, 24)
  print(underline('This text is underlined!'))

  bold_and_underlined = bold + underline
  print(bold_and_underlined('This text is bold and underlined!'))
  ```
  """

  def __init__(self, start, end):
    self.data = f'{CSI}{start}m'
    self._end = f'{CSI}{end}m'

  def __add__(self, other):
    cls = type(self)
    if isinstance(other, cls):
      new = cls.__new__(cls)
      new.data = f'{self.data}{other.data}'
      new._end = f'{self._end}{other._end}'
      return new
    return self.data + other

  def __call__(self, s) -> str:
    return self.data + str(s) + self._end


# Typographic styles
reset = Style(0, 0)
"""Resets any previously applied styles."""
bold = Style(1, 22)
"""Boldens the text."""
dim = Style(2, 22)
"""Dims the text."""
italic = Style(3, 23)
"""Italicises the text."""
underline = Style(4, 24)
"""Underlines the text."""
blink = Style(5, 25)
"""Makes the text look like its flashing."""
invert = Style(7, 27)
"""Swaps the foreground and background colours."""
hide = Style(8, 28)
"""Makes the text invisible."""
strike = Style(9, 29)
"""Adds a strikethrough to the text."""

# Regular colours
default = Style(39, 39)
"""Sets the text colour to default."""
black = Style(30, 39)
"""Sets the text colour to black."""
red = Style(31, 39)
"""Sets the text colour to red."""
green = Style(32, 39)
"""Sets the text colour to green."""
yellow = Style(33, 39)
"""Sets the text colour to yellow."""
blue = Style(34, 39)
"""Sets the text colour to blue."""
purple = Style(35, 39)
"""Sets the text colour to purple."""
cyan = Style(36, 39)
"""Sets the text colour to cyan."""
white = Style(37, 39)
"""Sets the text colour to white."""

# Regular background colours
on_default = Style(49, 49)
"""Sets the background colour to default."""
on_black = Style(40, 49)
"""Sets the background colour to black."""
on_red = Style(41, 49)
"""Sets the background colour to red."""
on_green = Style(42, 49)
"""Sets the background colour to green."""
on_yellow = Style(43, 49)
"""Sets the background colour to yellow."""
on_blue = Style(44, 49)
"""Sets the background colour to blue."""
on_purple = Style(45, 49)
"""Sets the background colour to purple."""
on_cyan = Style(46, 49)
"""Sets the background colour to cyan."""
on_white = Style(47, 49)
"""Sets the background colour to white."""

# Bright colours
bright_black = Style(90, 39)
"""Sets the text colour to grey."""
bright_red = Style(91, 39)
"""Sets the text colour to bright red."""
bright_green = Style(92, 39)
"""Sets the text colour to bright green."""
bright_yellow = Style(93, 39)
"""Sets the text colour to bright yellow."""
bright_blue = Style(94, 39)
"""Sets the text colour to bright blue."""
bright_purple = Style(95, 39)
"""Sets the text colour to bright purple."""
bright_cyan = Style(96, 39)
"""Sets the text colour to bright cyan."""
bright_white = Style(97, 39)
"""Sets the text colour to a lighter shade of white."""

# Bright background colours
on_bright_black = Style(100, 49)
"""Sets the background colour to grey."""
on_bright_red = Style(101, 49)
"""Sets the background colour to bright red."""
on_bright_green = Style(102, 49)
"""Sets the background colour to bright green."""
on_bright_yellow = Style(103, 49)
"""Sets the background colour to bright yellow."""
on_bright_blue = Style(104, 49)
"""Sets the background colour to bright blue."""
on_bright_purple = Style(105, 49)
"""Sets the background colour to bright purple."""
on_bright_cyan = Style(106, 49)
"""Sets the background colour to bright cyan."""
on_bright_white = Style(107, 49)
"""Sets the background colour to a lighter shade of white."""


def rgb(r: int, g: int, b: int) -> Style:
  """Creates a colour `Style` for given rgb values."""
  return Style(f'38;2;{r};{g};{b}', 39)


def on_rgb(r: int, g: int, b: int) -> Style:
  """Creates a background colour `Style` for given rgb values."""
  return Style(f'48;2;{r};{g};{b}', 49)
