Clint: Python Command-line Application Tools
============================================

**Clint** is a module filled with a set of awesome tools for developing
commandline applications.

.. image:: https://github.com/kennethreitz/clint/raw/master/misc/clint.jpeg

**C** ommand
**L** ine
**IN** terface
**T** ools
. 

Features:
---------

- CLI Colors and Indents
- Iterator-based Progress Bar
- Implicit Argument Handling
- Simple Support for Unix Pipes
- Application Directory management


Example
-------

I want to indent my console text. ::

    >>> from clint.textui import puts, indent

    >>> puts('not indented text')
    >>> with indent(4):
    >>>     puts('indented text')
    not indented text
        indented text

I want to quote my console text (like email). ::

    >>> puts('not indented text')
    >>> with indent(4, quote=' >'):
    >>>     puts('quoted text')
    >>>     puts('pretty cool, eh?')
    
    not indented text
     >  indented text
     >  pretty cool, eh?

I want to color my console text. ::

    >>> from clint.textui import colored

    >>> puts(colored.red('red text'))
    red text

    # It's red in Windows, OSX, and Linux alike.

I want to get data piped to stdin. ::

    >>> clint.piped_in()
    
    # if no data was piped in, piped_in returns None


I want to get the first commandline argument passed in. ::

    >>> clint.args.get(0)

    # if no argument was passed, get returns None


I want to store a configuration file. ::

    >>> from clint import resources

    >>> resources.init('Company', 'AppName')
    >>> resources.user.write('config.ini', file_contents)

    # OSX: '/Users/appuser/Library/Application Support/AppName/config.ini'
    # Windows: 'C:\\Users\\appuser\\AppData\\Local\\Company\\AppName\\config.ini'
    # Linux: '/home/appuser/.config/appname/config.ini'


Installation
------------

To install clint, simply: ::

    $ pip install clint

Or, if you absolutely must: ::

    $ easy_install clint

But, you really shouldn't do that.



License:
--------

ISC License. ::

    Copyright (c) 2011, Kenneth Reitz <me@kennethreitz.com>

    Permission to use, copy, modify, and/or distribute this software for any
    purpose with or without fee is hereby granted, provided that the above
    copyright notice and this permission notice appear in all copies.

    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


Contribute
----------

If you'd like to contribute, simply fork `the repository`_, commit your changes
to the **develop** branch (or branch off of it), and send a pull request. Make
sure you add yourself to AUTHORS_.


Roadmap
-------
- Unittests
- Sphinx Documentation
- Python 2.5, 3.1, 3.2 Support



.. _`the repository`: http://github.com/kennethreitz/clint
.. _AUTHORS: http://github.com/kennethreitz/clint/blob/master/AUTHORS
