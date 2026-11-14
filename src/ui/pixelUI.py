import pygame as pg
import pygame_gui as ui

from src.ui import make_button as mb


class PixelUI:
    def __init__(self, screen: pg.Surface):
        self.manager: ui.UIManager = ui.UIManager(screen.get_size())
        self.buttons: dict[str, ui.elements.UIButton] = {}

    def create_button(
        self, rect, color, text, content: pg.Surface | None = None
    ) -> ui.elements.UIButton:
        """`content` : surface a dessiner sur la face (logo, etc.). Si None, on dessine `text`."""
        key = text.replace(" ", "")
        if content is None:
            content = mb.render_text(text)
        theme = mb.get_theme(rect, color, key, content)
        self.manager.get_theme().load_theme(theme)
        # Le texte est deja dans l'image : pas de texte pygame_gui par-dessus
        btn = ui.elements.UIButton(rect, "", self.manager, object_id=f"#btn_{key}")
        self.buttons[key] = btn

        return btn
