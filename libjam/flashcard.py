"""Used for getting user input inside the terminal."""

# Importing readline if available for a better input() experience
try:
  import readline as readline
except ModuleNotFoundError:
  pass

# Internal imports
from . import writer


def ask(prompt: str, prompt_style: callable = None) -> bool:
  """Asks the user a yes/no question."""
  prompt = f'{prompt} [y/n]: '
  if prompt_style:
    prompt = prompt_style(prompt)
  while True:
    user_input = input(prompt).strip().lower()
    if user_input in ('y', 'yes'):
      return True
    elif user_input in ('n', 'no'):
      return False


def select(
  prompt: str,
  items: list[str],
  prompt_style: callable = writer.bold,
) -> str|None:
  """Asks the user to select one item from a list.

  Returns `None` if the user decides to abort.

  The `prompt_style` is called to finalise the prompt. By default it's
  set to `writer.bold`, but can either be set to `None`, or any other
  callable object (e.g. a function).
  """
  # Creating the prompt
  n_items = len(items)
  prompt = f'{prompt} (1-{n_items}, 0 to abort): '
  if prompt_style:
    prompt = prompt_style(prompt)
  # Printing available items
  text = [f'{i}) {item}' for i, item in enumerate(items, start=1)]
  text = writer.to_columns(text)
  print(text + '\n')
  # Getting user input
  while True:
    choice = input(prompt).strip()
    if choice == '0':
      return None
    elif choice in [str(n) for n in range(1, n_items + 1)]:
      return items[int(choice) - 1]
    elif choice in items:
      return choice
