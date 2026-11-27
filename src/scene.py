import re
from collections.abc import Callable

import numpy as np
import pygame as pg

# import src.map.generate_world as gw
from src.entities.chicken import Chicken
from src.entities.chicken_coop import Chicken_coop
from src.entities.haybale import HayBale
from src.entities.pig import Pig
from src.map.chunk import Chunk
from src.map.grid import Grid
from src.render import *
from src.state import GameState, StateManager
from src.utils import log
from src.utils.camera import Camera

# from entities.entity import Entity
from src.utils.projection import Projection
from src.utils.score import score

MOVES: dict[int, tuple[int, int]] = {
    pg.K_LEFT: (-1, 0),
    pg.K_RIGHT: (1, 0),
    pg.K_UP: (0, -1),
    pg.K_DOWN: (0, 1),
    pg.K_a: (-1, 0),
    pg.K_d: (1, 0),
    pg.K_w: (0, -1),
    pg.K_s: (0, 1),
}

OG_MAP = False


class Scene:
    def __init__(
        self, screen_size: tuple[int, int], state_mgr: StateManager, scale: float = 1.0
    ) -> None:
        # Elements of the game
        self.state_mgr: StateManager = state_mgr
        self.dead_state: str = "GAME OVER"
        self.tile: int = int(50 * scale)
        self.grid_size: tuple[int, int] = (15, 5)
        self.col, self.row = self.grid_size
        self.mode: str = "PROD"
        self.score: score = score("src/score.jsonc")
        self.max_lives: int = 5
        self.lives: int = self.max_lives
        self.timer: float = 120.0
        self.time: float = self.timer
        self.input: list[tuple[int, int]] = []

        self.chicken_actions: dict[str, Callable[[], None]] = {
            "END": self.back_chicken_coop,
            "SAFE": self.chill,
            "MUD": self.on_mud,  # changer en "MUD" --> doooone
            "ROAD": self.on_road,
        }

        self.last_chunk_type: str = "SAFE"
        self.seed: int = self.get_seed()
        self.rng = np.random.default_rng(
            self.seed
        )  # Est-ce correct ? OUI OMG ça fonctionne #émue -> pas bon endroit pour rng ??
        # Si si, c'est super ! on changera la place de plein de choses quand on aura la boucle de jeu complete

        # Rendering Object
        self.FLAT: Projection = Projection.flat(self.tile)
        self.DEFO: Projection = Projection.deformation(1.1, 0.7, 15, self.tile)
        self.proj: Projection = self.DEFO
        self.cam: Camera = Camera(screen_size)

        # Prepare the world
        self.grid: Grid = Grid(self.grid_size, self.tile, scale)
        self.grid.generate_world(self.rng)
        # col, row = self.proj.unproject(screen_size[0] / 2, screen_size[1] / 2)
        self.chicken: Chicken = Chicken(round(self.grid_size[0] / 2), 1, scale)
        # self.grid.grid[0] += self.chicken
        # self.haybale: HayBale = HayBale(round(col - 10), round(row), scale)
        # self.pig: Pig = Pig(round(col - 10), round(row), scale)  ATTENTION maintenant PIG == MUD

        # Subscribtion
        self.state_mgr.subscribe(self.on_state_change)

        # Test
        # self.grid.grid[18] += self.haybale
        self.spawn_chicken()
        # elf.grid.grid[13] += self.pig

        # OG MAP
        if OG_MAP:
            self.grid.grid[29].type = "SAFE"
            row = self.grid_size[1]
            for i in range(row - 2, row // 2, -1):
                self.grid.grid[i].type = "ROAD"
            self.grid.grid[row // 2].type = "SAFE"
            for i in range(row // 2 - 1, 0, -1):
                self.grid.grid[i].type = "MUD"
            self.grid.grid[0].type = "END"

        sixieme = int(self.col/6)

        self.grid.grid[0].type = "END"
        for e in range(5): # 5 poulaillers
            entity = Chicken_coop(0,0,scale)
            entity.col = sixieme + (sixieme * e)
            self.grid.grid[0] +=  entity


    @property
    def tile_size(self) -> tuple[int, int]:
        return self.tile, self.tile

    def reset_game(self) -> None:
        self.lives = self.max_lives
        self.time = self.timer
        self.seed = self.get_seed()
        self.rng = np.random.default_rng(self.seed)
        if not OG_MAP:
            self.grid.generate_world(self.rng)
            self.spawn_chicken()
        self.score = score("src/score.jsonc")
        self.chicken.is_alive = True
        self.respawn_chicken(True)

    def on_state_change(self, new_state: GameState, old_state: GameState) -> None:
        if new_state == GameState.MENU and (
            old_state == GameState.GAME_OVER
            or old_state == GameState.PAUSE
            or old_state == GameState.LEADERBOARD
        ):
            self.reset_game()
        elif new_state == GameState.GAME_OVER:
            self.respawn_chicken()
            self.lives = int(self.max_lives)
            self.time = float(self.timer)

        elif new_state == GameState.PLAY and old_state == GameState.GAME_OVER:
            self.reset_game()

    def prep_world(self):
        # gw.generate_world()
        # gw.generate_entity()
        pass

    def update(self, dt: float):
        if self.state_mgr.current != GameState.PAUSE:
            self.grid.update(dt)
            self.cam.follow(self.proj.cell_center(*self.chicken.gpos), dt)
        if self.is_game_over():
            self.state_mgr.set(GameState.GAME_OVER)
            return
        if self.state_mgr.current == GameState.PLAY:
            self.time -= dt
            if self.chicken.is_alive:
                self.chicken_update(dt)
            else:
                self.respawn_chicken()

    def handle_events(self, event: pg.Event) -> bool:
        if event.type == pg.KEYDOWN:
            if event.key in MOVES:
                self.input.append(MOVES[event.key])
            if event.key == pg.K_p:
                if self.proj == self.DEFO:
                    self.proj = self.FLAT
                    self.mode = "DEBUG"
                    log.debug("PROJ -> FLAT")
                else:
                    self.proj = self.DEFO
                    self.mode = "PROD"
                    log.debug("PROJ -> DEFORMATION")

        return False

    def draw(self, screen: pg.Surface) -> None:
        visible_tiles = self.grid.get_visible_tiles(self.cam.visible_rect, self.proj)
        all_entities = self.grid.get_visible_entities(self.cam.visible_rect, self.proj)
        draw_grid(screen, visible_tiles, self.proj, self.cam)
        draw_entities(screen, all_entities, self.proj, self.cam, self.tile, self.mode)

    def is_game_over(self) -> bool:
        time_left = self.time <= 0
        lives_left = self.lives <= 0
        state = time_left or lives_left
        if state:
            if lives_left:
                self.dead_state = "No more lives !"
            elif time_left:
                self.dead_state = "No more time !"
            return True
        elif self.is_win():
            self.dead_state = ""
        return False

    def update_chicken_chunk(self):
        last_row = int(self.chicken.last_pos[1])
        new_row = int(self.chicken.row)
        max_row = self.grid.row - 1
        min_row = 0
        if new_row > max_row or new_row < min_row:
            self.chicken.is_alive = False
        elif last_row != new_row:
            self.grid.grid[last_row] -= self.chicken
            self.grid.grid[new_row] += self.chicken
            self.last_chunk_type = self.grid.grid[last_row].type

    def get_chicken_chunk(self) -> Chunk | None:
        chunk = None
        if self.chicken.is_alive:
            chunk = self.grid.grid.get(int(self.chicken.row))
            if isinstance(chunk, Chunk) and self.chicken in chunk:
                return chunk
        return chunk

    def chicken_is_collide(
        self, chunk: Chunk, is_center: bool = False
    ) -> tuple[bool, Entity | None]:
        """Return if the chicken is collide with a entity | if the center of the chicken_lr is on a entity"""
        if len(chunk) == 1:
            return False, None
        chicken_rect = self.chicken.resize_lr(self.tile_size)
        for e in chunk:
            entity_rect = e.resize_lr(self.tile_size)
            if e != self.chicken and chicken_rect.colliderect(entity_rect):
                if is_center:
                    return (entity_rect.collidepoint(chicken_rect.center), e)
                return (True, e)
        return (False, None)

    def chicken_update(self, dt: float):
        if self.input:
            move = self.input.pop(0)
            if self.chicken.move(*move):
                self.score.update("FOWARD", -move[1])
            else:
                pass  # self.input.insert(0, move)  # buffer for smoother input
            self.update_chicken_chunk()
        chunk = self.get_chicken_chunk()
        if chunk:
            _ = self.chicken_actions.get(chunk.type, self.chill)(chunk)

    def respawn_chicken(self, is_winning: bool = False):
        self.score.next_round()
        self.input.clear()
        self.lives -= 1 if not is_winning else 0
        self.chicken.is_movable = False
        self.chicken.is_alive = True
        self.chicken.row = len(self.grid.grid) - 1
        self.chicken.col = len(self.grid.grid[0].tiles) // 2
        self.update_chicken_chunk()

    def spawn_chicken(self):
        self.grid.grid[len(self.grid.grid) - 1] += self.chicken

    def snap_chicken(self, e: Entity | float, not_pos: bool = True):
        if not_pos:
            for entity in e.pieces():
                er = entity.resize_lr(self.tile_size)
                cr = self.chicken.resize_lr(self.tile_size)
                if er.collidepoint(cr.center):
                    self.chicken.col = entity.col
        else:
            self.chicken.col = e

    def nearest_tile(self, chunk: Chunk) -> int:
        for c, r in chunk.tiles:
            rect_tile = pg.Rect(c * self.tile, r * self.tile, *self.tile_size)
            cr = self.chicken.resize_lr(self.tile_size)
            if rect_tile.collidepoint(cr.center):
                return c
        return self.chicken.col

    def back_chicken_coop(self, chunk: Chunk):
        is_collide, e = self.chicken_is_collide(chunk, True)
        if chunk.type == "END" and is_collide and not e.is_occupied:
            self.score.update("CHICKEN_SAVE")
            self.respawn_chicken(True)
            e.is_occupied = True
        else:
            self.respawn_chicken()

    def chill(self, chunk: Chunk):
        if self.last_chunk_type == "MUD":
            self.chicken.is_movable = False
            self.snap_chicken(self.nearest_tile(chunk), False)

    def on_mud(self, chunk: Chunk):
        is_collide, e = self.chicken_is_collide(chunk, True)
        if chunk.type == "MUD" and is_collide:
            self.chicken.is_movable = True
            self.snap_chicken(e)
        else:
            self.respawn_chicken()

    def on_road(self, chunk: Chunk):
        if self.last_chunk_type == "MUD":
            self.chicken.is_movable = False
            self.snap_chicken(self.nearest_tile(chunk), False)
        is_collide, e = self.chicken_is_collide(chunk)
        if is_collide:
            self.respawn_chicken()

    def is_win(self) -> bool:
        """Check if all chicken coop is occupied ( Not a very reliable method... )"""
        all_occupied = 0
        end_chunk = self.grid.grid[0]
        size = len(end_chunk)
        if size <= 1:
            return False
        for e in end_chunk:
            if hasattr(e, "occupied"):
                all_occupied += 1
        return all_occupied == (size - 1)


    def get_seed(self) -> int:
        seed: str = ""
        numbers = np.random.default_rng().integers(1, 10, 5)
        for n in numbers:
            seed += str(n)
        return int(seed)


