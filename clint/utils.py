# -*- coding: utf-8 -*-

import sys
import errno
from os import makedirs



def progressbar(it, prefix='', size=32, hide=False):
    count = len(it)
    if count:
        def _show(_i):
            x = int(size*_i/count)
            if not hide:
                sys.stdout.write("%s[%s>%s] %i/%i\r" % (prefix, "="*x, "-"*(size-x), _i, count))
                sys.stdout.flush()

        _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    if not hide:
        sys.stdout.write("\n")
        sys.stdout.flush()


def is_collection(obj):
    """Tests if an object is a collection"""

    if isinstance(obj, basestring):
        return False

    return hasattr(obj, '__getitem__')


def fixedwidth(string, width=15):
    """Adds column to output steam."""
    if len(string) > width:
        return string[:width]
    else:
        return string.ljust(width)


def mkdir_p(path):
    """mkdir -p"""
    try:
        makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise
