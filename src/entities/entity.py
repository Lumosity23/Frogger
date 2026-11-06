from dataclasses import dataclass

import pygame as pg


@dataclass
class Entity:
    col: float
    row: float
    scale: float
    img: pg.Surface | None = None
    is_alive: bool = False
    duration: float = 1
    clock: float = 0.0

    @property
    def gpos(self) -> tuple[float, float]:
        return (self.col, self.row)

    @property
    def lift(self) -> float:
        return 0.0

    @property
    def size(self) -> tuple[int, int]:
        return self.img.get_size()

    def update(self, dt: float):
        if getattr(self, "imgs") is not None:
            self.update_anim(dt)

    def get_anim(self, n:int, path:str, scale:float) -> dict[int, pg.Surface]:
        slice_img = {}
        image = pg.image.load(path).convert_alpha()
        image = pg.transform.scale(image, pg.math.Vector2(image.get_size()) * scale)
        w = image.width/n
        h = image.height
        for x in range(n):
            slice = image.subsurface(pg.Rect(x*w, 0, w, h))
            slice_img[x] = slice
            
        return slice_img

    def update_anim(self, dt):
        n:float = len(self.imgs)
        step: float = self.duration / n
        self.clock += dt
        key: int = int(self.clock // step)
        if key > n: 
            self.clock = 0.0
            key = 1
        self.img = self.imgs[max(0, key-1)].copy()


        
        
