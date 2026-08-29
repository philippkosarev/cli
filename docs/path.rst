Path
====

Example
-------

Here is an example CLI for extracting archives:

.. code-block::

  from libjam import captain, writer, Path
  import sys

  @captain()
  def cli(archive, out_directory, **opts):
    archive, out_directory = Path(archive), Path(out_directory)
    # Validating input
    if not archive.exists():
      cli.usage_error(f'{archive}: no such file or directory.')
    if not archive.is_file():
      cli.usage_error(f'{archive}: not a file.')
    if not archive.can_unpack():
      cli.usage_error(f'{archive}: unsupported filetype.')
    # Extracting
    with writer.ProgressBar(f"Extracting '{archive.name}'") as bar:
      archive.unpack_with_progress(out_directory, bar.update)

  if __name__ == '__main__':
    sys.exit(cli())


API
---

.. autoclass:: libjam.Path
