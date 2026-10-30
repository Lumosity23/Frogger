TILE_W = 100  # largeur d'une case à l'écran (px)
TILE_H = 50  # hauteur d'une case à l'écran (px), TILE_W / 2 pour une iso 2:1


def cell_to_screen(col: float, row: float) -> tuple[float, float]:
    """Position écran du centre-bas d'une case logique."""
    sx = (col - row) * TILE_W / 2
    sy = (col + row) * TILE_H / 2
    return sx, sy


def screen_to_cell(sx: float, sy: float) -> tuple[float, float]:
    """Inverse : utile pour le clic souris ou le debug."""
    a = TILE_W / 2
    b = TILE_H / 2
    col = (sx / a + sy / b) / 2
    row = (sy / b - sx / a) / 2
    return col, row
