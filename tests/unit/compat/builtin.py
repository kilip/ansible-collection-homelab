# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

#
# Compat for python2.7
#

# One unittest needs to import builtins via __import__() so we need to have
# the string that represents it
try:
    import __builtin__
except ImportError:
    BUILTINS = 'builtins'
else:
    BUILTINS = '__builtin__'
