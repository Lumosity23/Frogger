import math

import pygame as pg

# --- Paramètres identiques à ta classe Grid ---
DX = 1.1  # facteur de distorsion horizontal
DY = 0.7  # facteur de distorsion vertical
ROT = 15.0  # rotation en degrés
CELL_SIZE = 50  # taille d'une case (px)
COLS = 1
ROWS = 1
COLOR_LINE = (244, 244, 244)
MARGIN = 10  # marge autour de la grille (px)
OUTPUT = "grille_export.png"


def make_grid(col: int, row: int, cell_size: int):
    """Même logique que Grid.make_grid : lignes centrées sur l'origine."""
    lines = []
    grid_w = col * cell_size
    grid_h = row * cell_size

    for i in range(col + 1):
        x = cell_size * i - grid_w / 2
        lines.append(((x, -grid_h / 2), (x, grid_h / 2)))

    for i in range(row + 1):
        y = cell_size * i - grid_h / 2
        lines.append(((-grid_w / 2, y), (grid_w / 2, y)))

    return lines


def transform(point, theta: float, dx: float, dy: float):
    """Rotation puis distorsion, dans le même ordre que Grid.rotate_grid."""
    x, y = point
    rx = x * math.cos(theta) - y * math.sin(theta)
    ry = x * math.sin(theta) + y * math.cos(theta)
    return rx * dx, ry * dy


def main():
    theta = math.radians(ROT)

    lines = [
        (transform(p1, theta, DX, DY), transform(p2, theta, DX, DY))
        for p1, p2 in make_grid(COLS, ROWS, CELL_SIZE)
    ]

    # Calcule les limites pour dimensionner l'image
    xs = [p[0] for line in lines for p in line]
    ys = [p[1] for line in lines for p in line]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    width = int(math.ceil(max_x - min_x)) + 2 * MARGIN
    height = int(math.ceil(max_y - min_y)) + 2 * MARGIN
    offset_x = -min_x + MARGIN
    offset_y = -min_y + MARGIN

    surface = pg.Surface((width, height), pg.SRCALPHA)
    surface.fill((0, 0, 0, 0))  # fond transparent

    for p1, p2 in lines:
        start = (round(p1[0] + offset_x), round(p1[1] + offset_y))
        end = (round(p2[0] + offset_x), round(p2[1] + offset_y))
        pg.draw.line(surface, COLOR_LINE, start, end, 1)

    pg.image.save(surface, OUTPUT)
    print(f"Grille sauvegardée : {OUTPUT} ({width}x{height} px)")


if __name__ == "__main__":
    main()
