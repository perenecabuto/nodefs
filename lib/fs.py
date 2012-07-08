#!/usr/bin/env python
# -*- encoding : utf-8 -*-

from errno import ENOENT
from stat import S_IFDIR, S_IFREG
from time import time

from fuse import FuseOSError
from fuse import Operations
from fuse import LoggingMixIn

from lib.model import NodeManager


class NodeFS(Operations, LoggingMixIn):

    def init(self, path):
        print "init path: %s" % (path,)

        self.node_manager = NodeManager()

    def create(self, path, mode):
        print "create ", path, " ", mode

        splitted_path = path.split("/")
        node_path = "/".join(splitted_path[:-1])
        pattern = splitted_path[-1]
        node = self.node_manager.search_by_path(node_path)
        node.create_child_by_pattern(pattern, is_leaf=True)

        return node.id

    def getattr(self, path, fh=None):
        print "getattr path: %s, fh: %s" % (path, fh)

        now = time()
        node = self.node_manager.search_by_path(path)

        if node:
            if node.is_leaf:
                # File
                return dict(st_mode=(S_IFREG | 0o644), st_ctime=now, st_mtime=now, st_atime=now, st_nlink=1, st_size=node.contents_length)
            else:
                # Dir
                return dict(st_mode=(S_IFDIR | 0o755), st_ctime=now, st_mtime=now, st_atime=now, st_nlink=2)

        raise FuseOSError(ENOENT)

    def readdir(self, path, fh):
        print "readdir path:", path

        dir_content = ['.', '..']
        node = self.node_manager.search_by_path(path)

        dir_content += [n.pattern for n in node.children]

        return dir_content

    def read(self, path, size, offset, fh):
        print "read ", path, " ", size, " ", offset, " ", fh
        node = self.node_manager.search_by_path(path)

        return node.read_contents(size, offset)

    def write(self, path, data, offset, fh):
        print "write ", path, " ", offset, " ", fh

        node = self.node_manager.search_by_path(path)
        node.write_contents(data, reset=offset == 0)

        return len(data)

    def truncate(self, path, length, fh=None):
        print "truncate ", path, " ", length, " ", fh

    def setxattr(self, path, name, value, options, position=0):
        print "setxattr"
        # Ignore options
        #attrs = self.files[path].setdefault('attrs', {})
        #attrs[name] = value

    def statfs(self, path):
        print "statfs"

        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)

    def mkdir(self, path, mode):
        print "mkdir ", path, " ", mode

        splitted_path = path.split("/")
        node_path = "/".join(splitted_path[:-1])
        pattern = splitted_path[-1]
        node = self.node_manager.search_by_path(node_path)
        node.create_child_by_pattern(pattern, is_leaf=False)

    def unlink(self, path):
        print "unlink"

        self.files.pop(path)

    def utimens(self, path, times=None):
        print "utimens"

        now = time()
        atime, mtime = times if times else (now, now)
        self.files[path]['st_atime'] = atime
        self.files[path]['st_mtime'] = mtime
