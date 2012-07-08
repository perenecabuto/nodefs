# -*- coding: utf-8 -*-

import unittest
from lib.model import NodeManager
from lib.model import Node
from lib.model import NodeProfile
from tests.fixtures import profiles
from lib import conf

conf.node_profiles = profiles.schema


class FunctionalTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.node_manager = NodeManager()

    def test_get_default_node_profile(self):
        profile = conf.get_current_node_profile()
        self.assertIsInstance(profile, NodeProfile)

    def test_get_root_node_from_path(self):
        """Ao passar o path raiz deve retornar o root node"""

        node = self.node_manager.search_by_path('/')
        self.assertIsInstance(node, Node)
        self.assertTrue(node.is_root)

    def test_list_root_node_from_path(self):
        """Ao passar o path raiz deve retornar um array com seus nodes filhos"""

        node = self.node_manager.search_by_path('/')
        self.assertIsInstance(node, Node)
        self.assertIsInstance(node.children, list)
        self.assertGreater(len(node.children), 0)
        self.assertEqual(node.children[0].path, '/folder_1/')
        self.assertEqual(node.children[1].path, '/folder_2/')

    def test_get_second_level_node_children(self):
        node = self.node_manager.search_by_path('/folder_1/')
        self.assertEqual(node.children[0].path, '/folder_1/folder_1.1/')
        self.assertEqual(node.children[1].path, '/folder_1/folder_1.2/')

    def test_get_file_nodes_content(self):
        node = self.node_manager.search_by_path('/folder_1/folder_1.1/contentfile.txt')

        self.assertEqual(node.read_contents(), 'this is the content of contentfile.txt\n')

    def test_add_file(self):
        node = self.node_manager.search_by_path('/folder_1/folder_1.1/')

        new_node = node.create_child_by_pattern('test_file_1.txt')
        self.assertIn(new_node, node.children)

        new_node.write_contents("test file contents")

        gotten_node_contents = self.node_manager.search_by_path(new_node.path).contents
        self.assertEqual(new_node.contents, gotten_node_contents)
