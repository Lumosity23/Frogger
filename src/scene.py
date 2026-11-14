import pygame as pg

import src.map.generate_world as gw
from src.entities.chicken import Chicken
from src.entities.haybale import HayBale
from src.map.chunk import Chunk
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

# appeler get_seed


class Scene:
    def __init__(self, screen_size: tuple[int, int], scale: float = 1.0) -> None:
        # Elements of the game
        self.tile: float = 50.0
        grid_size: tuple[int, int] = (15, 30)
        self.mode: str = "PROD"
        self.FLAT: Projection = Projection.flat(self.tile * scale)
        self.DEFO: Projection = Projection.deformation(1.1, 0.7, 15, self.tile * scale)
        self.proj: Projection = self.DEFO
        # self.prep_world()
        self.grid: Grid = Grid(grid_size, self.tile, scale)
        self.cam: Camera = Camera(screen_size)
        col, row = self.proj.unproject(screen_size[0] / 2, screen_size[1] / 2)
        self.chicken: Chicken = Chicken(round(grid_size[0] / 2), 1, scale)
        self.haybale: HayBale = HayBale(round(col - 10), round(row), scale)
        self.grid.grid[18] += self.haybale
        self.grid.grid[28] += self.chicken

    def update(self, dt: float):
        self.grid.update(dt)
        if self.chicken.is_alive:
            self.update_chicken_chunk()
            self.cam.follow(self.proj.cell_center(*self.chicken.gpos), dt)

    def handle_events(self, event: pg.Event) -> bool:
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
        draw_entities(screen, all_entities, self.proj, self.cam, self.tile, self.mode)

    def update_chicken_chunk(self):
        last_row = int(self.chicken.last_pos[1])
        new_row = int(self.chicken.row)
        max_row = self.grid.row - 1
        min_row = 0
        if new_row > max_row or new_row < min_row:
            self.chicken.is_alive = False
        elif last_row != new_row:
            self.grid.grid[last_row] -= self.chicken
            self.grid.grid[new_row] += self.chicken

    def get_chicken_chunk(self) -> Chunk | int:
        chunk = -1
        if self.chicken.is_alive:
            chunk = self.grid.grid.get(int(self.chicken.row), -1)
            if isinstance(chunk, Chunk) and self.chicken in chunk:
                return chunk
        return -1

    def chicken_is_collide(self, is_center: bool = False) -> bool:
        """Return if the chicken is collide with a entity | if the center of the chicken_lr is on a entity"""
        chunk = self.get_chicken_chunk()
        tile = (self.tile, self.tile)
        if isinstance(chunk, Chunk):
            chicken_rect = self.chicken.resize_lr(tile)
            for e in chunk:
                entity_rect = e.resize_lr(tile)
                if not isinstance(e, Chicken) and chicken_rect.colliderect(entity_rect):
                    if is_center:
                        return entity_rect.collidepoint(chicken_rect.center)
                    return True
        return False

    def prep_world(self):
        gw.generate_world()
        gw.generate_entity()
