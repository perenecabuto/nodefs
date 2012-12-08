# -*- coding: utf-8 -*-

import os
import sys

NODEFS_PROFILE_MODULE = os.environ.get('NODEFS_PROFILE_MODULE') or 'nodefs_schema'

try:
    __import__(NODEFS_PROFILE_MODULE)
    profile = sys.modules[NODEFS_PROFILE_MODULE]
    schema = profile.schema
except ImportError, e:
    print """
        You need to set you nodefs schema module.
        It can be a nodefs_schema.py on the the root of your project (by convinience)
        or it can be set by an export NODEFS_PROFILE_MODULE=my.beautiful.nodefs_schema on shell
    """

    if e:
        print "! An exception has occurred: ", e.message

    sys.exit(1)

