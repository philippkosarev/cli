drawer
======

Example
-------

Here is an example CLI for extracting archives:

.. code-block::

  from libjam import captain, writer, drawer
  import os
  import sys

  @captain()
  def cli(archive, out_directory, **opts):
    # Validating input
    if not os.path.exists(archive):
      cli.usage_error(f'{archive}: no such file or directory.')
    if not os.path.isfile(archive):
      cli.usage_error(f'{archive}: not a file.')
    if not drawer.can_unpack(archive):
      cli.usage_error(f'{archive}: unsupported filetype.')
    # Extracting
    name = os.path.basename(archive)
    with writer.ProgressBar(f"Extracting '{name}'") as bar:
      drawer.unpack_with_progress(archive, out_directory, bar.update)

  if __name__ == '__main__':
    sys.exit(cli())


API
---

.. automodule:: libjam.drawer
