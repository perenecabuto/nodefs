# -*- coding: utf-8 -*-

import os
import conf


class NodeManager(object):

    def search_by_path(self, path):
        node = None
        splitted_path = path.split(os.path.sep)
        node = conf.get_root_node()

        if len(splitted_path) > 0:
            pass

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

    def get_children_of_node(self, node):
        nodes = []

        for abstract_node in self.abstract_nodes:
            nodes += abstract_node.get_nodes(parent=node)

        return nodes

    def get_nodes(self, parent):
        return self.selector.get_nodes(self, parent)


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
