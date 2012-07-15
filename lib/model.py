# -*- coding: utf-8 -*-

import os
import conf
import re
#from memoize import Memoizer

#store = {}
#memo = Memoizer(store)


class NodeManager(object):

    def search_by_path(self, path):
        node = self.build_by_path(path)

        if node and node.parent and node in node.parent.children:
            return node

    def build_by_path(self, path):
        node = None
        node = conf.get_root_node()
        path = re.sub("^%s+" % re.escape(os.sep), "", path + os.sep)
        path = re.sub(os.sep + "+", os.sep, path)
        path = re.sub("^" + os.sep, "", path)
        splitted_path = path.split(os.path.sep)[:-1]

        if len(splitted_path):
            for idx in xrange(len(splitted_path)):
                path_slice = splitted_path[idx]
                node = node.build_child(pattern=path_slice)

                if not node:
                    break

        return node


class NodeProfile(object):

    abstract_nodes = []

    def __init__(self, abstract_nodes):
        self.abstract_nodes = abstract_nodes


class AbstractNode(object):

    writable = False
    selector = None
    abstract_nodes = []

    def __init__(self, selector, abstract_nodes=[], writable=writable):
        self.selector = selector
        self.abstract_nodes = abstract_nodes
        self.writable = writable

    def __str__(self):
        return str(self.selector)

    @property
    def is_leaf_generator(self):
        return self.selector.is_leaf_generator

    @property
    def weight(self):
        return self.selector.weight

    def abstract_nodes_by_weight(self, only_writables=False):
        from operator import attrgetter

        abstract_nodes = [abn for abn in self.abstract_nodes if not only_writables or abn.writable == only_writables]

        return sorted(abstract_nodes, key=attrgetter('weight'))

    def match_child(self, parent_node, pattern, only_writables=False):
        abstract_node = None
        abstract_nodes = self.abstract_nodes_by_weight(only_writables=only_writables)

        for an in abstract_nodes:
            if an.matches_node_pattern(parent_node, pattern):
                abstract_node = an
                break

        return abstract_node

    def matches_node_pattern(self, parent_node, pattern):
        return self.selector.matches_node_pattern(parent_node, pattern)

    def get_children_of_node(self, node):
        nodes = []

        for abstract_node in self.abstract_nodes:
            nodes += abstract_node.get_nodes(parent_node=node)

        return nodes

    def add_node(self, node):
        return node.abstract_node.selector.add_node(node)

    def read_node_contents(self, node, size=-1, offset=0):
        return self.selector.read_node_contents(node, size, offset)

    def node_contents_length(self, node):
        return self.selector.node_contents_length(node)

    def get_nodes(self, parent_node):
        return self.selector.get_nodes(self, parent_node)

    def write_node_contents(self, node, data, reset=False):
        if not self.selector.is_leaf_generator:
            raise TypeError("Node(%s) is not writable, 'cause selector.is_leaf_generator is false" % node)

        return self.selector.write_node_contents(node, data, reset)

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

    def __init__(self, pattern, abstract_node, parent=None, is_root=False, is_leaf=False):
        if not isinstance(abstract_node, AbstractNode):
            raise TypeError('abstract_node should be an AbstractNode')

        if not parent:
            is_root = True

        if is_root:
            parent = None

        self.pattern = pattern
        self.parent = parent
        self.abstract_node = abstract_node
        self.is_root = is_root
        self.is_leaf = is_leaf

    def __str__(self):
        return "(%s) %s" % (self.abstract_node, self.pattern)

    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def id(self):
        return long("".join(str(int(ord(l))) for l in tuple(self.path)))

    @property
    def path(self):
        path = ''

        if self.parent:
            path = self.parent.path + self.pattern

        if not self.is_leaf:
            path += os.sep

        return path

    @property
    def children(self):
        return self.abstract_node.get_children_of_node(self)

    @property
    def contents_length(self):
        return self.abstract_node.node_contents_length(self)

    @property
    def contents(self):
        return self.read_contents()

    def build_child(self, pattern):
        abstract_node = self.abstract_node.match_child(self, pattern)

        if not abstract_node:
            return None

        return Node(parent=self, pattern=pattern, abstract_node=abstract_node, is_leaf=abstract_node.is_leaf_generator)

    def read_contents(self, size=-1, offset=0):
        return self.abstract_node.read_node_contents(self, size, offset)

    def write_contents(self, data, reset=False):
        self.abstract_node.write_node_contents(self, data, reset)

    def create_child_by_pattern(self, pattern):
        abstract_node = self.abstract_node.match_child(self, pattern, only_writables=True)

        if not abstract_node:
            return None

        # TODO melhorar esta logica de verificacao de folhas, pq nao deve ser possivel criar um noh folha para um selector que nao eh gerador de folhas
        node = Node(parent=self, pattern=pattern, abstract_node=abstract_node, is_leaf=abstract_node.is_leaf_generator)
        abstract_node.add_node(node)

        return node
