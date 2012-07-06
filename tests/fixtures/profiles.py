from lib.model import AbstractNode
from lib.model import NodeProfile
from lib.selectors.base import StaticSelector

import os

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
                            AbstractNode(
                                selector=StaticSelector(projection='folder_1.1.2'),
                            ),
                            AbstractNode(
                                selector=StaticSelector(
                                    projection='contentfile.txt',
                                    contentfile_path=os.path.dirname(__file__) + "/contentfile.txt",
                                ),
                            ),
                        ]
                    ),

                    AbstractNode(
                        selector=StaticSelector(projection='folder_1.2'),
                        abstract_nodes=[
                            AbstractNode(
                                selector=StaticSelector(projection='folder_1.2.1'),
                            ),
                            AbstractNode(
                                selector=StaticSelector(projection='folder_1.2.2'),
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
