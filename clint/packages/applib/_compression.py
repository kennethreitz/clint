# Copyright (c) 2010 ActiveState Software Inc. All rights reserved.

import sys
import os
from os import path
import tarfile
import zipfile
from contextlib import closing

from applib import sh

__all__ = ['implementors']


class CompressedFile:
    
    def __init__(self, filename):
        self.filename = filename

    def extractall_with_single_toplevel(self, f, names):
        """Same as ``extractall`` but ensures a single toplevel directory

        Some compressed archives do not stick to the convension of having a
        single top-level directory. For eg.,
        http://code.google.com/p/grapefruit/issues/detail?id=3

        In such cases, a new toplevel directory corresponding to the name of the
        compressed file (eg: 'grapefruit-0.1a3' if compressed file is named
        'grapefruit-0.1a3.tar.gz') is created and then extraction happens
        *inside* that directory.

        - f:     tarfile/zipefile file object
        - names: List of filenames in the archive

        Return the absolute path to the toplevel directory.
        """
        toplevels = _find_top_level_directories(names, sep='/')

        if len(toplevels) == 0:
            raise sh.PackError('archive is empty')
        elif len(toplevels) > 1:
            toplevel = _archive_basename(self.filename)
            os.mkdir(toplevel)
            with sh.cd(toplevel):
                f.extractall()
            return path.abspath(toplevel)
        else:
            f.extractall()
            toplevel = path.abspath(toplevels[0])
            assert path.exists(toplevel)
            if not path.isdir(toplevel):
                # eg: http://pypi.python.org/pypi/DeferArgs/0.4
                raise SingleFile('archive has a single file: %s', toplevel)
            return toplevel
        
        

class ZippedFile(CompressedFile):
    """A zip file"""

    @staticmethod
    def is_valid(filename):
        return zipfile.is_zipfile(filename)

    def extract(self):
        try:
            f = zipfile.ZipFile(self.filename, 'r')
            try:
                return self.extractall_with_single_toplevel(
                    f, f.namelist())
            except OSError as e:
                if e.errno == 17:
                    # http://bugs.python.org/issue6510
                    raise sh.PackError(e)
                # http://bugs.python.org/issue6609
                if sys.platform.startswith('win'):
                    if isinstance(e, WindowsError) and e.winerror == 267:
                        raise sh.PackError('uses Windows special name (%s)' % e)
                raise
            except IOError as e:
                # http://bugs.python.org/issue10447
                if sys.platform == 'win32' and e.errno == 2:
                    raise sh.PackError('reached max path-length: %s' % e)
                raise
            finally:
                f.close()
        except (zipfile.BadZipfile, zipfile.LargeZipFile) as e:
            raise sh.PackError(e)

    @classmethod
    def pack(cls, paths, file):
        raise NotImplementedError('pack: zip files not supported yet')
    

class TarredFile(CompressedFile):
    """A tar.gz/bz2 file"""
    
    @classmethod
    def is_valid(cls, filename):
        try:
            with closing(tarfile.open(filename, cls._get_mode())) as f:
                return True
        except tarfile.TarError:
            return False

    def extract(self):
        try:
            f = tarfile.open(self.filename, self._get_mode())
            try:
                _ensure_read_write_access(f)
                return self.extractall_with_single_toplevel(
                    f, f.getnames())
            finally:
                f.close()
        except tarfile.TarError as e:
            raise sh.PackError(e)
        except IOError as e:
            # see http://bugs.python.org/issue6584
            if 'CRC check failed' in str(e):
                raise sh.PackError(e)
            # See github issue #10
            elif e.errno == 22 and "invalid mode ('wb')" in str(e):
                raise sh.PackError(e)
            else:
                raise
            
    @classmethod
    def pack(cls, paths, file):
        f = tarfile.open(file, cls._get_mode('w'))
        try:
            for pth in paths:
                assert path.exists(pth), '"%s" does not exist' % path
                f.add(pth)
        finally:
            f.close()

    def _get_mode(self):
        """Return the mode for this tarfile"""
        raise NotImplementedError()


class GzipTarredFile(TarredFile):
    """A tar.gz2 file"""

    @staticmethod
    def _get_mode(mode='r'):
        assert mode in ['r', 'w']
        return mode + ':gz'


class Bzip2TarredFile(TarredFile):
    """A tar.gz2 file"""

    @staticmethod
    def _get_mode(mode='r'):
        assert mode in ['r', 'w']
        return mode + ':bz2'


implementors = dict(
    zip = ZippedFile,
    tgz = GzipTarredFile,
    bz2 = Bzip2TarredFile)


class MultipleTopLevels(sh.PackError):
    """Can be extracted, but contains multiple top-level dirs"""
class SingleFile(sh.PackError):
    """Contains nothing but a single file. Compressed archived is expected to
    contain one directory
    """
    
def _ensure_read_write_access(tarfileobj):
    """Ensure that the given tarfile will be readable and writable by the
    user (the client program using this API) after extraction.

    Some tarballs have u-x set on directories or u-w on files. We reset such
    perms here.. so that the extracted files remain accessible for reading
    and deletion as per the user's wish.

    See also: http://bugs.python.org/issue6196
    """
    dir_perm = tarfile.TUREAD | tarfile.TUWRITE | tarfile.TUEXEC
    file_perm = tarfile.TUREAD | tarfile.TUWRITE

    for tarinfo in tarfileobj.getmembers():
        tarinfo.mode |= (dir_perm if tarinfo.isdir() else file_perm)
        

def _find_top_level_directories(fileslist, sep):
    """Find the distinct first components in the fileslist"""
    toplevels = set()
    for pth in fileslist:
        firstcomponent = pth.split(sep, 1)[0]
        toplevels.add(firstcomponent)
    return list(toplevels)
    

def _archive_basename(filename):
    """Return a suitable base directory name for the given archive"""
    exts = (
        '.tar.gz',
        '.tgz',
        '.tar.bz2',
        '.bz2',
        '.zip')

    filename = path.basename(filename)
    
    for ext in exts:
        if filename.endswith(ext):
            return filename[:-len(ext)]
    return filename + '.dir'
