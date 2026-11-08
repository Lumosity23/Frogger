import json
import os

import pygame as pg
import pygame_gui.elements as pui

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_PROJECT = os.path.abspath(os.path.join(HERE, "..", ".."))
ASSETS = os.path.join(ROOT_PROJECT, "assets")
THEME_OUT = os.path.join(HERE, "theme.json")
RESOLUTION = 6  # 4 px ecran = 1 px image

DARKER = -25
SHADOW = -45


def get_theme(
    rect: pg.Rect, color: tuple[int, int, int], text: str
) -> dict[str, dict[str, dict[str, dict[str, str]]]]:
    theme = {
        f"#btn_{text}": {
            "images": {
                "normal_image": make_shape(rect, color, text, "normal"),
                # "hovered_image": make_shape(rect, color, text, "hovered"),  # ne sert a rien pour l'instant
                "selected_image": make_shape(rect, color, text, "selected"),
                # "disabled_image": make_shape(rect, color, text, "disabled"),  # ne sert a rien pour l'instant
            }
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


def button(rect: pg.Rect, color: tuple[int, int, int], text: str) -> pui.UIButton:
    new_text = text.replace(" ", "")
    theme = get_theme(rect, color, new_text)
    with open(THEME_OUT, "w") as file:
        json.dump(theme, file)

    return pui.UIButton(rect, text, object_id=f"#btn_{new_text}")


if __name__ == "__main__":
    print(button(pg.Rect(0, 0, 200, 80), (134, 230, 67), "button de test"))
