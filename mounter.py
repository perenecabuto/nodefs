#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from fuse import FUSE

from lib.fs import NodeFS

from tests.fixtures import profiles
from lib import conf

conf.node_profiles = profiles.schema


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
