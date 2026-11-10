import pygame as pg
import pygame_gui as ui

from src.ui import make_button as mb


class PixelUI:
    def __init__(self, screen: pg.Surface):
        self.manager: ui.UIManager = ui.UIManager(screen.get_size())
        self.buttons: dict[str, ui.elements.UIButton] = {}

    def create_button(self, rect, color, text) -> ui.elements.UIButton:
        key = text.replace(" ", "")
        theme = mb.get_theme(rect, color, key)
        self.manager.get_theme().load_theme(theme)
        btn = ui.elements.UIButton(rect, text, self.manager, object_id=f"#btn_{key}")
        self.buttons[key] = btn

        return btn
