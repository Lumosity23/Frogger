from collections.abc import Sequence

import pygame as pg
from pygame.math import Vector2
from pygame.rect import Rect


class Camera:
    def __init__(self, screen_size: tuple[int, int]) -> None:
        self.offset: Vector2 = pg.math.Vector2()
        self.screen_size: tuple[int, int] = screen_size
        self.screen_center: Vector2 = pg.math.Vector2(screen_size) / 2

    @property
    def visible_rect(self) -> Rect:
        return Rect(self.offset.x, self.offset.y, *self.screen_size)

    def follow(self, entity_position: tuple[float, float], dt: float):
        """follow an entity ( eg : chicken )"""
        ideal = Vector2(entity_position) - self.screen_center
        self.offset += (ideal - self.offset) * min(1.0, 8.0 * dt)

    def to_view(
        self, points: Sequence[tuple[float, float]]
    ) -> list[tuple[float, float]]:
        return [(x - self.offset.x, y - self.offset.y) for x, y in points]
