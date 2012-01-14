#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from clint import args
from clint.textui import colored, puts, indent

if __name__ == '__main__':

    puts('Test:')
    with indent(4):
        puts('%s Fake test 1.' % colored.green('✔'))
        puts('%s Fake test 2.' % colored.red('✖'))

    puts('')
    puts('Greet:')
    with indent(4):
        puts(colored.red('Здравствуйте'))
        puts(colored.green('你好。'))
        puts(colored.yellow('سلام'))
        puts(colored.magenta('안녕하세요'))
        puts(colored.blue('नमस्ते'))
        puts(colored.cyan('γειά σου'))

    puts('')
    puts('Arguments:')
    with indent(4):
        for arg in args.all:
            puts('%s' % colored.red(arg))
