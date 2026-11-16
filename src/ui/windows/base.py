import pygame as pg
import pygame_gui as ui


class Window:
    """Base class for a window. Each window is a file that inherits from it.

    - name: name used to open it (pixel.open("MENU"))
    - build: creates the elements (called once, at creation)
    - handle_event: returns the next window's name, or None
    """

    name: str = ""
    background: str = "#000000"  # window background colour
    background_alpha: int = 0  # 0 = fully transparent background

    def __init__(self, pixel) -> None:
        self.pixel = pixel  # PixelUI
        self.panel = pixel.panel(
            f"WIN_{self.name}",
            pg.Rect((0, 0), pixel.manager.window_resolution),
            color=self.background,
            alpha=self.background_alpha,
        )
        self.build()
        self.hide()

    def build(self) -> None:
        """Override: create the elements with container=self.panel."""

    def show(self) -> None:
        self.panel.show()

    def hide(self) -> None:
        self.panel.hide()

    def handle_event(self, event: pg.Event) -> str | None:
        """Override. Return the next window's name, or None."""
        return None
