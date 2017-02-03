#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from clint.arguments import Args
from clint.textui import puts, colored

all_args = Args().grouped

for item in all_args:
    if item is not '_':
        puts(colored.red("key:%s" % item))
        print(all_args[item].all)

