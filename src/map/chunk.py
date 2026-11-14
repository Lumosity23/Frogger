from dataclasses import dataclass

from src.entities.entity import Entity


@dataclass
class Chunk:
    row: int
    velocity: float = 0.0
    direction: int = 1
    type: str = "SAFE"

    @property
    def logic_size(self) -> int:
        return sum([int(e.lsize[0]) for e in self.entities])

    def __post_init__(self):
        self.entities: list[Entity] = []

    def update(self, dt: float):
        step: float = dt * self.velocity * self.direction
        for e in self.entities:
            e.col += step
            e.update(dt)

    def __getitem__(self, index: int) -> Entity:  # chunk[i]
        return self.entities[index]

    def __iadd__(self, entity: Entity) -> Chunk:  # chunk += entity
        entity.row = self.row
        entity.last_pos = entity.col, self.row
        self.entities.append(entity)
        return self  # c'est cette ligne qui manquais pour bien faire fonctionner __iadd__ ! OMG

    def __isub__(self, entity: Entity) -> Chunk:
        self.entities.remove(entity)
        return self

    def append(self, entity: Entity):
        entity.row = self.row
        self.entities.append(entity)
