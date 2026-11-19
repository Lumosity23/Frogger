from dataclasses import dataclass

from src.entities.chicken import Chicken
from src.entities.entity import Entity


@dataclass
class Chunk:
    row: int
    col: int
    padding: float = 3.0
    velocity: float = 1.0
    direction: int = -1
    type: str = "SAFE"

    @property
    def logic_size(self) -> int:
        return sum([int(e.lsize[0]) for e in self.entities])

    def __post_init__(self):
        self.entities: list[Entity] = []
        self.tiles: list[tuple[int, int]] = [(c, self.row) for c in range(self.col)]

    def update(self, dt: float):
        step: float = dt * self.velocity * self.direction

        for i, e in enumerate(self.entities):
            if e.is_alive:
                if e.is_movable:
                    e.col += step
                e.update(dt)
                if (self.direction > 0 and e.col >= self.col) or (
                    self.direction < 0
                    and e.col < -e.lsize[0]
                    or (isinstance(e, Chicken) and e.col >= self.col)
                ):
                    e.is_alive = False
            else:
                self.respawn_entity(e, i)

    def respawn_entity(self, e: Entity, i: int):
        if isinstance(e, Chicken):
            return
        if len(self.entities) <= 1:
            e.is_alive = True
            e.col = -e.lsize[0] if self.direction > 0 else self.col
            return

        next_entity = self.entities[(i + 1) % len(self.entities)]

        if not next_entity.is_alive:
            return

        if self.direction > 0:
            # Spawn à gauche (-e.lsize[0]) : distance jusqu'au bord gauche de next_entity
            distance = next_entity.col - (-e.lsize[0])
            spawn_col = -e.lsize[0]
        else:
            # Spawn à droite (self.col) : distance jusqu'au bord droit de next_entity
            next_right = next_entity.col + next_entity.lsize[0]
            distance = self.col - next_right
            spawn_col = self.col

        if distance >= self.padding:
            e.is_alive = True
            e.col = spawn_col

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

    def __len__(self) -> int:
        return len(self.entities)
