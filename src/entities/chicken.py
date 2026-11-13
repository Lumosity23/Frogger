import math
import os
from typing import override

import pygame as pg

from src.entities.entity import Entity

HOP_TIME = 0.25  # durée d'un saut (s)
HOP_HEIGHT = 17  # hauteur maximale du saut (px)

ROOT = os.path.dirname(os.path.abspath(__name__))
ASSETS = os.path.join(ROOT, "assets")
PATH = os.path.join(ASSETS, "chicken_faces.png")


class Chicken(Entity):
    def __init__(self, col: float, row: float, scale: float = 1.0) -> None:
        super().__init__(col, row, scale)
        self.face_dir: dict[tuple[int, int], pg.Surface] = self.get_faces(
            "assets/chicken_faces.png", scale
        )
        self.img = self.face_dir[(0, 1)].copy()
        self.is_alive: bool = True
        self.clock: float = 1.0
        self.from_cell: tuple[float, float] = (col, row)
        self.last_pos = (self.col, self.row)
        self.lsize = 0.6, 0.6

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

    def get_faces(self, path: str, scale: float) -> dict[tuple[int, int], pg.Surface]:
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        return {
            dir: img
            for dir, img in zip(directions, self.get_anim(4, path, scale).values())
        }

    def move(self, dcol: int, drow: int) -> None:
        """chicken's controls"""
        if not self.is_jumping:
            self.last_pos = (self.col, self.row)
            self.from_cell = self.last_pos
            self.col += dcol
            self.row += drow
            self.clock = 0.0
            self.img = self.face_dir[dcol, drow].copy()

    def update(self, dt: float) -> None:
        if self.is_jumping:
            self.clock = min(1.0, self.clock + dt / HOP_TIME)

    def jump(self) -> float:
        """The height of the jump"""
        return math.sin(self.clock * math.pi) * (HOP_HEIGHT * self.scale)
