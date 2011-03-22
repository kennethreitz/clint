#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from clint.textui import puts, max_width, min_width

lorem = 'Lorem ipsum dolor sit amet, consehdfhdfhdfhdfhdfhctetur adi pisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'

if __name__ == '__main__':
    # puts(min_width('test\nit', 20) + ' me')
    # puts(min_width(lorem, 20) + ' me')
    
    print max_width(lorem, 20)