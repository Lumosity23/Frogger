# from dataclasses import dataclass

import pygame as pg

# from src.utils.vector2 import Vector2

"""@dataclass
class Chicke:
    x: float
    y: float
    pos: Vector2 = Vector2(x, self.y)"""


class Chicken:
    def __init__(self, x: float, y: float) -> None:
        # self.pos: Vector2 = Vector2(x, y)
        self.img: pg.Surface = pg.image.load("assets/chicken.png").convert_alpha()
        self.rect: pg.Rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_alive: bool = True

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.rect)

    # def update(...)
    #   A toi de jouer !
