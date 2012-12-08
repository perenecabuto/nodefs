#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from fuse import FUSE

#import logging
#logging.basicConfig(level=logging.INFO)
from nodefs.lib.fs import NodeFS
from nodefs.lib import conf
from nodefs.lib import profile

conf.node_profiles = profile.schema


def mount(path):
    FUSE(NodeFS(), path, foreground=True, nothreads=False, nonempty=True)


def main():
    args = sys.argv[1:]

    if not args:
        print 'usage: %s <mountpoint>' % sys.argv[0]
        exit(1)

    path = args[0]

    print " * Mounting FS on %s" % path
    mount(path)


if __name__ == '__main__':
    main()

