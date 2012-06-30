from lib.model import AbstractNode
from lib.model import NodeProfile
from lib.selectors import StaticSelector

schema = {
    'default': NodeProfile(
        abstract_nodes=[
            AbstractNode(selector=StaticSelector(projection='folder_1')),
            AbstractNode(selector=StaticSelector(projection='folder_2')),
        ]
    )
}
