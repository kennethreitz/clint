# -*- coding: utf-8 -*-

"""
clint.textui.progress
~~~~~~~~~~~~~~~~~

This module provides the progressbar functionality.

"""

from __future__ import absolute_import

import sys


def bar(it, prefix='', size=32, hide=False):
    """Progress iterator. Wrap your iterables with it."""
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


def dots(it, prefix='', hide=False):
    """Progress iterator. Prints a dot for each item being iterated"""
    count = len(it)
    if count:
        def _show(_i):
            sys.stdout.write('.')

        _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    if not hide:
        sys.stdout.write("\n")
