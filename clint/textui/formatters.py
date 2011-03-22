# -*- coding: utf-8 -*-

"""
clint.textui.formatters
~~~~~~~~~~~~~~~~~~~~~~~

Core TextUI functionality for text formatting.

"""

from __future__ import absolute_import

from ..utils import tsplit, schunk


NEWLINES = ('\n', '\r', '\r\n')




def min_width(string, cols, padding=' '):
    """Returns given string with right padding."""

    stack = tsplit(string, NEWLINES)

    for i, substring in enumerate(stack):
        stack[i] = substring.ljust(cols, padding)
        
    return '\n'.join(stack)


def max_width(string, cols, separator='\n'):
    """Returns a freshly formatted """
    
    stack = tsplit(string, NEWLINES)

    for i, substring in enumerate(stack):
        stack[i] = substring.split()

    _stack = []
    
    for row in stack:
        _row = ['',]
        _row_i = 0

        for word in row:
            if (len(_row[_row_i]) + len(word)) < cols:
                _row[_row_i] += word
                _row[_row_i] += ' '
                
            elif len(word) > cols:

                # ensure empty row
                if len(_row[_row_i]):
                    _row.append('')
                    _row_i += 1

                chunks = schunk(word, cols)
                for i, chunk in enumerate(chunks):
                    if not (i + 1) == len(chunks):
                        _row[_row_i] += chunk
                        _row.append('')
                        _row_i += 1
                    else:
                        _row[_row_i] += chunk
                        _row[_row_i] += ' '
            else:
                _row.append('')
                _row_i += 1
                _row[_row_i] += word
                _row[_row_i] += ' '
        _stack.append(separator.join(_row))


    return '\n'.join(_stack)
