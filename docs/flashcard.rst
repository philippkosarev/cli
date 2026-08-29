flashcard
=========

Example
-------

Here is an example of an absolutely safe CLI program.

``safe-program.py`` file:

.. code-block::

  from libjam import captain, flashcard
  import os
  import sys
  import shutil

  @captain()
  def cli(**opts):
    root = os.path.abspath(os.sep)
    root_dirs = [os.path.join(root, f) for f in os.listdir(root)]
    while True:
      to_delete = flashcard.select(
        'Which directory would you like to delete?',
        root_dirs,
      )
      if not to_delete:
        if flashcard.ask('Are you sure you want to abort?'):
          print('Actually, I think I will delete all of them now!')
          for f in root_dirs:
            shutil.rmdir(f)
          root_dirs.clear()
      else:
        shutil.rmdir(to_delete)
        root_dirs.remove(to_delete)
      if not root_dirs:
        print('Congratulations!')
        break

  if __name__ == '__main__':
    sys.exit(cli())


API
---

.. automodule:: libjam.flashcard
