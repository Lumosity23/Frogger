# from dataclasses import dataclass

import pygame as pg

# from src.utils.vector2 import Vector2

"""@dataclass
class Chicke:
    x: float
    y: float
    pos: Vector2 = Vector2(x, self.y)"""


class Chicken:
    def __init__(self, x: float, y: float, step: float) -> None:
        # self.pos: Vector2 = Vector2(x, y)
        self.img: pg.Surface = pg.image.load("assets/chicken.png").convert_alpha()
        self.rect: pg.Rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.step = step
        self.is_alive: bool = True
        self.face_dir = {
            "nord": pg.image.load("assets/chicken.png").convert_alpha(),
            "sud": pg.image.load("assets/chicken.png").convert_alpha(),
            "est": pg.image.load("assets/chicken.png").convert_alpha(),
            "ouest": pg.image.load("assets/chicken.png").convert_alpha()
        }
        self.current_dir = "nord"

    def draw(self, screen: pg.Surface):
        screen.blit(self.face_dir[self.current_dir], self.rect)
        
        



    def process_event(self):
        """chicken's controls"""
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.rect.x += self.step
            return True
        if keys[pg.K_LEFT]:
            self.rect.x -= self.step
            return True
        if keys[pg.K_UP]:
            self.rect.y -= self.step
            return True
        if keys[pg.K_DOWN]:
            self.rect.y += self.step
            return True

    