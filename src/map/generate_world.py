# Atribution des types de chunks (background) + dispatcher
# Distribution des entitées dans les chunks
# Distribution des types de chunksvd    √

# SAFE type qui accept que chicken  √
# move uptade pas vitesse chicken
# entities avec lsize -> varie entre 1 et 10 000 ( et plus encore.... )
# condition de passage, nb entities déjà présente dans chunk --> logic_size

import numpy as np

from src.entities.entity import Entity
from src.entities.haybale import HayBale
from src.entities.pig import Pig
from src.map.chunk import Chunk
from src.scene import Scene
from src.map.grid import Grid

chunk_type: dict[str, tuple[int, bool]] = { # à quoi serve les numéros ?? Possible de changer ?? -> juste liste de tuple avec type, True/False ??
    "SAFE": (5, False),
    "ROAD": (6, True),
    "MUD": (8, True),
    "END": (1, True),
}

entity_set: dict[type[Entity], int] = {Pig: 30, HayBale: 30}


def generate_entity(
    entity_set: dict[type[Entity], int], scale: float
) -> list[list[Entity]]:
    """initiate entities"""
    world: list[list[Entity]] = []
    for entity_type in entity_set:
        list_entities: list[Entity] = []
        for _ in range(entity_set[entity_type].value):
            _ = np.random.default_rng(Scene.rng).integers(1, 5, 1)  # A faire !
            list_entities.append(entity_type(0, 0, scale))
        world.append(list_entities)
    return world

def get_chunk_type(Scene: Scene, chunk_type: str) -> list[str]:
    """initiate chunk type and return in list (with seed)"""
    diffwei = [50, 90, 65, 50, 50, 20, 20, 10, 0] # Facteur pour augmenter les chances d'avoir plus 1 fois le même type de chunk
    n = 1
    act_field = chunk_type[1]
    possibilities = {
    "ROAD": ["SAFE", "MUD"],
    "MUD": ["ROAD", "SAFE"],
    "SAFE": ["ROAD", "MUD"]
    }
    world = ["END"] #liste commence avec le END de la fin, coordonné y depuis haut écran --> correct ?

    while len(world) <= Scene.grid_size[1] - 1:
        # print(f"{same_field} {act_field}")
        res = Scene.rng[n].integers(1, 50) + wei #comment appeler "res" pour plus explicite ? 
        act_field = #res du random ?? ou pas bsn de def ici car fait ligne 63
        if res > 50:
            same_field += 1
            wei += diffwei[same_field] # same_field "+1" ? 
        if res <= 50:
            for field in range(same_field): world.append(act_field)
            same_field = 1
            act_field = Scene.rng[n].choice(possibilities[act_field]) 
        
            n += 2
            wei = 50
    world.append("SAFE")
    return world
                
 

def generate_world(world: list[str], grid: Grid) -> list[tuple[str, bool]]: # tuple du type et true/false pour les entités
    """Associate types to chunks"""
    for i, type in enumerate(world):
        chunk = grid.grid[i]
        chunk.type = type
    
    


def entity_distribution(chunk_type, generate_entity()) -> #?? :
    if chunk_type.value is True
        for 
    

#if __name__ == "__main__":
     