# -*- coding: utf-8 -*-

import os
import conf
import re
from memoize import Memoizer

store = {}
memo = Memoizer(store)


class NodeManager(object):

    def search_by_path(self, path):
        node = None
        node = conf.get_root_node()
        path = re.sub("^%s+" % re.escape(os.sep), "", path + os.sep)
        path = re.sub(os.sep + "+", os.sep, path)
        path = re.sub("^" + os.sep, "", path)
        splitted_path = path.split(os.path.sep)[:-1]

        if len(splitted_path):
            for idx in xrange(len(splitted_path)):
                path_slice = splitted_path[idx]
                node = node.get_child(pattern=path_slice)

                if not node:
                    break

        return node


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

    def match_child(self, pattern):
        abstract_node = None

        if len(self.abstract_nodes) == 1:
            abstract_node = self.abstract_nodes[0]
        else:
            for ab in self.abstract_nodes_by_weight:
                if ab.matches_node_pattern(pattern):
                    abstract_node = ab
                    break

        return abstract_node

    @property
    def weight(self):
        return self.selector.weight

    @property
    def abstract_nodes_by_weight(self):
        from operator import attrgetter
        return sorted(self.abstract_nodes, key=attrgetter('weight'))

    def matches_node_pattern(self, pattern):
        return self.selector.matches_node_pattern(self, pattern)

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

    def get_child(self, pattern):
        abstract_node = self.abstract_node.match_child(pattern)

        if abstract_node:
            return Node(parent=self, pattern=pattern, abstract_node=abstract_node)

    @property
    def id(self):
        if not hasattr(self, '_id'):
            self._id = long("".join(str(int(ord(l))) for l in list(self.pattern)))

        return self._id

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
