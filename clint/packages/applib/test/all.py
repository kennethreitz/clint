# Copyright (c) 2010 ActiveState Software Inc. All rights reserved.

from __future__ import unicode_literals
import os
from os import path
import tempfile
import sys

import pytest

from applib import sh
from applib import textui
from applib.misc import safe_unicode
import six


fixtures = path.join(path.dirname(__file__), 'fixtures')

def test_import():
    import applib
    import applib.base
    import applib.sh
    import applib.textui
    import applib.log
    import applib.misc


def test_sh_runerror_unicode():
    # https://github.com/activestate/applib/issues/12
    with pytest.raises(sh.RunError):
        try:
            sh.run('echo ' + "\u1234" + " & nonexistant")
        except sh.RunError as e:
            print(safe_unicode(e))
            raise


def test_sh_runerror_limit():
    with pytest.raises(sh.RunError):
        from random import choice
        import string
        LINE = ''.join([choice(string.ascii_letters) for x in range(80)])
        try:
            sh.run(r'''python -c "print('\n'.join(['%s']*100)); raise SystemExit('an error');"''' % LINE)
        except sh.RunError as e:
            c = str(e).count(LINE)
            # def _limit_str(s, maxchars=80*15): --- so ~ 15 lines (not 100 lines)
            assert c < 20, "original message: %s" % e  
            assert '[...]' in str(e)
            raise


def test_safe_unicode():
    from applib.misc import safe_unicode
    import six

    abc_bytes = b'ab\nc'
    abc_text = 'ab\nc'

    assert safe_unicode(abc_bytes) == abc_text
    assert safe_unicode(abc_text) == abc_text

    foo_text = 'abc'  # note: \x89 is ignored.
    foo_bytes = b'\x89abc'

    assert safe_unicode(foo_text) == foo_text
    assert safe_unicode(foo_bytes) == foo_text


def test_sh_rm_file():
    with sh.tmpdir():
        with open('afile', 'w') as f: f.close()
        assert path.exists('afile')
        sh.rm('afile')
        assert not path.exists('afile')


def test_sh_rm_dir():
    with sh.tmpdir():
        sh.mkdirs('adir')
        with sh.cd('adir'):
            with open('afile', 'w') as f: f.close()
            assert path.exists('afile')
        assert path.exists('adir')
        sh.rm('adir')
        assert not path.exists('adir')
 

# Workaround a py.test bug:
# Error evaluating 'skipif' expression
#     b'sys.platform == "win32"'
# Failed: expression is not a string
def skipif(expr):
    if not six.PY3:
        expr = expr.encode()
    return pytest.mark.skipif(expr)

        
@skipif('sys.platform == "win32"')
def test_sh_rm_symlink():
    with sh.tmpdir():
        with open('afile', 'w') as f: f.close()
        assert path.exists('afile')
        os.symlink('afile', 'alink')
        assert path.lexists('alink')
        sh.rm('alink')
        assert not path.lexists('alink')
        
        
@skipif('sys.platform == "win32"')
def test_sh_rm_broken_symlink():
    with sh.tmpdir():
        os.symlink('afile-notexist', 'alink')
        assert not path.exists('alink')
        assert path.lexists('alink')
        sh.rm('alink')
        assert not path.lexists('alink')
        

@skipif('sys.platform == "win32"')
def test_sh_rm_symlink_dir():
    with sh.tmpdir():
        sh.mkdirs('adir')
        with sh.cd('adir'):
            with open('afile', 'w') as f: f.close()
            assert path.exists('afile')
        assert path.exists('adir')
        os.symlink('adir', 'alink')
        assert path.lexists('alink')
        sh.rm('alink')
        assert path.exists('adir')
        assert not path.lexists('alink')
        
        
def test_console_width_detection():
    width = textui.find_console_width()
    assert width is None
    

def test_colprint():
    sample_table = [
        ['python-daemon', '4.5.7.7.3-1', 'blah foo meh yuck'],
        ['foo',           '6.1', ('some very loooooooooong string here .. I '
                                  'suggest we make it even longer .. so longer '
                                  ' that normal terminal widths should entail '
                                  'colprint to trim the string')]]
    textui.colprint(sample_table)

    # try with empty inputs
    textui.colprint(None)
    textui.colprint([])

        
def test_compression_ensure_read_access():
    """Test the ensure_read_access() hack in _compression.py"""
    def test_pkg(pkgpath):
        testdir = tempfile.mkdtemp('-test', 'pypm-')
        extracted_dir, _ = sh.unpack_archive(pkgpath, testdir)
        # check if we have read access on the directory
        for child in os.listdir(extracted_dir):
            p = path.join(extracted_dir, child)
            if path.isdir(p):
                os.listdir(p)
        sh.rm(testdir)

    yield 'u-x on dirs', test_pkg, path.join(fixtures, 'generator_tools-0.3.5.tar.gz')
    yield 'u-w on ._setup.py', test_pkg, path.join(fixtures, 'TracProjectMenu-1.0.tar.gz')
    

def test_compression_catch_invalid_mode():
    """Error <IOError: [Errno 22] invalid mode ('wb') or filename> from
    tarfile.py should be handled"""
    def extract():
        testdir = tempfile.mkdtemp('-test', 'pypm-')
        extracted_dir, _ = sh.unpack_archive(
            path.join(fixtures, 'libtele-0.2.tar.gz'), testdir)
    if sys.platform == 'win32' and sys.version_info[:2] >= (2, 7):
        with pytest.raises(sh.PackError):
            extract()
    else:
        extract()
    
    
@pytest.mark.xfail
def test_compression_issue_11():
    """https://github.com/ActiveState/applib/issues/#issue/11
    
    * Windows: IOError: [Errno 13] Permission denied: '.\\airi-0.0.1\\AIRi'
    * OSX: IOError: [Errno 21] Is a directory: './airi-0.0.1/AIRi
    * OSX Archive Utility (Finder): Unable to unarchive "airi-0.0.1.tar" ...
         (Error 1 - Operation not permitted.)
    """
    testdir = tempfile.mkdtemp('applib')
    d, _ = sh.unpack_archive(path.join(fixtures, 'airi-0.0.1.tar.gz'), testdir)
    
