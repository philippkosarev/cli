#! /usr/bin/env python3

# Imports
import sys
import cli


# Creating the CLI
@cli.cli('very-smart-ai')
class main:
  """Trust me, it's the smartest one out there."""

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

  @cli.opt('mcbeth', 'Ponder whether to be or not to be.')
  @cli.opt('quiet', 'Be quiet.', 'q')
  def wonder(**opts):
    """Where's my copy of My Weekend in Stevenage by Filthy Henderson?"""
    if opts['mcbeth']:
      print("I just want to be a fish.")
    elif opts['quiet']:
      print('I REFUSE!')
    else:
      print('Thanks for staying quiet.')


# Running the CLI
if __name__ == '__main__':
  sys.exit(main())
