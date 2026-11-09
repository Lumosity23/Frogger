import pygame as pg

from src.entities.chicken import Chicken
from src.entities.haybale import HayBale
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
        tile: float = 50
        grid_size: tuple = (15, 30)
        self.mode: str = "PROD"
        self.FLAT: Projection = Projection.flat(tile * scale)
        self.DEFO: Projection = Projection.deformation(1.1, 0.7, 15, tile * scale)
        self.proj: Projection = self.DEFO
        self.grid: Grid = Grid(grid_size, tile, scale)
        self.cam: Camera = Camera(screen_size)
        col, row = self.proj.unproject(screen_size[0] / 2, screen_size[1] / 2)
        self.chicken: Chicken = Chicken(round(grid_size[0]/2), 1, scale)
        self.haybale: HayBale = HayBale(round(col), round(row), scale)
        self.grid.grid[18] += self.haybale
        self.grid.grid[28] += self.chicken

    def update(self, dt: float):
        self.grid.update(dt)
        self.cam.follow(self.proj.cell_center(*self.chicken.gpos), dt)

    def handle_events(self, events: list[pg.Event]) -> bool:
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key in MOVES:
                    self.chicken.move(*MOVES[event.key])
                if event.key == pg.K_p:
                    if self.proj == self.DEFO:
                        self.proj = self.FLAT
                        self.mode = "DEBUG"
                        log.debug("PROJ -> FLAT")
                    else:
                        self.proj = self.DEFO
                        self.mode = "PROD"
                        log.debug("PROJ -> DEFORMATION")

        return False

    def draw(self, screen: pg.Surface) -> None:
        visible_tiles = self.grid.get_visible_tiles(self.cam.visible_rect, self.proj)
        all_entities = self.grid.get_visible_entities(self.cam.visible_rect, self.proj)
        draw_grid(screen, visible_tiles, self.proj, self.cam)
        draw_entities(screen, all_entities, self.proj, self.cam, self.mode)

    def update_chicken_chunk(self):
        last_row = self.chicken.last_pos[1]
        new_row = self.chicken.row
        if last_row != new_row:
            self.grid.grid[last_row] -= self.chicken 
            self.grid.grid[new_row] += self.chicken 
