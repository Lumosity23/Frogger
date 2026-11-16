# Atribution des types de chunks (background) + dispatcher
# Distribution des entitées dans les chunks
# Distribution des tupes de chunks

# SAFE type sui accept que chicken
# move uptade pas vitesse chicken
# entities avec lsize -> varie entre 1 et 10 000 ( et plus encore.... )
# condition de passage, nb entities déjà présente dans chunk --> logic_size

import numpy as np

from src.scene import Scene
from src.entities.entity import Entity
from src.entities.haybale import HayBale
from src.entities.pig import Pig
from src.map.chunk import Chunk


chunk_type: dict[str, tuple[int, bool]] = {
    "SAFE": (5, False),
    "ROAD": (6, True),
    "PIG": (8, True),
    "END": (1,False)
}

entity_set: dict[Entity.__class__, int] = {
    Pig: 30,
    HayBale: 30
}

def generate_entity(entity_set, scale)-> list[list[Entity]]:
    """initiate entities"""
    world :list = []
    for entity_type in entity_set:
        list_entities :list = []
        for _ in range(entity_set[entity_type].value):
            list_entities.append(entity_type(0, 0, scale))
        world.append(list_entities)
    return world        

def get_chunk_type(Scene, chunk_type) -> list[dict[str, int]]:
    max_rows :int = int(Scene.grid_size[1] - 2)
    rows :int = max_rows
    section :dict[str, int]
    map :list[dict[str, int]]
    
    for r in rows:
        if rows + 3 >= max_rows:
            return map
        else:
            block = [rng.choice(chunk_type), rng.choice(rows)]
        rows -= rows - ussed_row
        #section + chunk SAFE ???
        map.append(section)

        chunk_type[Scene.rng.integers(0, 2)]

#str(rng.choice(chunk_type))
# section = block + chunk SAFE
# block = seed type chunk + seed nb lignes


def generate_world(chunk_type, seed) -> tuple[int, list[list[Chunk]]] :
    """initiate chunk with type and return with seed"""
    first = np.random.default_rng(seed).integers(0, 1, grid_size)




#def entity_distribution(chunk_type):
