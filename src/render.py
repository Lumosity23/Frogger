import pygame as pg

from src.entities.chicken import Chicken
from src.entities.entity import Entity
from src.utils.camera import Camera
from src.utils.projection import Projection

GRASS_A = (120, 180, 90)
GRASS_B = (105, 165, 80)


def z_sorting(entities: list[Entity], projecter: Projection) -> list[Entity]:
    """Sort entities with a rule"""
    return sorted(entities, key=lambda e: projecter.depth(e.col, e.row))


def draw_grid(
    screen: pg.Surface,
    visible_tiles: list[tuple[float, float]],
    projecter: Projection,
    cam: Camera,
) -> None:
    """Draw on screen the tiles of the grid"""
    for c, r in visible_tiles:
        color = GRASS_A if (c + r) % 2 == 0 else GRASS_B
        # 1 - projection / 2 - offset of the camera / 3 - draw on screen
        _ = pg.draw.polygon(screen, color, cam.to_view(projecter.tile_corners(c, r)))


def draw_entities(
    screen: pg.Surface,
    entities: list[Entity],
    projecter: Projection,
    cam: Camera,
    mode: str = "PROD",
) -> None:
    """Draw on screen the entities"""
    fast_blit = screen.blit
    for e in z_sorting(entities, projecter):
        # 1 - projection / 2 - offset of the camera / 3 - draw on screen
        w, h = e.size
        pos = cam.to_view([projecter.cell_center(*e.gpos)])[0]
        # center the sprite [temporaire] --> devra aller dans la class de l'entity car propre a chacun
        pos = pos[0] - (w / 2), pos[1] - h * 0.9
        _ = fast_blit(e.img, pos)
        # Draw the hitBox of the entity
        if mode == "DEBUG":
            _ = pg.draw.rect(screen, "RED", pg.rect.Rect(pos, e.size), width=1)
