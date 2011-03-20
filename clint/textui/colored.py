# -*- coding: utf-8 -*-

"""
clint.colored
~~~~~~~~~~~~~

This module provides a simple and elegant wrapper for colorama.

"""


from __future__ import absolute_import

from ..packages import colorama



colorama.init(autoreset=True)


__all__ = (
    'red', 'green', 'yellow', 'blue',
    'black', 'magenta', 'cyan', 'white'
)


class ColoredString(object):
    """Enhanced string for __len__ operations on Colored output."""
    def __init__(self, color, s):
        super(ColoredString, self).__init__()
        self.s = s
        self.color = color
        self.color_str = '%s%s%s' % (
            getattr(colorama.Fore, self.color), self.s, colorama.Fore.RESET)
        
    def __len__(self):
        return len(self.s)
        
    def __repr__(self):
        return "<%s-string: '%s'>" % (self.color, self.s)
        
    def __str__(self):
        return self.__unicode__().encode('utf8')
        
    def __unicode__(self):
        return self.color_str
        
    def __add__(self, other):
        return str(self.color_str) + str(other)
        
    def __radd__(self, other):
        return str(other) + str(self.color_str)
        
    def __mul__(self, other):
        return (self.color_str * other)



def black(string):
    return ColoredString('BLACK', string)

def red(string):
    return ColoredString('RED', string)

def green(string):
    return ColoredString('GREEN', string)

def yellow(string):
    return ColoredString('YELLOW', string)

def blue(string):
    return ColoredString('BLUE', string)

def magenta(string):
    return ColoredString('MAGENTA', string)

def cyan(string):
    return ColoredString('CYAN', string)

def white(string):
    return ColoredString('WHITE', string)
