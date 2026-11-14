import os

import pygame as pg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_PROJECT = os.path.abspath(os.path.join(HERE, "..", ".."))
ASSETS = os.path.join(ROOT_PROJECT, "assets")
RESOLUTION = 6  # 4 px ecran = 1 px image

FONT_PATH = os.path.join(ASSETS, "font", "PublicPixel.ttf")  # .ttf, pas .woff
FONT_SIZE = 16

DARKER = -25
SHADOW = -45
PRESS_OFFSET = 3  # decalage de la face (et du contenu) quand on appuie, en pixels image


def get_theme(
    rect: pg.Rect,
    color: tuple[int, int, int],
    text: str,
    content: pg.Surface,
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
                "active_bg": "#00000000",
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
                "normal_image": make_shape(rect, color, text, "normal", content),
                "selected_image": make_shape(rect, color, text, "selected", content),
            },
        }
    }
    return theme


def render_text(text: str, color: tuple[int, int, int] = (255, 255, 255)) -> pg.Surface:
    font = pg.font.Font(FONT_PATH, FONT_SIZE)
    return font.render(text, False, color)


def shade(color: tuple[int, int, int], amount: int) -> tuple[int, int, int]:
    """Lightens (amount > 0) or darkens (amount < 0) an RGB color."""
    return tuple(max(0, min(255, c + amount)) for c in color)


def grid(bs: pg.Surface) -> tuple[int, int]:
    """Taille de la surface en pixels image."""
    return bs.get_width() // RESOLUTION, bs.get_height() // RESOLUTION


def cell(
    bs: pg.Surface, color: tuple[int, int, int], x: int, y: int, w: int, h: int
) -> None:
    """Remplit un bloc (x, y, w, h) exprime en pixels image."""
    gw, gh = grid(bs)
    fx, fy = bs.get_width() / gw, bs.get_height() / gh
    x0, y0 = round(x * fx), round(y * fy)
    _ = bs.fill(
        color, pg.Rect(x0, y0, round((x + w) * fx) - x0, round((y + h) * fy) - y0)
    )


def outline(bs: pg.Surface, color: tuple[int, int, int]) -> None:
    COLOR = (244, 244, 244)
    gw, gh = grid(bs)
    cell(bs, COLOR, 1, 1, gw - 2, 1)  # top line
    cell(bs, COLOR, 0, 2, 1, gh - 3)  # left line
    cell(bs, COLOR, gw - 1, 2, 1, gh - 3)  # right line
    cell(bs, COLOR, 1, gh - 1, gw - 2, 1)  # bottom line
    for x, y in ((1, 2), (gw - 2, 2), (1, gh - 2), (gw - 2, gh - 2)):  # inside corners
        cell(bs, COLOR, x, y, 1, 1)


def shadows(bs: pg.Surface, color: tuple[int, int, int]) -> None:
    COLOR = shade(color, SHADOW)
    gw, gh = grid(bs)
    cell(bs, COLOR, 1, 2, gw - 2, gh - 3)


def face(
    bs: pg.Surface,
    color: tuple[int, int, int],
    content: pg.Surface | None = None,
    pressed: bool = False,
) -> None:
    gw, gh = grid(bs)
    y = PRESS_OFFSET if pressed else 0
    COLOR = shade(color, DARKER) if pressed else color
    cell(bs, COLOR, 2, y, gw - 4, 1)  # top line
    cell(bs, COLOR, 1, 1 + y, gw - 2, gh - 4)  # rect
    cell(bs, COLOR, 2, gh - 3 - y, gw - 4, 1)  # bottom line

    if content is not None:
        dy = y * bs.get_height() // gh  # meme decalage que la face, en pixels ecran
        draw_content(bs, content, dy)


def draw_content(bs: pg.Surface, content: pg.Surface, dy: int = 0) -> None:
    """Centre le contenu sur le bouton, en pleine resolution (pour rester net).

    Seules les marges vides sont retirees, pour centrer sur les pixels visibles.
    """
    visible = content.get_bounding_rect()
    if visible.w == 0 or visible.h == 0:
        return

    dst = pg.Rect(0, 0, visible.w, visible.h)
    dst.center = bs.get_rect().center
    dst.y += dy // 2

    _ = bs.blit(content, dst, area=visible)


def make_shape(
    rect: pg.Rect,
    color: tuple[int, int, int],
    name: str,
    state: str,
    content: pg.Surface | None = None,
) -> dict[str, str]:
    PATH = f"{ASSETS}/button/image_{name}_{state}.png"
    bs = pg.Surface(rect.size, pg.SRCALPHA)

    if state == "normal":
        shadows(bs, color)
        outline(bs, color)
        face(bs, color, content)
    elif state == "selected":
        shadows(bs, color)
        face(bs, color, content, pressed=True)
        outline(bs, color)
    else:
        raise ValueError(f"etat de bouton inconnu : {state}")

    pg.image.save(bs, PATH)
    return {"path": PATH}
