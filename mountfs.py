#!/usr/bin/env python
# -*- encoding : utf-8 -*-

import os
import sys
import re

from errno import ENOENT
from stat import S_IFDIR, S_IFREG
from time import time

from fuse import FUSE
from fuse import FuseOSError
from fuse import Operations
from fuse import LoggingMixIn

from contas.controle.models import Controle
#from contas.controle.models import Conta

from django.core.management.base import BaseCommand
#from django.core.management.base import CommandError


def parse_controle(path):
    return re.search('(\d{,2})-(\d{4})/?$', path)


def parse_conta(path):
    return re.search('(\d{,2})-(\d{4})/([^/]+)/?$', path)


def parse_arquivo(path):
    return re.search('(\d{,2})-(\d{4})/([^/]+)/([^/]+)?$', path)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not args:
            print 'usage: %s <mountpoint>' % sys.argv[0]
            exit(1)

        path = args[0]

        print " * Mounting FS on %s" % path
        FUSE(ContaFs(), path, foreground=True, nothreads=True)


class ContaFs(Operations, LoggingMixIn):
    """ blah blah blah """

    def init(self, path):
        print "init path: %s" % (path,)

    def create(self, path, mode):
        print "create"
        self.files[path] = dict(st_mode=(S_IFREG | mode), st_nlink=1,
            st_size=0, st_ctime=time(), st_mtime=time(), st_atime=time())
        self.fd += 1
        return self.fd

    def getattr(self, path, fh=None):
        print "getattr path: %s, fh: %s" % (path, fh)
        now = time()

        if path == '/':
            return dict(st_mode=(S_IFDIR | 0755), st_ctime=now, st_mtime=now, st_atime=now, st_nlink=1)

        m_controle = parse_controle(path)
        m_contas = parse_conta(path)
        m_arquivo = parse_arquivo(path)

        if m_controle or m_contas:
            return dict(st_mode=(S_IFDIR | 0755), st_ctime=now, st_mtime=now, st_atime=now, st_nlink=1)

        if m_arquivo:
            controle = Controle.objects.get(mes=m_arquivo.group(1), ano=m_arquivo.group(2))
            conta = controle.conta_set.get(nome__exact=m_arquivo.group(3))
            return dict(st_mode=(S_IFREG | 0644), st_ctime=now, st_mtime=now, st_atime=now, st_nlink=1, st_size=conta.arquivo.size)

        raise FuseOSError(ENOENT)

    def open(self, path, flags):
        print "open"
        return 1

    def read(self, path, size, offset, fh):
        print "read ", path, " ", size, " ", offset, " ", fh

        m_arquivo = parse_arquivo(path)
        controle = Controle.objects.get(mes=m_arquivo.group(1), ano=m_arquivo.group(2))
        conta = controle.conta_set.get(nome__exact=m_arquivo.group(3))

        f = conta.arquivo.file
        f.seek(offset, 0)
        buf = f.read(size)
        f.close()

        return buf

    def readdir(self, path, fh):
        print "readdir path:", path
        dir_content = ['.', '..']

        m_controle = parse_arquivo(path)
        m_contas = parse_conta(path)

        if m_controle:
            print "controle"
            controle = Controle.objects.get(mes=m_controle.group(1), ano=m_controle.group(2))
            dir_content += [str(conta) for conta in controle.conta_set.all()]

        elif m_contas:
            print "contas"
            controle = Controle.objects.get(mes=m_contas.group(1), ano=m_contas.group(2))
            conta = controle.conta_set.get(nome__exact=m_contas.group(3))
            dir_content += [os.path.basename(str(conta.arquivo))]

        elif path == '/':
            dir_content += [str(controle) for controle in Controle.objects.all()]

        return dir_content

    def setxattr(self, path, name, value, options, position=0):
        print "setxattr"
        # Ignore options
        attrs = self.files[path].setdefault('attrs', {})
        attrs[name] = value

    def statfs(self, path):
        print "statfs"
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)

    def truncate(self, path, length, fh=None):
        print "truncate"
        self.data[path] = self.data[path][:length]
        self.files[path]['st_size'] = length

    def unlink(self, path):
        print "unlink"
        self.files.pop(path)

    def utimens(self, path, times=None):
        print "utimens"
        now = time()
        atime, mtime = times if times else (now, now)
        self.files[path]['st_atime'] = atime
        self.files[path]['st_mtime'] = mtime

    def write(self, path, data, offset, fh):
        print "write"
        self.data[path] = self.data[path][:offset] + data
        self.files[path]['st_size'] = len(self.data[path])
        return len(data)
