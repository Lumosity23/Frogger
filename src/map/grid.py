from math import ceil, floor
from src.utils.log import debug

from pygame.rect import Rect

from src.utils.projection import Projection

from src.map.chunk import Chunk

from src.entities.entity import Entity


class Grid:
    def __init__(self, screen_size: tuple[int, int], tile: float, scale: float = 1.0):
        self.scale: float = scale
        self.col: float = 30
        self.row: float = 30
        self.tile: float = tile
        self.cell_size: int = int(tile * scale)
        self.grid: dict[int, Chunk] = self.make_grid()
        self.tiles:list[list[tuple[float, float]]] = self.make_tiles(self.col, self.row)

    def make_tiles(self, col: float, row: float) -> list[list[tuple[float, float]]]:
        """
        Make a grid of tuple[col, row]
        ```python
        [
            [ tuple(0,0), tuple(1,0), tuple(2,0) ],
            [ tuple(0,1), tuple(1,1), tuple(2,1) ],
            [ tuple(0,2), tuple(1,2), tuple(2,2) ],
        ]
        ```
        where each tuple is a position of a tile --> tuple[col, row]
        """

        return [[(x, y) for x in range(int(col))] for y in range(int(row))]

    def make_grid(self) -> dict[int, Chunk]:
        grid: dict[int, Chunk] = {}
        for i in range(self.row):
            grid[i] = Chunk(i)
        return grid

    # Ceci est une methode temporaire en attendant le systeme de chunk
    def get_visible_rows(self, r: Rect, proj: Projection) -> list[tuple[float, float]]:
        """Return the visible rows"""
        corners = [r.topleft, r.topright, r.bottomleft, r.bottomright]
        rows = [proj.unproject(*corner)[1] for corner in corners]

        min_row = max(0, floor(min(rows)))
        max_row = min(len(self.tiles), ceil(max(rows)))

        return min_row, max_row

    def get_visible_tiles(self, rect: Rect, proj: Projection):
        minr, maxr = self.get_visible_rows(rect, proj)
        return [entity for row in self.tiles[minr:maxr] for entity in row]

    def get_visible_entities(self, rect: Rect, proj: Projection) -> list[Entity]:
        minr, maxr = self.get_visible_rows(rect, proj)
        all_entities = []
        for key in range(minr, maxr):
            chunk = self.grid[key]
            for e in chunk:
                all_entities.append(e)
        return all_entities




    def update(self, dt: float):
        for chunk in self.grid.values():
            chunk.update(dt)



    # Ju si tu sais cree le systeme de chunk ce serai trop bien !
    # aussi modifie `make_tiles` a ta "guise" pour avoir ce que tu veux
