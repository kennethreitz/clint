# -*- coding: utf-8 -*-

"""
clint.utils
~~~~~~~~~~~~

Various Python helpers used within clint.

"""

from __future__ import absolute_import
from __future__ import with_statement

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
    except OSError, exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise

def tsplit(string, delimiters):
    """Behaves str.split but supports tuples of delimiters."""
    
    delimiters = tuple(delimiters)
    stack = [string,]
    
    for delimiter in delimiters:
        for i, substring in enumerate(stack):
            substack = substring.split(delimiter)
            stack.pop(i)
            for j, _substring in enumerate(substack):
                stack.insert(i+j, _substring)
            
    return stack

def schunk(string, size):
    """Splits string into n sized chunks."""

    stack = []

    substack = []
    current_count = 0

    for char in string:
        if not current_count < size:
            stack.append(''.join(substack))
            substack = []
            current_count = 0

        substack.append(char)
        current_count += 1

    if len(substack):
        stack.append(''.join(substack))

    return stack
