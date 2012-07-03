# -*- coding: utf-8 -*-

from ..model import Node
import weights


class Selector(object):

    weight = weights.DEFAULT

    def get_nodes(self, abstract_node, node=None):
        raise NotImplemented("You must implement get nodes to retrieve nodes from somewhere")

    def matches_node_pattern(self, abstract_node, pattern):
        raise NotImplemented("You must implement matches_node_pattern to check if the pattern can be from this selector")


class StaticSelector(Selector):

    weight = weights.EXTRA_LIGHT

    def __init__(self, projection):
        self.projection = projection

    def matches_node_pattern(self, abstract_node, pattern):
        return pattern == self.projection

    def get_nodes(self, abstract_node, node=None):
        return [
            Node(
                pattern=self.projection,
                parent=node,
                abstract_node=abstract_node,
            )
        ]
