import os

from src.entities.entity import Entity

# from map.chunk import Chunk

ROOT = os.path.dirname(os.path.abspath(__name__))
ASSETS = os.path.join(ROOT, "assets")
PATH = os.path.join(ASSETS, "hay_bale_anim.png")


class HayBale(Entity):
    def __init__(self, col, row, scale):
        super().__init__(col, row, scale)
        self.duration = 0.7
        self.is_alive = True
        self.imgs = self.get_anim(8, PATH, scale)
