# -*- coding: utf-8 -*-

from model import Node


class Selector(object):

    def __init__(self, projection):
        self._projection = projection

    @property
    def projection(self):
        """How the objects selected from the selector will behave"""
        return self._projection

    def get_nodes(self, abstract_node, node):
        raise NotImplemented("You must implement get nodes to retrieve nodes from somewhere")


class StaticSelector(Selector):

    def get_nodes(self, abstract_node, node):
        return [
            Node(
                pattern=self.projection,
                parent=node,
                abstract_node=abstract_node,
            )
        ]
