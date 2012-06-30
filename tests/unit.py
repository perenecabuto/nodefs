# -*- coding: utf-8 -*-

import unittest
from lib.model import Node


class TestNode(unittest.TestCase):

    def test_instance(self):
        self.assertTrue(Node())
