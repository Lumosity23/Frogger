import os

import pygame as pg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_PROJECT = os.path.abspath(os.path.join(HERE, "..", ".."))
ASSETS = os.path.join(ROOT_PROJECT, "assets")
RESOLUTION = 6  # 4 px ecran = 1 px image

DARKER = -25
SHADOW = -45


def get_theme(
    rect: pg.Rect, color: tuple[int, int, int], text: str
) -> dict[str, dict[str, dict[str, dict[str, str]]]]:
    theme = {
        f"#btn_{text}": {
            "misc": {
                "shadow_width": "0",
                "border_width": "0",
            },
            "colours": {
                "normal_bg": "#00000000",
                "hovered_bg": "#00000000",
                "selected_bg": "#00000000",
                "disabled_bg": "#00000000",
                "active_bg": "#00000000",  # état pendant le clic maintenu
                "normal_border": "#00000000",
                "hovered_border": "#00000000",
                "selected_border": "#00000000",
                "active_border": "#00000000",
                "disabled_border": "#00000000",
                "normal_text": "#FFFFFF",
                "selected_text": "#FFFFFF",
                "active_text": "#FFFFFF",
                "hovered_text": "#FFFFFF",
            },
            "images": {
                "normal_image": make_shape(rect, color, text, "normal"),
                # "hovered_image": make_shape(rect, color, text, "hovered"),  # ne sert a rien pour l'instant
                "selected_image": make_shape(rect, color, text, "selected"),
                # "disabled_image": make_shape(rect, color, text, "disabled"),  # ne sert a rien pour l'instant
            },
        }
    }
    return theme


def shade(color: tuple[int, int, int], amount: int) -> tuple[int, int, int]:
    """Lightens (amount > 0) or darkens (amount < 0) an RGB color."""
    return tuple(max(0, min(255, c + amount)) for c in color)


def outline(bs: pg.Surface, color: tuple[int, int, int], state: bool) -> pg.Surface:
    COLOR = (244, 244, 244)
    w, h = bs.get_size()
    _ = bs.fill(COLOR, pg.Rect(1, 1, w - 2, 1))  # top line
    _ = bs.fill(COLOR, pg.Rect(0, 2, 1, h - 3))  # left line
    _ = bs.fill(COLOR, pg.Rect(w - 1, 2, 1, h - 3))  # right line
    _ = bs.fill(COLOR, pg.Rect(1, h - 1, w - 2, 1))  # bottom line
    for x, y in ((1, 2), (w - 2, 2), (1, h - 2), (w - 2, h - 2)):  # each inside corners
        bs.set_at((x, y), COLOR)
    return bs


def shadows(bs: pg.Surface, color: tuple[int, int, int], state: bool) -> pg.Surface:
    COLOR = shade(color, SHADOW)
    w, h = bs.get_size()
    _ = bs.fill(COLOR, pg.Rect(1, 2, w - 2, h - 3))
    return bs


def face(
    bs: pg.Surface, color: tuple[int, int, int], pressed: bool = False
) -> pg.Surface:
    w, h = bs.get_size()
    COLOR, y = (shade(color, DARKER), 3) if pressed else (color, 0)
    _ = bs.fill(COLOR, pg.Rect(2, y, w - 4, 1))  # top line
    _ = bs.fill(COLOR, pg.Rect(1, 1 + y, w - 2, h - 4))  # rect
    _ = bs.fill(COLOR, pg.Rect(2, (h - 3) - y, w - 4, 1))  # bottom line
    return bs


RECIPES = {False: (shadows, outline, face), True: (shadows, face, outline)}


def make_shape(
    rect: pg.Rect, color: tuple[int, int, int], name: str, state: str
) -> dict[str, str]:
    PATH = f"{ASSETS}/button/image_{name}_{state}.png"
    dimension = rect.w // RESOLUTION, rect.h // RESOLUTION
    bs = pg.Surface(dimension, pg.SRCALPHA)  # base surface
    pressed = state == "selected"
    for layer in RECIPES[pressed]:
        layer(bs, color, pressed)

    bs = pg.transform.scale(bs, rect.size)
    pg.image.save(bs, PATH)

    return {"path": PATH}
