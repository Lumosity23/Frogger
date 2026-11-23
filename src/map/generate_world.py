#

import numpy as np

from src.entities.entity import Entity
from src.entities.haybale import HayBale
from src.entities.pig import Pig
from src.map.chunk import Chunk
from src.scene import Scene
from src.map.grid import Grid

CHUNK_TYPE: dict[str, tuple[int, bool]] = { # à quoi serve les numéros ?? Possible de changer ?? -> juste liste de tuple avec type, True/False ??
    "SAFE": False,
    "ROAD": True,
    "MUD": True,
    "END": True,
}

ENTITY_SET: dict[type[Entity], int] = {Pig: 50, HayBale: 50}


def generate_entity(scale: float) -> list[list[Entity]]:
    """initiate entities"""
    world: list[list[Entity]] = []
    rng = np.random.default_rng(12345)
    for entity_type in ENTITY_SET:
        list_entities: list[Entity] = []
        for _ in range(ENTITY_SET[entity_type].value):
            lsize = rng.integers(1, 5, 1)
            e = entity_type(0, 0, scale)
            e.lsize = (lsize, 1)
            list_entities.append(e)
        world.append(list_entities)
    return world

def get_chunk_type(rng, chunk_type: str, gs) -> list[str]:
    """initiate chunk type and return in list (with seed)"""
    diffwei = [50, 90, 65, 50, 50, 20, 20, 10, 0] # Facteur pour augmenter les chances d'avoir plus 1 fois le même type de chunk
    act_field = "END"
    possibilities = {
    "ROAD": ["SAFE", "MUD"],
    "MUD": ["ROAD", "SAFE"],
    "SAFE": ["ROAD", "MUD"],
    "END": ["ROAD", "MUD"]
    }
    world = []

    while len(world) <= gs[1] - 1:
        # print(f"{same_field} {act_field}")
        res = rng.rng[n].integers(1, 50) + wei #comment appeler "res" pour plus explicite ?
        act_field = #res du random ?? ou pas bsn de def ici car fait ligne 63
    while len(world) <= scene.grid_size[1] - 1: # -1 car d'office "SAFE" en fin de liste (début de map)
        # print(f"{same_field} {act_field}")
        res = rng.integers(1, 50) + wei #comment appeler "res" pour plus explicite ?
        if res > 50:
            same_field += 1
            wei += diffwei[same_field] # same_field "+1" ?
        if res <= 50:
            for field in range(same_field): world.append(act_field)
            same_field = 1
            act_field = rng.rng[n].choice(possibilities[act_field])

            n += 2
            wei = 50
    world.append("SAFE")
    return world


            act_field = rng.choice(possibilities[act_field])

            wei = 50
    world.append("SAFE")
    return world

def generate_world(world: list[str], grid: Grid) -> list[tuple[str, bool]]: # tuple du type et true/false pour les entités
    """Associate types to chunks"""
    for i, type in enumerate(world):
        chunk = grid.grid[i]
        chunk.type = type


def entity_distribution(chunk_type, generate_entity()) -> :#?? :
    if chunk_type.value is True
        pass


def get_world(rng, grid, entities):
    pass

def set_padding(rng, grid):
    for c in len(): #chaque chunk
        _ = np.random.integers(2, 6, 1)


def entity_distribution(rng, grid, e: Entity):
    for c in grid:
        if CHUNK_TYPE.value is True:
            if CHUNK_TYPE == "MUD":
                e == Pig

            elif CHUNK_TYPE == "ROAD":
                e == HayBale

            else: print("what is that")





#if __name__ == "__main__":
