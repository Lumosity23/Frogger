import math
from dataclasses import dataclass


@dataclass
class Projection:
    a: float
    b: float
    c: float
    d: float

    @classmethod
    def deformation(cls, dx: float, dy: float, rot: float, tile: float) -> Projection:
        t = math.radians(rot)
        return cls(
            tile * dx * math.cos(t),
            -tile * dx * math.sin(t),
            tile * dy * math.sin(t),
            tile * dy * math.cos(t),
        )

    @classmethod
    def flat(cls, tile: float) -> Projection:
        """Flat view for debug ( without projection )"""
        return cls(tile, 0, 0, tile)

    @property
    def det(self) -> float:
        """Compute the determinant of the projection"""
        return self.a * self.d - self.b * self.c

    def project(self, col: float, row: float) -> tuple[float, float]:
        """Convert grid position into screen position"""
        return self.a * col + self.b * row, self.c * col + self.d * row

    def unproject(self, sx: float, sy: float) -> tuple[float, float]:
        """Convert screen position into grid position"""
        if abs(self.det) < 1e-12:
            raise ValueError("Projection non inversible : déterminant nul")
        col = (self.d * sx - self.b * sy) / self.det
        row = (-self.c * sx + self.a * sy) / self.det
        return col, row

    def cell_center(self, col: float, row: float) -> tuple[float, float]:
        """Center of the tile on screen"""
        return self.project(col + 0.5, row + 0.5)

    def depth(self, col: float, row: float) -> float:
        """Law of sorting entities on the projection"""
        _, sy = self.cell_center(col, row)
        return sy

    def tile_corners(self, col: int, row: int) -> list[tuple[float, float]]:
        """return the 4 screen_point of a tile ( top / right / bottom / left )"""
        return [
            self.project(col, row),
            self.project(col + 1, row),
            self.project(col + 1, row + 1),
            self.project(col, row + 1),
        ]
