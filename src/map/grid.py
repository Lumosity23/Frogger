from math import ceil, floor

from pygame.rect import Rect

from src.utils.projection import Projection


class Grid:
    def __init__(
        self, screen_size: tuple[int, int], projecter: Projection, scale: float = 1.0
    ):
        self.scale: float = scale
        self.col: float = 30.0
        self.row: float = 30.0
        self.cell_size: int = int(50 * scale)
        self.PROJ: Projection = projecter
        self.grid: list[list[tuple[float, float]]] = self.make_grid(self.col, self.row)

    def make_grid(self, col: float, row: float) -> list[list[tuple[float, float]]]:
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

    # Ceci est une methode temporaire en attendant le systeme de chunk
    def visible_rows(self, r: Rect) -> list[tuple[float, float]]:
        """Return the visible rows"""
        corners = [r.topleft, r.topright, r.bottomleft, r.bottomright]
        rows = [self.PROJ.unproject(*corner)[1] for corner in corners]

        min_row = max(0, floor(min(rows)))
        max_row = min(len(self.grid), ceil(max(rows)))

        return [entity for row in self.grid[min_row:max_row] for entity in row]

    # Ju si tu sais cree le systeme de chunk ce serai trop bien !
    # aussi modifie `make_grid` a ta "guise" pour avoir ce que tu veux
