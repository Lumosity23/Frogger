import pygame as pg
import pygame_gui as ui

from src.state import GameState, StateManager
from src.ui import make_button as mb
from src.ui.windows.base import Window
from src.utils import log

FONT_PATH = "assets/font/PublicPixel.ttf"


class PixelUI:
    def __init__(self, screen: pg.Surface, state_mgr: StateManager):
        self.manager: ui.UIManager = ui.UIManager(screen.get_size())
        self.state_mgr: StateManager = state_mgr
        self.state_mgr.subscribe(self.on_state_change)

        # UIElements
        self.buttons: dict[str, ui.elements.UIButton] = {}
        self.images: dict[str, ui.elements.UIImage] = {}
        self.panels: dict[str, ui.elements.UIPanel] = {}

        # Windows
        self.windows: dict[str, Window] = {}
        self.current: Window | None = None

        # Data
        self.colors: dict[str, str] = {}
        self.texts: dict[str, str] = {}
        self._fonts: dict[int, pg.font.Font] = {}  # one font per size, cached in memory

        self._define_assets()

    # Definition of the UI
    def _define_assets(self) -> None:
        self.colors = {
            "text": (255, 255, 255),
            "title": (255, 178, 102),
            "outline": (0, 0, 0),
            "purple": "#8f2ead",
            "purple_hover": "#a94fc4",
        }

        self.texts = {
            "TITLE": "CHICKENNER",
            "PLAY": "PLAY",
            "QUIT": "QUIT",
        }

    def font(self, size: int) -> pg.font.Font:
        """Return the project font at the requested size (loaded once)."""
        if size not in self._fonts:
            self._fonts[size] = pg.font.Font(FONT_PATH, size)
        return self._fonts[size]

    def text(self, key: str) -> str:
        return self.texts[key]

    def set_style(self, selector: str, **props) -> None:
        """Add a style to the pygame_gui theme. e.g. set_style("#pnl_X", colours={...})"""
        self.manager.get_theme().load_theme({selector: props})

    # Text rendered as surfaces
    def render_text(
        self,
        text: str,
        size: int = 24,
        color: tuple[int, int, int] = (255, 255, 255),
        outline: tuple[int, int, int] | None = None,
        width: int = 3,
    ) -> pg.Surface:
        """Render text to a surface, with an optional outline.

        The outline is the same text in the outline colour, drawn offset in
        all 8 directions; the main text is drawn on top.
        """
        font = self.font(size)
        base = font.render(text, False, color)
        if outline is None or width <= 0:
            return base

        shape = font.render(text, False, outline)
        w, h = base.get_size()
        out = pg.Surface((w + 2 * width, h + 2 * width), pg.SRCALPHA)
        for dx in range(-width, width + 1):
            for dy in range(-width, width + 1):
                if dx or dy:
                    _ = out.blit(shape, (width + dx, width + dy))
        _ = out.blit(base, (width, width))
        return out

    def text_image(
        self,
        key: str,
        center: tuple[int, int],
        size: int = 24,
        color: tuple[int, int, int] = (255, 255, 255),
        outline: tuple[int, int, int] | None = None,
        width: int = 3,
        container: ui.core.IContainerLikeInterface | None = None,
    ) -> ui.elements.UIImage:
        surface = self.render_text(self.texts[key], size, color, outline, width)
        return self.image(key, surface, surface.get_rect(center=center), container)

    def image(
        self,
        key: str,
        surface: pg.Surface,
        rect: pg.Rect,
        container: ui.core.IContainerLikeInterface | None = None,
    ) -> ui.elements.UIImage:
        img = ui.elements.UIImage(
            relative_rect=rect,
            image_surface=surface,
            manager=self.manager,
            container=container,
        )
        self.images[key] = img
        return img

    # Containers
    def panel(
        self,
        key: str,
        rect: pg.Rect,
        color: str = "#000000",
        alpha: int = 255,
        container: ui.core.IContainerLikeInterface | None = None,
    ) -> ui.elements.UIPanel:
        """Coloured container, from fully transparent to opaque.

        color: hex colour, e.g. "#000000"
        alpha: 0 = fully transparent, 255 = opaque
        """
        rgba = self._rgba(color, alpha)
        self.set_style(
            f"#pnl_{key}",
            colours={"normal_bg": rgba, "dark_bg": rgba, "normal_border": rgba},
            misc={"border_width": "0", "shadow_width": "0"},
        )
        pnl = ui.elements.UIPanel(
            relative_rect=rect,
            manager=self.manager,
            container=container,
            object_id=f"#pnl_{key}",
        )
        self.panels[key] = pnl
        return pnl

    @staticmethod
    def _rgba(color: str, alpha: int) -> str:
        """Convert '#RRGGBB' + alpha (0-255) to '#RRGGBBAA'."""
        alpha = max(0, min(255, int(alpha)))
        return f"#{color.lstrip('#')[:6]}{alpha:02x}"

    # Buttons
    def create_button(
        self,
        rect,
        color,
        text,
        content: pg.Surface | None = None,
        container: ui.core.IContainerLikeInterface | None = None,
    ) -> ui.elements.UIButton:
        """Pixel-art button, drawn from an image generated by make_button.
        `content`: surface drawn on the button face (logo, etc.). If None, `text` is drawn."""
        key = text.replace(" ", "")
        if content is None:
            content = mb.render_text(text)
        theme = mb.get_theme(rect, color, key, content)
        self.manager.get_theme().load_theme(theme)
        # The text is already in the image: no pygame_gui text on top
        btn = ui.elements.UIButton(
            rect, "", self.manager, container=container, object_id=f"#btn_{key}"
        )
        self.buttons[key] = btn
        return btn

    # Window management
    def add_window(self, window: Window) -> None:
        self.windows[window.name] = window

    def open(self, name: str) -> None:
        if self.current is not None:
            self.current.hide()
        self.current = self.windows[name]
        # log.debug(self.current.__class__.__name__)
        self.current.show()

    def on_state_change(self, new_state: GameState, old_state: GameState) -> None:
        # Ouvre la bonne fenêtre selon le nouvel état
        mapping = {
            GameState.MENU: "MENU",
            GameState.PLAY: "HUD",
            GameState.PAUSE: "PAUSE",
            GameState.GAME_OVER: "GAME_OVER",
            GameState.LEADERBOARD: "LEADERBOARD",
        }
        window_name = mapping.get(new_state)
        if window_name and window_name in self.windows:
            self.open(window_name)

    def handle_event(self, event: pg.Event) -> bool:
        consumed = bool(self.manager.process_events(event))
        if self.current is None:
            return consumed
        next_name = self.current.handle_event(event)
        if next_name is not None:
            if next_name == "QUIT":
                pg.event.post(pg.event.Event(pg.QUIT))
            elif next_name in self.windows:
                self.open(next_name)
            return True
        return consumed

    def update(self, dt: float) -> None:
        if self.current is not None:
            self.current.update(dt)
        self.manager.update(dt)

    def draw(self, screen: pg.Surface) -> None:
        self.manager.draw_ui(screen)
