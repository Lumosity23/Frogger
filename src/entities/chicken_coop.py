import os
from typing import override

from src.entities.entity import Entity

ROOT = os.path.dirname(os.path.abspath(__name__))
ASSETS = os.path.join(ROOT, "assets")
PATH = os.path.join(ASSETS, "chicken_coop.png")


class chicken_coop(Entity):
    def __init__(self, col, row, scale):
        super().__init__(col, row, scale)
        self.duration = 0.7
        self.is_alive = True
        self.lsize = (1, 1)
        self.is_movable = False
        self.imgs = self.get_anim(1, PATH, scale)  # une frame = une case
        self.img = self.imgs[0]
        self.lift_val = -10.0 * scale

    @property
    @override
    def lift(self) -> float:
        return self.lift_val
