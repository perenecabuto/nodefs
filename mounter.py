#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from fuse import FUSE

from lib.fs import NodeFS

NODEFS_PROFILE_MODULE = os.environ.get('NODEFS_PROFILE_MODULE') or 'nodefs_schema'

try:
    __import__(NODEFS_PROFILE_MODULE)
    profile = sys.modules[NODEFS_PROFILE_MODULE]
except ImportError:
    print """
        You need to set you nodefs schema module.
        It can be a nodefs_schema.py on the the root of your django project (by convinience)
        or it can be set by an export NODEFS_PROFILE_MODULE=my.beautiful.nodefs_schema on shell
    """
    sys.exit(1)

from lib import conf

conf.node_profiles = profile.schema


def mount(path):
    """docstring for mount"""

    FUSE(NodeFS(), path, foreground=True, nothreads=True)


if __name__ == '__main__':

    args = sys.argv[1:]
    if not args:
        print 'usage: %s <mountpoint>' % sys.argv[0]
        exit(1)

    path = args[0]

    print " * Mounting FS on %s" % path
    mount(path)
