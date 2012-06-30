# -*- coding: utf-8 -*-


class NodeManager(object):

    def search_by_path(self, path):
        node = Node()

        return node


class Node(object):

    parent = None
    abstract_node = None

    def __init__(self, pattern, parent, abstract_node):
        if not is_instance(abstract_node, AbsbractNode):
            raise 

        self.pattern = pattern
        self.parent = parent
        self.abstract_node = abstract_node
