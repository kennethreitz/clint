# Copyright (c) 2010 ActiveState Software Inc. All rights reserved.

"""Base module"""

import sys
from os.path import abspath, join, expanduser
import logging

from appdirs import AppDirs

from applib import location, log
from applib.log import LogawareCmdln as Cmdln

__all__ = ['Application', 'Cmdln']


class Application(object):
    """Object representing the application
    
    - name:                   Name of the application
    
    - company:                Company developing the application
    
    - compatibility_version:  The major version which promises
                              backward-compatability among all of its minor
                              versions. Eg: 5.2; 5.2.1, 5.2.2, etc.. should
                              use the same compatability version (5.2). This
                              value is used in the settings directory path.
                              
    - locations:              An object holding a set of OS-specific but
                              generic location values (eg: APPDATA). See
                              ``Locations`` class for details.
    """

    def __init__(self, name, company, compatibility_version=None):
        self.name = name
        self.company = company
        self.compatibility_version = compatibility_version
        self.locations = AppDirs2(
            name, company, compatibility_version, roaming=False)
        
    def run(self, cmdln_class):
        """Run the application using the given cmdln processor.
        
        This method also ensures configuration of logging handlers for console
        """
        assert issubclass(cmdln_class, Cmdln)
        l = logging.getLogger('')
        log.setup_trace(l, self.locations.log_file_path)
        cmdln_class(install_console=True).main()


class AppDirs2(AppDirs):
    @property
    def log_file_path(self):
        if sys.platform in ('win32', 'darwin'):
            name = self.appname + '.log'
        else:
            name = self.appname.lower() + '.log'
        return join(self.user_log_dir, name)


if __name__ == '__main__':
    # self-test code
    app = Application('PyPM', 'ActiveState', '0.1')
    print('user_data_dir', app.locations.user_data_dir)
    print('site_data_dir', app.locations.site_data_dir)
    print('user_cache_dir', app.locations.user_cache_dir)
    print('log_file_path', app.locations.log_file_path)

