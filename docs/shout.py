#! /usr/bin/env python3

import cli

# Creating the CLI
@cli.cli
@cli.opt('world', 'Adds " world" before the exclamation mark.', 'w')
def shout(text: str, **opts):
  """Shouts the given text back."""
  if opts['world']:
    text += ' world'
  print(text + '!')
  return 'anything'

# Running the CLI
returned = shout()

# This assertion will succeed
assert returned == 'anything'
