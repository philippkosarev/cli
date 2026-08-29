#! /usr/bin/env python3

from libjam import captain

# Creating the CLI
@captain()
def shout(text: str, *, world=False):
  """Shouts the given text back."""
  if world:
    text += ' world'
  print(text + '!')
  return 'anything'

# Adding an option to the CLI
shout.add_option(
  'world', "Adds ' world' before the exclamation mark.", 'w',
)

# Running the CLI
returned = shout()

# This assertion will succeed
assert returned == 'anything'
