# -*- coding: utf-8 -*-

"""
clint.utils
~~~~~~~~~~~~

Various Python helpers used within clint.

"""

from __future__ import absolute_import

import sys
import errno
from os import makedirs


def is_collection(obj):
    """Tests if an object is a collection. Strings don't count."""

    if isinstance(obj, basestring):
        return False

    return hasattr(obj, '__getitem__')


def mkdir_p(path):
    """Emulates `mkdir -p` behavior."""
    try:
        makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise
