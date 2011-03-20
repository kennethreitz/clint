#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from time import sleep
from random import random
from clint.textui import progressbar


if __name__ == '__main__':
    for i in progressbar(range(100)):
        sleep(random() * 0.2)

    
    