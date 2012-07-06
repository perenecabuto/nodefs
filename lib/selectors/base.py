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


class StaticSelector(Selector):

    weight = weights.EXTRA_LIGHT
    contentfile_path = None
    projection = ''

    def __init__(self, projection, contentfile_path=None):
        self.projection = projection
        self.contentfile_path = contentfile_path
        self.is_leaf_generator = bool(contentfile_path)

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

    def write_node_contents(self, node, data):
        f = open(self.contentfile_path, 'w')
        f.write(data)
        f.close()

    def append_node_contents(self, node, data):
        f = open(self.contentfile_path, 'a')
        f.write(data)
        f.close()

    def node_contents_length(self, node):
        f = open(self.contentfile_path, 'r')
        f.seek(0, 2)
        size = f.tell()
        f.close()

        return size
