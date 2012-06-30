# -*- coding: utf-8 -*-

import unittest
from lib.model import NodeManager
from lib.model import Node


class FunctionalTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.node_manager = NodeManager()

    def test_list_root_node_from_path(self):
        """Ao passar o path raiz deve retornar um array"""

        result = self.node_manager.search_by_path('/')
        self.assertIsInstance(result, Node)
        pass

    #def test_root_nodes_as_test_profile(self):
        #"""Os nós filhos devem ser aqueles que foram especificados"""

        #result = self.node_manager.search_by_path('/')
        #expected = [
            #1,
            #2,
        #]

        #self.assertEqual(result, expected)
        #pass
