import os
from typing import override

from src.entities.group import EntityGroup

ROOT = os.path.dirname(os.path.abspath(__name__))
ASSETS = os.path.join(ROOT, "assets")
PATH = os.path.join(ASSETS, "pig_anim.png")


class Pig(EntityGroup):
    def __init__(self, col, row, scale):
        super().__init__(col, row, scale)
        self.duration = 0.7
        self.is_alive = True
        self.lsize = (3, 1)
        self.imgs = self.get_anim(6, PATH, scale)
        self.lift_val = -20.0

    @property
    @override
    def lift(self) -> float:
        return self.lift_val
