# -*- coding: utf-8 -*-

node_profiles = {}
current_profile = 'default'


def get_current_node_profile():
    return get_node_profile(current_profile)


def get_node_profile(profile_name=None):
    profile_name = profile_name or current_profile
    return node_profiles.get(profile_name)


def get_root_abstract_node():
    from lib.model import AbstractNode
    from lib.selectors import StaticSelector

    return AbstractNode(
        selector=StaticSelector(''),
        abstract_nodes=get_current_node_profile().abstract_nodes,
    )


def get_abstract_nodes_by_level(level):
    i = 0
    abstract_nodes = get_current_node_profile().abstract_nodes

    while (i < level):
        _abstract_nodes = []

        for an in abstract_nodes:
            _abstract_nodes += an.abstract_nodes

        abstract_nodes = _abstract_nodes
        i += 1

    return abstract_nodes


def get_root_node():
    from lib.model import Node
    return Node(
        pattern='',
        parent=None,
        abstract_node=get_root_abstract_node(),
        is_root=True,
    )
