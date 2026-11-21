import pygame as pg


def slice_spritesheet(path: str, n: int, scale: float = 1.0) -> dict[int, pg.Surface]:
    """Découpe une spritesheet horizontale en n frames égales."""
    image = pg.image.load(path).convert_alpha()
    if scale != 1.0:
        new_size = (round(image.get_width() * scale), round(image.get_height() * scale))
        image = pg.transform.scale(image, new_size)
    w = image.get_width() // n
    h = image.get_height()
    return {x: image.subsurface(pg.Rect(x * w, 0, w, h)).copy() for x in range(n)}


def render_digits(
    text: str | int,
    digits: dict[int, pg.Surface],
    scale: float = 1.0,
    spacing: int | None = None,
) -> pg.Surface:
    """Compose une surface contenant la suite de chiffres alignés."""
    s_text = str(text)
    if spacing is None:
        spacing = max(1, round(2 * scale))
    surfaces: list[pg.Surface] = [digits[int(c)] for c in s_text if c.isdigit()]
    if not surfaces:
        return pg.Surface((1, 1), pg.SRCALPHA)

    total_w = sum(s.get_width() for s in surfaces) + spacing * (len(surfaces) - 1)
    max_h = max(s.get_height() for s in surfaces)
    res = pg.Surface((total_w, max_h), pg.SRCALPHA)

    cur_x = 0
    for s in surfaces:
        y = (max_h - s.get_height()) // 2
        res.blit(s, (cur_x, y))
        cur_x += s.get_width() + spacing

    return res
