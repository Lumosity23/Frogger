from typing import TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from src.map.grid import Grid


def add_danger_line(tiles: list[list[tuple[int, int]]]) -> list[list[tuple[int, int]]]:
    for line in tiles:
        row = line[0][1]
        line.insert(0, (-1, row))
        line.append((len(line), row))
