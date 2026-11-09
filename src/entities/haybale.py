import os 
from dataclasses import dataclass

from src.entities.entity import Entity
#from map.chunk import Chunk

ASSETS = f"{os.path.abspath(".")}\\assets\\"
PATH = f"{ASSETS}hay_bale_anim.png"

class HayBale(Entity):
    def __init__(self, col, row, scale):
        super().__init__(col, row, scale)
        self.duration = 0.7
        self.is_alive = True
        self.imgs = self.get_anim(8, PATH, scale)
        

