#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from clint.textui import colored
from clint.packages.colorama.conv import html
from clint.packages.colorama import caps
from clint.textui import columns

# Force capability to XTERM256 for now, otherwise it's boring
# I'm not sure a reliable detection mechanism even exists...
caps.capability = caps.ColorCapability.XTERM256

def colorizer(colors):
    for color in colors:
        yield colored.rgb(color, color)

if __name__ == '__main__':
    i = iter(colorizer(html.colors))
    while True:
        try:
            a = i.next()
        except StopIteration:
            break
        try:
            b = i.next()
        except StopIteration:
            b = ""
        try:
            c = i.next()
        except StopIteration:
            c = ""
        print columns([a,30],[b,30],[c,30])

        

