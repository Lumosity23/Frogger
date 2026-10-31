import pygame as pg

from src.entities.entity import Entity


class Chicken(Entity):
    def __init__(self, col: float, row: float) -> None:
        super().__init__(col, row)
        self.img: pg.Surface = pg.image.load("assets/chicken.png").convert_alpha()
        self.face_dir: dict[tuple[int, int], pg.Surface] = {
            (0, -1): pg.image.load("assets/chicken.png").convert_alpha(),
            (0, 1): pg.image.load("assets/chicken.png").convert_alpha(),
            (1, 0): pg.image.load("assets/chicken.png").convert_alpha(),
            (-1, 0): pg.image.load("assets/chicken.png").convert_alpha(),
        }
        self.current_dir: str = "nord"
        self.is_alive: bool = True

    def move(self, dcol: int, drow: int) -> None:
        """chicken's controls"""
        self.col += dcol
        self.row += drow
        # self.img = self.face_dir[(dcol, drow)].copy()
