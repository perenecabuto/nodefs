#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from fuse import FUSE
import logging
logging.basicConfig(level=logging.INFO)

from lib.fs import NodeFS

NODEFS_PROFILE_MODULE = os.environ.get('NODEFS_PROFILE_MODULE') or 'nodefs_schema'

#sys.path.append(os.path.abspath('.'))

try:
    __import__(NODEFS_PROFILE_MODULE)
    profile = sys.modules[NODEFS_PROFILE_MODULE]
except ImportError, e:
    print """
        You need to set you nodefs schema module.
        It can be a nodefs_schema.py on the the root of your project (by convinience)
        or it can be set by an export NODEFS_PROFILE_MODULE=my.beautiful.nodefs_schema on shell
    """

    if e:
        print "! An exception has occurred: ", e.message

    sys.exit(1)

from lib import conf

conf.node_profiles = profile.schema


def mount(path):
    """docstring for mount"""

    FUSE(NodeFS(), path, foreground=True, nothreads=False, nonempty=True)


def do_mount():
    args = sys.argv[1:]
    if not args:
        print 'usage: %s <mountpoint>' % sys.argv[0]
        exit(1)

    path = args[0]

    print " * Mounting FS on %s" % path
    mount(path)

if __name__ == '__main__':
    do_mount()
