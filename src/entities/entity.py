from dataclasses import dataclass

import pygame as pg


@dataclass
class Entity:
    col: float
    row: float
    img: pg.Surface | None = None
    rect: pg.Rect | None = None
    is_alive: bool = False

    @property
    def gpos(self) -> tuple[float, float]:
        return (self.col, self.row)
