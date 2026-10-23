import copy
from math import pi

import pygame as pg

from src.utils.vector2 import Vector2

##########################################################################################
# Utilisation des effet de distortion sur la grille                       | Arr == Arrow |
# - "o" / "p" -> pour faire tourne la grille sur elle meme                ################
# - ArrUP / ArrDOWN -> etire la grille verticalement                                     #
# - ArrLEFT / ArrRIGHT -> etire la grille horizontalement                                #
##########################################################################################


class Grid:
    def __init__(self, screen_size: tuple[int, int], mode: str = "DEBUG"):
        self.mode: str = mode
        self.screen_size: tuple[int, int] = screen_size
        self.cell_size: int = 50
        self.color_line: tuple[int, int, int] = (244, 244, 244)
        self.grid: list[tuple[Vector2, Vector2]] = []
        self.new_grid: list[tuple[Vector2, Vector2]] = self.make_grid(
            30, 30, self.cell_size
        )
        # Facteur de distortion
        # Les valeurs par default sont celle qui se rapproche le plus de crossy road
        self.dx: float = 1.1
        self.dy: float = 0.7
        self.rot: float = 15.0
        self.theta: float = pi / 180 * self.rot

    def on_draw(self, screen: pg.Surface):
        """Draw the grid on the screen"""
        for p1, p2 in self.grid:
            _ = pg.draw.line(
                screen,
                self.color_line,
                p1.pos_for_screen(self.screen_size),
                p2.pos_for_screen(self.screen_size),
            )

    def on_events(self):
        """Handle the events for the modifications of the grid"""
        if self.mode == "DEBUG":
            keys = pg.key.get_pressed()
            if keys[pg.K_RIGHT]:
                self.dx += 0.1
                return True
            if keys[pg.K_LEFT]:
                self.dx -= 0.1
                return True
            if keys[pg.K_UP]:
                self.dy += 0.1
                return True
            if keys[pg.K_DOWN]:
                self.dy -= 0.1
                return True
            if keys[pg.K_o]:
                self.rot -= 0.4
                self.update_theta()
                return True
            if keys[pg.K_p]:
                self.rot += 0.4
                self.update_theta()
                return True

    def on_update(self) -> None:
        """Update the shape of the grid"""
        self.grid = self.rotate_grid(copy.deepcopy(self.new_grid), self.theta)

    def rotate_grid(
        self, grid: list[tuple[Vector2, Vector2]], th: float
    ) -> list[tuple[Vector2, Vector2]]:
        """Rotate every point of the grid"""
        for point in grid:
            for p in point:
                p.rotate(th)
                p.x *= self.dx
                p.y *= self.dy
        return grid

    def make_grid(
        self, col: int, row: int, cell_size: int
    ) -> list[tuple[Vector2, Vector2]]:
        """Return the new grid"""
        grid: list[tuple[Vector2, Vector2]] = []
        grid_w = col * cell_size
        grid_h = row * cell_size

        for i in range(col + 1):
            x = cell_size * i - grid_w / 2
            grid.append((Vector2(x, 0 - grid_h / 2), Vector2(x, grid_h / 2)))

        for i in range(row + 1):
            y = cell_size * i - grid_h / 2
            grid.append((Vector2(-grid_w / 2, y), Vector2(grid_w / 2, y)))

        return grid

    def update_theta(self):
        """Update the angle of ratation for the grid"""
        self.theta = pi / 180 * self.rot

    def on_finish(self):
        """Send the value of Distortion ofr the grid"""
        return f"Gird : | DefX : {self.dx} | DefY : {self.dy} | THETA : {self.theta * 180 / pi} |"
