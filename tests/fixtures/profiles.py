from lib.model import AbstractNode
from lib.model import NodeProfile
from lib.selectors import StaticSelector

schema = {
    'default': NodeProfile(
        abstract_nodes=[
            AbstractNode(
                selector=StaticSelector(projection='folder_1'),
                abstract_nodes=[
                    AbstractNode(
                        selector=StaticSelector(projection='folder_1.1'),
                        abstract_nodes=[
                            AbstractNode(
                                selector=StaticSelector(projection='folder_1.1.1'),
                            ),
                        ]
                    ),
                ]
            ),

            AbstractNode(
                selector=StaticSelector(projection='folder_2'),
                abstract_nodes=[
                    AbstractNode(
                        selector=StaticSelector(projection='folder_2.1'),
                        abstract_nodes=[
                            AbstractNode(
                                selector=StaticSelector(projection='folder_2.1.1'),
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )
}
