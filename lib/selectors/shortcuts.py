# -*- coding: utf-8 -*-

from ..model import AbstractNode
from ..model import NodeProfile


def profile(abstract_nodes):
    return NodeProfile(abstract_nodes=abstract_nodes)


def absnode(selector, sub_absnodes=[], writable=False):
    return AbstractNode(
        writable=writable,
        selector=selector,
        abstract_nodes=sub_absnodes
    )
