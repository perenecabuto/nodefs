# -*- coding: utf-8 -*-

import os

from nodefs.lib.selectors.base import StaticSelector, MemorySelector
from nodefs.lib.shortcuts import profile, absnode


schema = {
    'default': profile([
        absnode(StaticSelector('folder_1'), [
            absnode(StaticSelector('folder_1.1'), [
                absnode(MemorySelector(), writable=True),
                absnode(StaticSelector('folder_1.1.2')),
                absnode(
                    StaticSelector(
                        projection='contentfile.txt',
                        contentfile_path=os.path.dirname(__file__) + "/contentfile.txt",
                    ),
                ),
            ]),

            absnode(StaticSelector(projection='folder_1.2'), [
                absnode(StaticSelector('folder_1.2.1')),
                absnode(StaticSelector('folder_1.2.2')),
            ]),
        ]),

        absnode(StaticSelector(projection='folder_2'), [
            absnode(StaticSelector(projection='folder_2.1'), [
                absnode(StaticSelector(projection='folder_2.1.1')),
            ]),
        ]),
    ])
}
