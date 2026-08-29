# Imports
import shutil
import pathlib

# Internal imports
from . import drawer


class Path(pathlib.Path):
  """An extension of `pathlib.Path` with `drawer`'s functionality.

  There are a few deviations from `drawer`'s functions:

  First, following the `pathlib.Path`'s existing `copy` method, which
  works on both files and directories, this extension has only one
  `copy_with_progress` method that also works for both files and
  directories.

  Second, the `unlink_tree` method, which links to `shutil.rmtree`, was
  added for convenience.
  """

  def copy_with_progress(self, target, progress_callback: callable):
    """Recursively copy this file or directory tree to the given
    destination while providing current progress.
    """
    if self.is_dir():
      function = drawer.copy_tree_with_progress
    else:
      function = drawer.copy_with_progress
    function(self, target, progress_callback)

  get_tree_size = drawer.get_tree_size
  to_readable_size = staticmethod(drawer.to_readable_size)

  unlink_tree = shutil.rmtree
  unlink_tree_with_progress = drawer.unlink_tree_with_progress

  start = drawer.start

  pack_zip = drawer.pack_zip
  pack_zip_with_progress = drawer.pack_zip_with_progress
  unpack_zip = drawer.unpack_zip
  unpack_zip_with_progress = drawer.unpack_zip_with_progress

  pack_7z = drawer.pack_7z
  pack_7z_with_progress = drawer.pack_7z_with_progress
  unpack_7z = drawer.unpack_7z
  unpack_7z_with_progress = drawer.unpack_7z_with_progress

  unpack_rar = drawer.unpack_rar
  unpack_rar_with_progress = drawer.unpack_rar_with_progress

  can_unpack = drawer.can_unpack
  unpack = drawer.unpack
  unpack_with_progress = drawer.unpack_with_progress
