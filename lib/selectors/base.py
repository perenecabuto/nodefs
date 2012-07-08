# -*- coding: utf-8 -*-

from ..model import Node
import weights


class Selector(object):

    weight = weights.DEFAULT
    is_leaf_generator = False

    def get_nodes(self, abstract_node, node=None):
        raise NotImplemented("You must implement get nodes to retrieve nodes from somewhere")

    def matches_node_pattern(self, abstract_node, pattern):
        raise NotImplemented("You must implement matches_node_pattern to check if the pattern can be from this selector")

    def read_node_contents(self, node, mode):
        raise NotImplemented("You must implement ->read_node_contents<- to get contents of a leaf node")

    def write_node_contents(self, node, data, reset=False):
        raise NotImplemented("You must implement ->write_node_contents<- to write contents of a leaf node")

    def node_contents_length(self, node):
        raise NotImplemented("You must implement ->node_contents_length<- to get contents length of a leaf node")

    def add_node(self, node):
        raise NotImplemented("You must implement ->add_node<-")


class StaticSelector(Selector):

    weight = weights.EXTRA_LIGHT
    projection = ''

    def __init__(self, projection, contentfile_path=None):
        self.projection = projection
        self.contentfile_path = contentfile_path
        self.is_leaf_generator = bool(contentfile_path)

    def __str__(self):
        return type(self).__name__

    def matches_node_pattern(self, abstract_node, pattern):
        return pattern == self.projection

    def get_nodes(self, abstract_node, node=None):
        return [
            Node(
                pattern=self.projection,
                parent=node,
                abstract_node=abstract_node,
                is_leaf=self.is_leaf_generator,
            )
        ]

    def read_node_contents(self, node, size=-1, offset=0):
        contents = ''

        if node.is_leaf and self.is_leaf_generator:
            f = open(self.contentfile_path, 'r')
            f.seek(offset)
            contents = f.read(size)
            f.close()

        return contents

    def write_node_contents(self, node, data, reset=False):
        file_mode = 'a'

        if reset:
            file_mode = 'w'

        f = open(self.contentfile_path, file_mode)
        f.write(data)
        f.close()

    def node_contents_length(self, node):
        f = open(self.contentfile_path, 'r')
        f.seek(0, 2)
        size = f.tell()
        f.close()

        return size


class MemorySelector(Selector):

    weight = weights.LIGHT
    is_leaf_generator = True
    cached_nodes = {}

    def get_nodes(self, abstract_node, node=None):
        return [
            Node(pattern=p, parent=node, abstract_node=abstract_node, is_leaf=self.is_leaf_generator)
            for p in self.cached_nodes.keys()
        ]

    def matches_node_pattern(self, abstract_node, pattern):
        return pattern in self.cached_nodes.keys()

    def read_node_contents(self, node, size=-1, offset=0):
        return self.cached_nodes.get(node.pattern, '')

    def write_node_contents(self, node, data, reset=False):
        self.cached_nodes[node.pattern] = data

    def node_contents_length(self, node):
        return len(self.cached_nodes.get(node.pattern, '') or '')

    def add_node(self, node):
        self.cached_nodes[node.pattern] = None
