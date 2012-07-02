# -*- coding: utf-8 -*-

from lib.model import Node
import weights


class Selector(object):
    weight = weights.DEFAULT

    def __init__(self, projection):
        self._projection = projection

    @property
    def projection(self):
        """How the objects selected from the selector will behave"""
        return self._projection

    def get_node(self, abstract_node, pattern):
        raise NotImplemented("You must implement get_node to retrieve a node")

    def get_nodes(self, abstract_node, node):
        raise NotImplemented("You must implement get nodes to retrieve nodes from somewhere")

    def matches_node_pattern(self, abstract_node, pattern):
        raise NotImplemented("You must implement matches_node_pattern to check if the pattern can be from this selector")


class StaticSelector(Selector):
    weight = weights.EXTRA_LIGHT

    def matches_node_pattern(self, abstract_node, pattern):
        return pattern == self.projection

    def get_node(self, abstract_node, pattern):
        return [node for node in self.get_nodes() if node.pattern == pattern][0]

    def get_nodes(self, abstract_node, node):
        return [
            Node(
                pattern=self.projection,
                parent=node,
                abstract_node=abstract_node,
            )
        ]
