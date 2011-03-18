# Copyright (c) 2010 ActiveState Software Inc. All rights reserved.

"""Various shell related wrappers
"""

import os
from os import path
import shutil
import tempfile
from fnmatch import fnmatch
from contextlib import contextmanager

from applib._proc import *


#
# Compression routines
#

class PackError(Exception):
    """Error during pack or unpack"""
    

def unpack_archive(filename, pth='.'):
    """Unpack the archive under ``path``
    
    Return (unpacked directory path, filetype)
    """
    from applib import _compression
    
    assert path.isfile(filename), 'not a file: %s' % filename
    assert path.isdir(pth)
    
    for filetype, implementor in _compression.implementors.items():
        if implementor.is_valid(filename):
            with cd(pth):
                return (implementor(filename).extract(), filetype)
    else:
        raise PackError('unknown compression format: ' + filename)


def pack_archive(filename, files, pwd, filetype="tgz"):
    """Pack the given `files` from directory `pwd`
    
    `filetype` must be one of ["tgz", "tbz2", "zip"]
    """
    from applib import _compression
    
    assert path.isdir(pwd)
    assert filetype in _compression.implementors, 'invalid filetype: %s' % filetype
    
    if path.exists(filename):
        rm(filename)
    
    with cd(pwd):
        relnames = [path.relpath(file, pwd) for file in files]
        _compression.implementors[filetype].pack(relnames, filename)
        
    return filename
        

#
# Path/file routines
#

def mkdirs(pth):
    """Make all directories along ``pth``"""
    if not path.exists(pth):
        os.makedirs(pth)
    else:
        assert path.isdir(pth)
    
    
def rm(p):
    """Remove the specified path recursively. Similar to `rm -rf ARG`
    
    Note: if ARG is a symlink, only that symlink will be removed.
    """
    if path.lexists(p):
        if path.isdir(p) and not path.islink(p):
            shutil.rmtree(p)
        else:
            os.remove(p)

    
def mv(src, dest, _mkdirs=False):
    """Move `src` to `dest`"""
    if _mkdirs:
        mkdirs(path.dirname(dest))
    shutil.move(src, dest)
    

def cp(src, dest, _mkdirs=False, ignore=None, copyperms=True):
    """Copy `src` to `dest` recursively"""
    assert path.exists(src)
    
    if _mkdirs:
        mkdirs(path.dirname(dest))
    
    if path.isdir(src):
        _copytree(src, dest, ignore=ignore, copyperms=copyperms)
    else:
        shutil.copyfile(src, dest)


def find(pth, pattern):
    """Find files or directories matching ``pattern`` under ``pth``"""
    matches = []
    if path.isfile(pth):
        if fnmatch(path.basename(pth), pattern):
            matches.append(pth)
    else:
        for root, dirs, files in os.walk(pth):
            matches.extend([
                path.join(root, f) for f in files+dirs
                if fnmatch(f, pattern)
            ])
    return matches
    
    
@contextmanager
def cd(pth):
    """With context to temporarily change directory"""
    assert path.isdir(existing(pth)), pth
    
    cwd = os.getcwd()
    os.chdir(pth)
    try:
        yield
    finally:
        os.chdir(cwd)


@contextmanager
def tmpdir(prefix='tmp-', suffix=''):
    """__with__ context to work in a temporary working directory
    
    Temporary directory will be deleted unless an exception was raised. During
    the context, CWD will be changed to the temporary directory.
    """
    d = tempfile.mkdtemp(prefix=prefix, suffix=suffix)
    with cd(d):
        yield d
    rm(d)


def existing(pth):
    """Return `pth` after checking it exists"""
    if not path.exists(pth):
        raise IOError('"{0}" does not exist'.format(pth))
    return pth
    
    
def _copytree(src, dst, symlinks=False, ignore=None, copyperms=True):
    """Forked shutil.copytree for `copyperms` support"""
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                _copytree(srcname, dstname, symlinks, ignore, copyperms)
            else:
                shutil.copy(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error) as why:
            raise
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except shutil.Error:
            _, err = sys.exec_info()
            errors.extend(err.args[0])
    if copyperms:
        try:
            shutil.copystat(src, dst)
        except WindowsError:
            # can't copy file access times on Windows
            pass
        except OSError:
            _, why = sys.exec_info()
            errors.extend((src, dst, str(why)))
    if errors:
        raise shutil.Error(errors)
    

# WindowsError is not available on other platforms
try:
    WindowsError
except NameError:
    class WindowsError(OSError): pass
