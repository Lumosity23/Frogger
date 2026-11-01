from dataclasses import dataclass

import pygame as pg
from pygame.rect import Rect


@dataclass
class Entity:
    col: float
    row: float
    img: pg.Surface | None = None
    is_alive: bool = False
    clock: float = 0.0

    @property
    def gpos(self) -> tuple[float, float]:
        return (self.col, self.row)

    @property
    def lift(self) -> float:
        return 0.0

    @property
    def size(self) -> tuple[int, int]:
        return self.img.get_size()
