# -*- coding: utf-8 -*-

node_profiles = {}
current_profile = 'default'
root_abstract_node = None
root_node = None


def get_current_node_profile():
    return get_node_profile(current_profile)


def get_node_profile(profile_name=None):
    profile_name = profile_name or current_profile
    return node_profiles.get(profile_name)


def get_root_abstract_node():
    global root_abstract_node

    if not root_abstract_node:
        from model import AbstractNode
        from selectors import StaticSelector
        root_abstract_node = AbstractNode(
            selector=StaticSelector(''),
            abstract_nodes=get_current_node_profile().abstract_nodes,
        )

    return root_abstract_node


def get_root_node():
    global root_node

    if not root_node:
        from model import Node
        root_node = Node(
            pattern='',
            parent=None,
            abstract_node=get_root_abstract_node(),
            is_root=True,
        )

    return root_node
