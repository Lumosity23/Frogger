from math import ceil, floor

# from numpy import random
from pygame.rect import Rect

from src.entities.entity import Entity
from src.map.chunk import Chunk

# from src.utils.log import debug
from src.utils.projection import Projection


class Grid:
    def __init__(self, grid_size: tuple[int, int], tile: float, scale: float = 1.0):
        self.scale: float = scale
        self.col: int = grid_size[0]
        self.row: int = grid_size[1]
        self.tile: float = tile
        self.cell_size: int = int(tile * scale)
        self.grid: dict[int, Chunk] = self.make_grid()

    def make_grid(self) -> dict[int, Chunk]:
        grid: dict[int, Chunk] = {}
        for i in range(self.row):
            grid[i] = Chunk(i, self.col)
        return grid

    # Ceci est une methode temporaire en attendant le systeme de chunk
    def get_visible_rows(self, r: Rect, proj: Projection) -> tuple[int, int]:
        """Return the visible rows"""
        corners = [r.topleft, r.topright, r.bottomleft, r.bottomright]
        rows = [proj.unproject(*corner)[1] for corner in corners]

        min_row = max(0, floor(min(rows)))
        max_row = min(self.row, ceil(max(rows)))

        return min_row, max_row

    def get_visible_tiles(self, rect: Rect, proj: Projection):
        minr, maxr = self.get_visible_rows(rect, proj)
        tiles: list[tuple[str, list[tuple[int, int]]]] = []
        for row in range(minr, maxr):
            c = self.grid[row]
            tiles.append((c.type, c.tiles))
        return tiles

    def get_visible_entities(self, rect: Rect, proj: Projection) -> list[Entity]:
        minr, maxr = self.get_visible_rows(rect, proj)
        all_entities: list[Entity] = []
        for key in range(minr, maxr):
            chunk = self.grid[key]
            for e in chunk:
                all_entities.append(e)
        return all_entities

    # def type de monde -> dans generate_word.py

    def update(self, dt: float):
        for chunk in self.grid.values():
            chunk.update(dt)
