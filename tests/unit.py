# -*- coding: utf-8 -*-

import unittest
from mock import mocksignature
from fuse import Operations

from lib.model import Node, AbstractNode, NodeProfile
from lib.selectors.base import StaticSelector
from lib.fs import NodeFS


class TestNode(unittest.TestCase):

    def setUp(self):
        abstract_node_class = mocksignature(AbstractNode, AbstractNode)
        selector_class = mocksignature(StaticSelector, StaticSelector)

        self.abstract_node = abstract_node_class(self)
        self.abstract_node.selector = selector_class(self)
        self.root_node = Node(pattern='', parent=None, abstract_node=self.abstract_node)

    def test_instance(self):
        self.assertIsInstance(self.root_node, Node)

    def test_id(self):
        node = Node(pattern='folder', parent=self.root_node, abstract_node=self.abstract_node)

        self.assertIsInstance(node.id, long)
        self.assertEqual(node.id, 4710211110810010111447L)

    def test_path(self):
        node = Node(pattern='folder', parent=self.root_node, abstract_node=self.abstract_node)
        self.assertIsInstance(node.path, unicode)

    def test_build_child(self):
        Node(pattern='folder', parent=self.root_node, abstract_node=self.abstract_node)
        self.abstract_node.match_child = lambda node, pattern: self.abstract_node

        self.assertIsInstance(self.root_node.build_child('folder'), Node)

    def test_children(self):
        node = Node(pattern='', parent=self.root_node, abstract_node=self.abstract_node)
        self.assertIsInstance(node.children, list)

    def test_read_contents(self):
        node = Node(pattern='', parent=self.root_node, abstract_node=self.abstract_node)
        self.abstract_node.read_node_contents = lambda node, size, offset: open('/etc/passwd').read()

        contents = node.read_contents()
        self.assertIsInstance(contents, str)


class TestAbstractNode(unittest.TestCase):

    def test_instance(self):
        abs_node = AbstractNode(selector=StaticSelector(''))

        self.assertTrue(abs_node)

    def test_read_node_contents(self):
        abs_node = AbstractNode(selector=StaticSelector(''))
        abs_node.read_node_contents = lambda node: open('/etc/passwd').read()
        node = mocksignature(Node, Node)

        self.assertIsInstance(abs_node.read_node_contents(node), str)


class TestStaticSelector(unittest.TestCase):

    def test_instance(self):
        selector = StaticSelector('')
        self.assertTrue(selector)

    def test_read_node_contents(self):
        test_fh = open('/etc/passwd')
        selector = StaticSelector(projection='', contentfile_path=test_fh.name)
        abs_node = AbstractNode(selector=selector)
        node = mocksignature(Node, Node)
        node.is_leaf = True

        contents = abs_node.read_node_contents(node)

        self.assertIsInstance(contents, str)
        self.assertEqual(contents, test_fh.read())


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

