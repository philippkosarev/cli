Secretary
=========

Example
-------

Here is an example of how a CLI download manager might use Secretary for its configuration.

``cli_config.py`` file:

.. code-block::

  # Imports
  from pathlib import Path
  from libjam import Secretary

  # Defining defaults
  default_downloads_dir = Path.home() / 'Downloads'
  if not default_downloads_dir.is_dir():
    default_downloads_dir = None
  defaults = {
    'downloads-directory': default_downloads_dir,
  }

  # Config template
  template = '''\
  # An override for the default downloads directory
  # downloads-directory = ''
  '''

  # Initialising config
  secretary = Secretary('download-manager')
  config = secretary.file('config', defaults, template)

  # Validating values
  downloads_dir = config.get('downloads-directory')
  if not downloads_dir:
    config.error(
      'Could not automatically find an existing Downloads directory.',
      "Please specify the 'downloads-directory' manually.",
    )
  downloads_dir = Path(downloads_dir)
  if not downloads_dir.is_dir():
    config.error("The specified 'downloads-directory' does not exist.")


``main_cli.py`` file:

.. code-block::

  from .cli_config import downloads_dir
  from .download_manager import DownloadManager

  download_manager = DownloadManager(downloads_dir)

  # The rest of the program...


Example error:

.. code-block::

  $ python -m download_manager.cli
  Configuration error in ~/.config/download-manager/config.toml:
  Could not automatically find an existing Downloads directory.
  Please specify the 'downloads-directory' manually.


API
---

.. autoclass:: libjam.Secretary

.. autoclass:: libjam.File
  :show-inheritance:
