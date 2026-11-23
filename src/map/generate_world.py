import numpy as np

from src.entities.entity import Entity
from src.entities.haybale import HayBale
from src.entities.pig import Pig
from src.map.chunk import Chunk
from src.utils import log

CHUNK_TYPE: dict[
    str, bool
] = {  # à quoi serve les numéros ?? Possible de changer ?? -> juste liste de tuple avec type, True/False ??
    "SAFE": False,
    "ROAD": True,
    "MUD": True,
    "END": True,
}


ENTITY_SET: dict[type[Entity], tuple[int, str]] = {
    Pig: (150, "MUD"),
    HayBale: (150, "ROAD"),
}
MAX_ENTITIES: int = 10


def generate_entity(scale: float) -> dict[str, list[Entity]]:
    """initiate entities"""
    world: dict[str, list[Entity]] = {}
    rng = np.random.default_rng(12345)
    for etype, (n, ctype) in ENTITY_SET.items():
        list_entities: list[Entity] = []
        for _ in range(n):
            lsize = rng.integers(1, 2, 1)[0]
            e = etype(0, 0, scale)
            e.lsize = (lsize, 1)
            list_entities.append(e)
        world[ctype] = list_entities
    return world


def get_chunk_type(rng: np.random.Generator, gs: tuple[int, int]) -> list[str]:
    """Génère les types de chunks (reproductible via le rng) et renvoie une liste
    de exactement `gs[0]` éléments, qui commence et finit par "SAFE".

    Le monde est construit par "bandes" : on choisit un nouveau type différent du
    précédent, puis on décide au hasard de la longueur de la bande.
    """
    n_rows = gs[0]

    # chance (en %) de prolonger une bande qui a déjà `longueur` chunks
    # (indexé par la longueur actuelle ; au-delà du tableau, on prend la dernière valeur)
    extend_chance = [50, 90, 65, 50, 50, 20, 20, 10, 0]

    # types possibles après un type donné (jamais deux bandes consécutives identiques)
    possibilities = {
        "ROAD": ["SAFE", "MUD"],
        "MUD": ["ROAD", "SAFE"],
        "SAFE": ["ROAD", "MUD"],
    }

    world: list[str] = ["SAFE"]
    current = "SAFE"

    while len(world) < n_rows - 1:
        current = str(rng.choice(possibilities[current]))

        length = 1
        while rng.integers(0, 100) < extend_chance[min(length, len(extend_chance) - 1)]:
            length += 1

        # on ne dépasse pas la place restante (il faut garder la dernière ligne pour "SAFE")
        length = min(length, n_rows - 1 - len(world))
        world.extend([current] * length)

    world.append("SAFE")
    return world


def set_type(world: list[str], grid: dict[int, Chunk]):
    """Associate types to chunks"""
    for i, type in enumerate(world):
        chunk = grid[i]
        chunk.type = type
    return grid


def set_padding(rng: np.random.Generator, grid: dict[int, Chunk]):
    for i in range(1, len(grid) - 1):
        c = grid[i]
        if CHUNK_TYPE[c.type]:
            c.padding = rng.integers(3, 6, 1)[0]
    return grid


def set_velocity(rng: np.random.Generator, grid: dict[int, Chunk]) -> dict[int, Chunk]:
    for i in range(1, len(grid) - 1):
        c = grid[i]
        if CHUNK_TYPE[c.type]:
            c.velocity = rng.integers(1, 3, 1)[0]

    return grid


def entity_distribution(
    rng: np.random.Generator, grid: dict[int, Chunk], entities: dict[str, list[Entity]]
):
    for i in range(1, len(grid) - 1):
        c = grid[i]
        if CHUNK_TYPE[c.type]:
            list_entity = entities[c.type]
            while c.logic_size <= MAX_ENTITIES:
                if len(list_entity) <= 1:
                    raise ValueError("ALERT PAS ASSEZ D'ENTITIES !!!!")
                ei = rng.integers(0, len(list_entity) - 1, 1)[0]
                c += list_entity.pop(ei)
    return grid


def get_world(
    rng: np.random.Generator, grid: dict[int, Chunk], entities: dict[str, list[Entity]]
) -> dict[int, Chunk]:
    grid_size = len(grid), grid[0].col
    chunk_type = get_chunk_type(rng, grid_size)
    grid = set_type(chunk_type, grid)
    grid = set_padding(rng, grid)
    grid = set_velocity(rng, grid)
    grid = entity_distribution(rng, grid, entities)
    return grid
