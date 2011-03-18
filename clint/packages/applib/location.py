# Copyright (c) 2010 ActiveState Software Inc. All rights reserved.

# This module is deprecated

from appdirs import *


#---- self test code

if __name__ == "__main__":
    print("applib: user data dir: %s" % user_data_dir("Komodo", "ActiveState"))
    print("applib: site data dir: %s" % site_data_dir("Komodo", "ActiveState"))
    print("applib: user cache dir: %s" % user_cache_dir("Komodo", "ActiveState"))

