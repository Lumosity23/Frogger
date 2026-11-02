import math
from typing import override

import pygame as pg
from pygame.math import Vector2

from src.entities.entity import Entity

HOP_TIME = 0.25  # durée d'un saut (s)
HOP_HEIGHT = 17  # hauteur maximale du saut (px)


class Chicken(Entity):
    def __init__(self, col: float, row: float, scale: float = 1.0) -> None:
        super().__init__(col, row, scale)
        self.img: pg.Surface = pg.image.load("assets/chicken.png").convert_alpha()
        self.img: pg.Surface = pg.transform.scale(
            self.img, Vector2(self.img.get_size()) * scale
        )
        self.face_dir: dict[tuple[int, int], pg.Surface] = {
            (0, -1): pg.image.load("assets/chicken.png").convert_alpha(),
            (0, 1): pg.image.load("assets/chicken.png").convert_alpha(),
            (1, 0): pg.image.load("assets/chicken.png").convert_alpha(),
            (-1, 0): pg.image.load("assets/chicken.png").convert_alpha(),
        }
        self.current_dir: str = "nord"
        self.is_alive: bool = True
        self.clock: float = 1.0
        self.from_cell: tuple[float, float] = (col, row)

    @property
    def is_jumping(self) -> bool:
        return self.clock < 1.0

    @property
    @override
    def lift(self) -> float:
        return self.jump()

    @property
    @override
    def gpos(self) -> tuple[float, float]:
        t = self.clock * self.clock * (3 - 2 * self.clock)
        fc, fr = self.from_cell
        return (fc + (self.col - fc) * t, fr + (self.row - fr) * t)

    def move(self, dcol: int, drow: int) -> None:
        """chicken's controls"""
        if not self.is_jumping:
            before = self.col, self.row
            self.from_cell = before
            self.col += dcol
            self.row += drow
            self.clock = 0.0

    def update(self, dt: float) -> None:
        if self.is_jumping:
            self.clock = min(1.0, self.clock + dt / HOP_TIME)

    def jump(self) -> float:
        """The height of the jump"""
        return math.sin(self.clock * math.pi) * (HOP_HEIGHT * self.scale)
