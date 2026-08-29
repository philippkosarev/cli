#! /usr/bin/env python3

# Imports
from libjam import captain
import sys


# Creating the CLI
@captain('very-smart-ai')
class cli:
  "Trust me, it's the smartest one out there."

  def shout(text, suffix=None):
    """I will be loud!"""
    text += '!'
    if suffix:
      text += suffix
    print(text)

  def whisper(*lines):
    """Shhhh! You don't want them to hear you..."""
    lines = [l + '...' for l in lines]
    text = '\n'.join(lines)
    print(text)

  def wonder(**opts):
    """Where's my copy of My Weekend in Stevenage by Filthy Henderson?"""
    if opts['mcbeth']:
      print("I just want to be a fish.")
    elif opts['quiet']:
      print('I REFUSE!')
    else:
      print('Thanks for staying quiet.')


# Adding options to the wonder command
cli.wonder_command.add_option(
  'mcbeth', 'Ponder whether to be or not to be.',
)
cli.wonder_command.add_option('quiet', 'Be quiet.', 'q')

# Running the CLI
if __name__ == '__main__':
  sys.exit(cli())
