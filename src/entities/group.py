from math import ceil

from src.entities.entity import Entity


class EntityGroup(Entity):
    """Une seule entité logique (rect de lsize). Au rendu, elle est dessinée case par case."""

    def pieces(self) -> list[Entity]:
        cols, rows = ceil(self.lsize[0]), ceil(self.lsize[1])
        return [
            Entity(
                self.col + i,
                self.row + j,
                self.scale,
                img=self.img,
                is_alive=self.is_alive,
                lift_val=self.lift_val,
            )
            for j in range(rows)
            for i in range(cols)
        ]
