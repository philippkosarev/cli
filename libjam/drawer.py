"""Provides a few missing pieces for file management."""

# Imports
import os
import sys
import math
import shutil
import filetype
import subprocess


def _statdir(directory) -> tuple[list[tuple[os.DirEntry, bool, int]], int]:
  total_size = 0
  items = []
  for entry in os.scandir(directory):
    size = entry.stat().st_size
    total_size += size
    is_dir = entry.is_dir()
    info = entry, is_dir, size
    items.append(info)
    if is_dir:
      pair = _statdir(entry)
      items.extend(pair[0])
      total_size += pair[1]
  return items, total_size


def copy_with_progress(src, dst, progress_callback: callable):
  """Copies the given file while providing current progress."""
  buffer_size = shutil.COPY_BUFSIZE
  filesize = os.stat(src).st_size
  n_buffers = math.ceil(filesize / buffer_size)
  approximated_filesize = buffer_size * n_buffers
  with open(src, 'rb') as src_fp, open(dst, 'wb') as dst_fp:
    for i in range(n_buffers):
      progress_callback(i * buffer_size, approximated_filesize)
      dst_fp.write(src_fp.read(buffer_size))
    progress_callback(approximated_filesize, approximated_filesize)


def copy_tree_with_progress(src, dst, progress_callback: callable):
  """Copies the given directory while providing current progress."""
  queue, total_size = _statdir(src)
  bytes_copied = 0

  def subprogress_callback(done, todo):
    progress_callback(done + bytes_copied, total_size)

  os.mkdir(dst)
  for entry, is_dir, size in queue:
    progress_callback(bytes_copied, total_size)
    entry_dst = os.path.join(dst, os.path.relpath(entry, src))
    if is_dir:
      os.mkdir(entry_dst)
    else:
      copy_with_progress(entry, entry_dst, subprogress_callback)
    bytes_copied += size
  progress_callback(bytes_copied, total_size)


def unlink_tree_with_progress(directory, progress_callback: callable):
  """Deletes the given directory while providing current progress."""
  bytes_deleted = 0
  queue, total_size = _statdir(directory)
  queue.reverse()
  for entry, is_dir, size in queue:
    progress_callback(bytes_deleted, total_size)
    if is_dir:
      os.rmdir(entry)
    else:
      os.unlink(entry)
    bytes_deleted += size
  os.rmdir(directory)
  progress_callback(bytes_deleted, total_size)


def get_tree_size(directory) -> int:
  """Returns the size of the given directory in bytes."""
  total_size = 0
  for entry in os.scandir(directory):
    total_size += entry.stat().st_size
    if entry.is_dir():
      total_size += get_tree_size(entry)
  return total_size


def to_readable_size(
  size: int,
  ndigits: int or None = 1,
) -> tuple[float, str, str]:
  """Given a number of bytes, returns a human readable filesize, as a tuple.

  Tuple format: (value, short unit name, long unit name)
  Example output: (6.9, 'MB', 'MegaBytes')
  """
  orders = [
    ('B', 'Bytes'),
    ('KB', 'KiloBytes'),
    ('MB', 'MegaBytes'),
    ('GB', 'GigaBytes'),
    ('TB', 'TeraBytes'),
    ('PB', 'PetaBytes'),
    ('EB', 'ExaBytes'),
    ('ZB', 'ZettaBytes'),
    ('YB', 'YottaBytes'),
    ('RB', 'RonnaBytes'),
    ('QB', 'QuettaBytes'),
  ]
  n_orders = len(orders)
  if size > 0:
    order = math.floor(math.log(size, 1000))
    if order >= n_orders:
      order = n_orders - 1
    size = size / (1000**order)
    size = round(size, ndigits)
  else:
    order = 0
  units = orders[order]
  return (size,) + units


def start(*args) -> int:
  """Like xdg-open, but platform-aware."""
  commands = {
    'linux': 'xdg-open',
    'darwin': 'open',
    'win32': 'start',
    'cygwin': 'start',
  }
  command = commands.get(sys.platform)
  if not command:
    raise NotImplementedError(f"Unsupported platform '{sys.platform}'")
  process = subprocess.run([command, *args], check=True)
  return process.returncode

def _generic_pack(src, dst, cls, write_func_name: str):
  if not os.path.exists(src):
    FileNotFoundError('File not found', src)
  if not os.path.isdir(src):
    NotADirectoryError('Not a directory', src)
  with cls(dst, 'w') as file:
    write = getattr(file, write_func_name)
    if os.path.isdir(src):
      for root, dirs, files in os.walk(src):
        for name in files:
          path = os.path.join(root, name)
          name = os.path.relpath(path, src)
          write(path, name)
    else:
      name = os.path.basename(src)
      write(src, name)


def _generic_pack_with_progress(
  src,
  dst,
  progress_callback: callable,
  cls,
  write_func_name: str,
):
  if not os.path.exists(src):
    FileNotFoundError('File not found', src)
  if not os.path.isdir(src):
    NotADirectoryError('Not a directory', src)
  files = []
  for root, dirnames, filenames in os.walk(src):
    for name in filenames:
      path = os.path.join(root, name)
      files.append(path)
  n_files = len(files)
  packed = 0
  with cls(dst, 'w') as file:
    write = getattr(file, write_func_name)
    for path in files:
      progress_callback(packed, n_files)
      name = os.path.relpath(path, src)
      write(path, name)
      packed += 1
    progress_callback(packed, n_files)


def _generic_unpack(src, dst, cls):
  with cls(src) as obj:
    obj.extractall(dst)


def _generic_unpack_with_progress(
  src,
  dst,
  progress_callback: callable,
  cls,
  namelist_function_name: str,
):
  with cls(src) as obj:
    namelist = getattr(obj, namelist_function_name)
    names = namelist()
    n_names = len(names)
    unpacked = 0
    for name in names:
      progress_callback(unpacked, n_names)
      obj.extract(name, dst)
      unpacked += 1
    progress_callback(unpacked, n_names)


def pack_zip(src, dst):
  """Packs the given directory to a zip file."""
  from zipfile import ZipFile
  _generic_pack(src, dst, ZipFile, 'write')


def pack_zip_with_progress(src, dst, progress_callback: callable):
  """Packs the given directory to a zip file while providing the
  current progress.
  """
  from zipfile import ZipFile
  _generic_pack_with_progress(
    src, dst,
    progress_callback,
    ZipFile, 'write'
  )


def unpack_zip(src, dst):
  """Unpacks the given zip archive to the specified directory."""
  from zipfile import ZipFile
  _generic_unpack(src, dst, ZipFile)


def unpack_zip_with_progress(src, dst, progress_callback: callable):
  """Unpacks the given zip archive to the specified directory while
  providing current progress.
  """
  from zipfile import ZipFile
  _generic_unpack_with_progress(
    src,
    dst,
    progress_callback,
    ZipFile,
    'namelist',
  )


def pack_7z(src, dst):
  """Packs the given directory to a 7zip file."""
  from py7zr import SevenZipFile
  _generic_pack(src, dst, SevenZipFile, 'write')


def pack_7z_with_progress(src, dst, progress_callback: callable):
  from py7zr import SevenZipFile
  _generic_pack_with_progress(
    src, dst,
    progress_callback,
    SevenZipFile, 'write'
  )


def unpack_7z(src, dst):
  """Unpacks the given 7zip archive to the specified directory."""
  from py7zr import SevenZipFile
  _generic_unpack(src, dst, SevenZipFile)


def unpack_7z_with_progress(src, dst, progress_callback: callable):
  """Unpacks the given tar archive to the specified directory while
  providing current progress.
  """
  from py7zr import SevenZipFile, callbacks
  class Callback(callbacks.ExtractCallback):
    def __init__(self, todo: int):
      self.todo = todo
      self.done = 0

    def report_start_preparation(self):
      progress_callback(self.done, self.todo)

    def report_start(self, file, size):
      progress_callback(self.done, self.todo)
      self.done += 1

    def report_end(self, file, size):
      progress_callback(self.done, self.todo)

    def report_postprocess(self):
      pass

    def report_update(self, size):
      pass

    def report_warning(self, message):
      pass

  with SevenZipFile(src) as obj:
    to_unpack = len(obj.namelist())
    callback = Callback(to_unpack)
    obj.extractall(dst, callback=callback)


def unpack_rar(src, dst):
  """Unpacks the given rar archive to the specified directory."""
  from rarfile import RarFile
  _generic_unpack(src, dst, RarFile)


def unpack_rar_with_progress(src, dst, progress_callback: callable):
  """Unpacks the given tar archive to the specified directory while
  providing current progress.
  """
  from rarfile import RarFile
  _generic_unpack_with_progress(
    src,
    dst,
    progress_callback,
    RarFile,
    'namelist',
  )


_unpack_functions = {
  'zip': unpack_zip,
  '7z': unpack_7z,
  'rar': unpack_rar,
}

_unpack_with_progress_functions = {
  'zip': unpack_zip_with_progress,
  '7z': unpack_7z_with_progress,
  'rar': unpack_rar_with_progress,
}


def can_unpack(archive) -> bool:
  """Checks if the given archive can be unpacked."""
  ext = filetype.guess_extension(archive)
  function = _unpack_functions.get(ext)
  return function is not None


def unpack(src, dst):
  """Unpacks the given archive to the specified directory.

  If the archive type is not supported `NotImplementedError` is raised.
  """
  ext = filetype.guess_extension(src)
  if not ext:
    raise NotImplementedError(
      f"Unable to determine file extension of {src}"
    )
  function = _unpack_functions.get(ext)
  if not function:
    raise NotImplementedError(
      f"Unsupported archive type '{ext}'"
    )
  function(src, dst)


def unpack_with_progress(src, dst, progress_callback: callable):
  """Unpacks the given archive to the specified directory while providing
  current progress.

  If the archive type is not supported `NotImplementedError` is raised.
  """
  ext = filetype.guess_extension(src)
  if not ext:
    raise ValueError(
      f"Unable to determine file extension of {src}"
    )
  function = _unpack_with_progress_functions.get(ext)
  if not function:
    raise NotImplementedError(f"Unsupported filetype {ext}")
  function(src, dst, progress_callback)
