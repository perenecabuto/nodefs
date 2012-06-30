# -*- coding: utf-8 -*-

import unittest
from mock import mocksignature
from lib.model import Node, AbstractNode, NodeProfile
from lib.selectors import StaticSelector


class TestNode(unittest.TestCase):

    def test_instance(self):
        root_node = None
        abstract_node_class = mocksignature(AbstractNode, AbstractNode)
        abstract_node = abstract_node_class(self)
        node = Node(
            pattern='',
            parent=root_node,
            abstract_node=abstract_node,
        )

        self.assertTrue(node)


class TestAbstractNode(unittest.TestCase):

    def test_instance(self):
        abs_node = AbstractNode(
            selector=StaticSelector('')
        )

        self.assertTrue(abs_node)


class TestStaticSelector(unittest.TestCase):

    def test_instance(self):
        selector = StaticSelector('')
        self.assertTrue(selector)


class NodeProfileTest(unittest.TestCase):

    def test_instance(self):
        node_profile = NodeProfile(
            abstract_nodes=[
                AbstractNode(
                    selector=StaticSelector(projection='')
                )
            ]
        )

        self.assertTrue(node_profile)
        self.assertIsInstance(node_profile.abstract_nodes, list)
