#! /usr/bin/env python3

import cli

# Creating the CLI
@cli(options=[
  ('world', 'Appends " world" before the exclamation mark.', 'w'),
])
def shout(text: str, *, world: bool = False):
  """Shouts the given text back."""
  if world:
    text += ' world'
  print(text + '!')
  return 'anything'

# Running the CLI
returned = shout()

# This assertion will succeed
assert returned == 'anything'
