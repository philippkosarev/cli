# Imports
import sys

# Internal imports
from . import _lib


# Creating our callable module
class Module(sys.modules[__name__].__class__):
  CLI = _lib.CLI
  __call__ = staticmethod(_lib.cli)
  Option = _lib.Option
  Partial = _lib.Partial
  part = staticmethod(_lib.part)


# Replacing the real module with our callable module
sys.modules[__name__] = Module(__name__)
