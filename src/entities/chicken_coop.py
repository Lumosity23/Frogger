import os
from typing import override
import pygame as pg

from src.entities.entity import Entity

ROOT = os.path.dirname(os.path.abspath(__name__))
ASSETS = os.path.join(ROOT, "assets")
PATH = os.path.join(ASSETS, "chicken_coop_anim.png")

#dict[int, pg.Surface]

class Chicken_coop(Entity):
    def __init__(self, col, row, scale):
        super().__init__(col, row, scale)
        self.duration = 0.7
        self.is_alive = True
        self.lsize = (1, 1)
        self.is_movable = False
        self.is_occupied: bool = False
        imgs = self.get_anim(2, PATH, scale)
        self.imgs = {}
        for i, img in imgs.items():
            self.imgs[bool(i)] = img
        self.lift_val = -10.0 * scale
        
    @property
    @override
    def lift(self) -> float:
        return self.lift_val

    @property
    def img(self):
        return self.imgs[self.is_occupied].copy()

    @img.setter
    def img(self, image: pg.Surface):
        pass



#image change quand pos_chicken == pos un coop
