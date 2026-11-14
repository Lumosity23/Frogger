import os
from dataclasses import dataclass

from src.entities.group import EntityGroup

ROOT = os.path.dirname(os.path.abspath(__name__))
ASSETS = os.path.join(ROOT, "assets")
PATH = os.path.join(ASSETS, "hay_bale_anim.png")


class HayBale(EntityGroup):
    def __init__(self, col, row, scale):
        super().__init__(col, row, scale)
        self.duration = 0.7
        self.is_alive = True
        self.lsize = (4, 1)
        self.imgs = self.get_anim(8, PATH, scale)  # une frame = une case
        self.img = self.imgs[0]
