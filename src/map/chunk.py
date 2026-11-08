from dataclasses import dataclass

from src.entities.entity import Entity


@dataclass
class Chunk:
    row: int
    velocity: float = 0.0
    direction: int = 1
    type: str = "SAFE"

    def __post_init__(self):
        self.entities: list[Entity] = []

    def update(self, dt: float):
        step: float = dt * self.velocity * self.direction
        for e in self.entities:
            e.col += step
            e.update(dt)

    def __getitem__(self, index):  # chunk[i]
        return self.entities[index]

    def __iadd__(self, entity: Entity) -> Chunk:  # chunk += entity
        entity.row = self.row
        self.entities.append(entity)
        return self  # c'est cette ligne qui manquais pour bien faire fonctionner __iadd__ !

    def append(self, entity: Entity):
        entity.row = self.row
        self.entities.append(entity)
