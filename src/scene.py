import pygame as pg

from src.entities.chicken import Chicken
from src.map.grid import Grid
from src.render import *
from src.utils import log
from src.utils.camera import Camera

# from entities.entity import Entity
from src.utils.projection import Projection

MOVES: dict[int, tuple[int, int]] = {
    pg.K_LEFT: (-1, 0),
    pg.K_RIGHT: (1, 0),
    pg.K_UP: (0, -1),
    pg.K_DOWN: (0, 1),
}


class Scene:
    def __init__(self, screen_size: tuple[int, int], scale: float = 1.0) -> None:
        # Elements of the game
        self.PROJ: Projection = Projection.deformation(1.1, 0.7, 15, 50 * scale)
        self.grid: Grid = Grid(screen_size, self.PROJ, scale)
        self.cam: Camera = Camera(screen_size)
        col, row = self.PROJ.unproject(screen_size[0] / 2, screen_size[1] / 2)
        self.chicken: Chicken = Chicken(round(col), round(row))

    def update(self, dt: float):
        self.cam.follow(self.PROJ.cell_center(*self.chicken.gpos), dt)

    def handle_events(self, events: list[pg.Event]) -> bool:
        for event in events:
            if event.type == pg.KEYDOWN and event.key in MOVES:
                self.chicken.move(*MOVES[event.key])
                return True
        return False

    def draw(self, screen: pg.Surface) -> None:
        visible_tiles = self.grid.visible_rows(self.cam.visible_rect)
        draw_grid(screen, visible_tiles, self.PROJ, self.cam)
        draw_entities(screen, [self.chicken], self.PROJ, self.cam)
