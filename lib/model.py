# -*- coding: utf-8 -*-

import os
import conf
import re


class NodeManager(object):

    def search_by_path(self, path):
        node = None
        node = conf.get_root_node()
        path = re.sub("^%s+" % re.escape(os.sep), "", path)
        path = re.sub("/+", "/", path)
        splitted_path = path.split(os.path.sep)

        if len(splitted_path) > 1:
            for idx in xrange(len(splitted_path)):
                path_slice = splitted_path[idx]
                node = self.get_node(idx, node, path_slice)

        return node

    def get_node(self, level, parent, pattern):
        abstract_node = self.search_abstract_node(parent_node=parent, level=level, pattern=pattern),
        return Node(parent=parent, pattern=pattern, abstract_node=abstract_node)

    def search_node(parent_node, abstract_node, pattern):
        node = None

        try:
            [nd for nd in parent_node.children if nd.pattern == pattern][0]
        except IndexError:
            pass

        return node

    def search_abstract_node(self, parent_node, level, pattern):
        abstract_node = None
        abstract_nodes = conf.get_abstract_nodes_by_level(parent_node, level)

        if len(abstract_nodes) == 1:
            abstract_node = abstract_nodes[0]
        elif len(abstract_nodes) > 1:
            abstract_node = self.search_node(parent_node, abstract_node, pattern).abstract_node

        return abstract_node


class NodeProfile(object):

    abstract_nodes = []

    def __init__(self, abstract_nodes):
        self.abstract_nodes = abstract_nodes


class AbstractNode(object):

    selector = None
    abstract_nodes = []

    def __init__(self, selector, abstract_nodes=[]):
        self.selector = selector
        self.abstract_nodes = abstract_nodes

    def get_children_of_node(self, node):
        nodes = []

        for abstract_node in self.abstract_nodes:
            nodes += abstract_node.get_nodes(parent_node=node)

        return nodes

    def get_nodes(self, parent_node):
        return self.selector.get_nodes(self, parent_node)

    def get_node(self, parent_node, pattern):
        node = None

        for nd in self.get_nodes(parent_node):
            if nd.pattern == pattern:
                node = nd
                break

        return node


class Node(object):

    parent = None
    pattern = ''
    abstract_node = None
    is_root = False
    is_leaf = False

    def __init__(self, pattern, parent, abstract_node, is_root=False):
        if not isinstance(abstract_node, AbstractNode):
            raise TypeError('abstract_node should be an AbstractNode')

        self.pattern = pattern
        self.parent = parent
        self.abstract_node = abstract_node
        self.is_root = is_root

    def __unicode__(self):
        return "(%s) %s" % (self.abstract_node, self.pattern)

    @property
    def path(self):
        """docstring for path"""
        path = ''

        if self.parent:
            path = self.parent.path + self.pattern

        if not self.is_leaf:
            path += os.sep

        return path

    @property
    def children(self):
        return self.abstract_node.get_children_of_node(self)
