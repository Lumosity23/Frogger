from dataclasses import dataclass

import pygame as pg


@dataclass
class Entity:
    col: float
    row: float
    scale: float
    img: pg.Surface | None = None
    is_movable: bool = True
    is_alive: bool = False
    duration: float = 1
    clock: float = 0.0
    lift_val: float = 0.0
    lsize: tuple[float, float] = (1.0, 1.0)
    direction: int = 1

    def __post_init__(self):
        self.last_pos: tuple[float, float] = self.col, self.row

    @property
    def gpos(self) -> tuple[float, float]:
        return (self.col, self.row)

    @property
    def lift(self) -> float:
        return self.lift_val

    @property
    def size(self) -> tuple[int, int]:
        return self.img.get_size()

    @property
    def logic_rect(self) -> tuple[float, float, float, float]:
        return (self.col, self.row, *self.lsize)

    def resize_lr(self, point: tuple[float, float]) -> pg.Rect:
        """Resize the logic rect with a Point"""
        x, y = point
        size = self.lsize[0] * x, self.lsize[1] * y
        return pg.Rect(self.col * x, self.row * y, *size)

    def pieces(self) -> list["Entity"]:
        """Ce qui est dessiné pour cette entité (surchargé par les groupes)"""
        return [self]

    def update(self, dt: float):
        if getattr(self, "imgs", None) is not None:
            self.update_anim(dt)

    def get_anim(
        self, n: int, path: str, scale: float, reverse: bool = False
    ) -> dict[int, pg.Surface]:
        image = pg.image.load(path).convert_alpha()
        image = pg.transform.scale(image, pg.math.Vector2(image.get_size()) * scale)
        w = image.width // n
        h = image.height
        d = image.width - w if reverse else 0
        return {
            x: image.subsurface(pg.Rect(abs(d - (x * w)), 0, w, h)).copy()
            for x in range(n)
        }

    def update_anim(self, dt: float):
        n: float = len(self.imgs)
        step: float = self.duration / n
        self.clock += dt
        key: int = int(self.clock // step)
        if key > n:
            self.clock = 0.0
            key = 1
        self.img = self.imgs[max(0, key - 1)].copy()
