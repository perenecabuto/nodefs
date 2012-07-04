# -*- coding: utf-8 -*-

import unittest
from mock import mocksignature
from fuse import Operations

from lib.model import Node, AbstractNode, NodeProfile
from lib.selectors.base import StaticSelector
from lib.fs import NodeFS


class TestNode(unittest.TestCase):

    def setUp(self):
        self.root_node = None
        self.abstract_node_class = mocksignature(AbstractNode, AbstractNode)
        self.abstract_node = self.abstract_node_class(self)

    def test_instance(self):
        node = Node(pattern='', parent=self.root_node, abstract_node=self.abstract_node)

        self.assertTrue(node)

    def test_id(self):
        node = Node(pattern='fakeid', parent=self.root_node, abstract_node=self.abstract_node)

        self.assertIsInstance(node.id, long)
        self.assertEqual(node.id, 10297107101105100L)


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


class TestNodeProfile(unittest.TestCase):

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


class TestNodeFS(unittest.TestCase):

    def def_instance(self):
        nodefs = NodeFS()
        self.assertIsInstance(nodefs, Operations)


