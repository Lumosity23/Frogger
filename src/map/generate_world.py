# Atribution des types de chunks (background) + dispatcher
# Distribution des entitées dans les chunks
# Distribution des tupes de chunks

# SAFE type sui accept que chicken
# move uptade pas vitesse chicken
# entities avec lsize -> varie entre 1 et 10 000
# condition de passage, nb entities déjà présente dans chunk --> logic_size

import numpy as np

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
    Pig: 10,
    HayBale: 12
}

def generate_entity(entity_set, scale)-> list[list[Entity]]:
    """initiate entities"""
    world :list = []
    for entity_type in entity_set:
        list_entities : list = []
        for _ in range(entity_set[entity_type].value):
            list_entities.append(entity_type(0, 0, scale))
        world.append(list_entities)
    return world        

def get_chunk_type(chunk_type, grid_size) -> list[dict[str, int]]:


def generate_world(chunk_type, seed) -> tuple[int, list[list[Chunk]]] :
    """initiate chunk with type and return with seed"""
    first = np.random.default_rng(seed).integers(0, 1, grid_size)


def get_seed() -> int:
    seed: str = ""
    numbers = np.random.default_rng().integers(1, 10, 5)
    for n in numbers: seed += str(n)
    return int(seed)



def entity_distribution(chunk_type):
