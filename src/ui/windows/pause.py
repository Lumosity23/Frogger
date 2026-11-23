"""
The PAUSE window.

Features:
- Semi-transparent dark overlay over the frozen game
- "pause.png" logo from assets
- Big long RESUME button with "resume.png"
- HOME button with "home.png" to return to menu
"""

import os

import pygame as pg
import pygame_gui as ui

from src.state import GameState
from src.ui.windows.base import Window

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_PROJECT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ASSETS = os.path.join(ROOT_PROJECT, "assets")

COLOR_RESUME = (240, 135, 40)  # Orange arcade matching play
COLOR_HOME = (217, 87, 99)    # Soft red matching quit/exit


def load_asset_img(path: str) -> pg.Surface:
    """Load an image from assets."""
    full = os.path.join(ASSETS, path)
    if os.path.exists(full):
        return pg.image.load(full).convert_alpha()
    raise FileNotFoundError(f"Asset '{path}' not found")


class PauseWindow(Window):
    name = "PAUSE"
    background_alpha = 0

    def build(self) -> None:
        screen_rect = pg.Rect((0, 0), self.pixel.manager.window_resolution)
        cx, cy = screen_rect.centerx, screen_rect.centery
        w, h = screen_rect.width, screen_rect.height

        scale_x = w / 600.0
        scale_y = h / 1000.0

        def to_res_multiple(v: float) -> int:
            return max(4, int(round(v / 4.0) * 4))

        # Semi-transparent dark overlay to dim the paused game behind
        self.pixel.panel(
            "PAUSE_BKG",
            screen_rect,
            color="#000000",
            alpha=160,
            container=self.panel,
        )

        # 1. Pause Logo / Icon
        pause_path = os.path.join(ASSETS, "pause.png")
        if os.path.exists(pause_path):
            raw_pause = pg.image.load(pause_path).convert_alpha()
            pause_scale = max(1, int(round(4 * scale_x)))
            pause_surf = pg.transform.scale_by(raw_pause, pause_scale)
            pause_rect = pause_surf.get_rect(center=(cx, cy - int(160 * scale_y)))
            self.pause_img = self.pixel.image(
                "PAUSE_LOGO", pause_surf, pause_rect, container=self.panel
            )

        # "PAUSED" Text below logo
        self.pixel.texts["PAUSE_TEXT"] = "PAUSED"
        self.pixel.text_image(
            "PAUSE_TEXT",
            center=(cx, cy - int(80 * scale_y)),
            size=int(28 * scale_x),
            color=self.pixel.colors["title"],
            outline=self.pixel.colors["outline"],
            width=3,
            container=self.panel,
        )

        icon_scale = max(1, int(round(3 * scale_x)))
        btn_h = to_res_multiple(88 * scale_y)
        resume_btn_w = to_res_multiple(280 * scale_x)  # Big long resume button
        home_btn_w = to_res_multiple(88 * scale_x)     # Square home button

        # 2. Big Long Resume Button (centered)
        resume_y = cy + int(30 * scale_y)
        resume_x = cx - resume_btn_w // 2
        resume_logo = pg.transform.scale_by(load_asset_img("resume.png"), icon_scale)
        self.resume_btn = self.pixel.create_button(
            pg.Rect(resume_x, resume_y, resume_btn_w, btn_h),
            COLOR_RESUME,
            "RESUME",
            content=resume_logo,
            container=self.panel,
        )

        # 3. Home Button (centered below Resume)
        home_y = resume_y + btn_h + to_res_multiple(24 * scale_y)
        home_x = cx - home_btn_w // 2
        home_logo = pg.transform.scale_by(
            load_asset_img(os.path.join("assets_logo", "home.png")), icon_scale
        )
        self.home_btn = self.pixel.create_button(
            pg.Rect(home_x, home_y, home_btn_w, btn_h),
            COLOR_HOME,
            "HOME",
            content=home_logo,
            container=self.panel,
        )

    def handle_event(self, event: pg.Event) -> str | None:
        if event.type == ui.UI_BUTTON_PRESSED:
            if event.ui_element is self.resume_btn:
                self.pixel.state_mgr.set(GameState.PLAY)
            elif event.ui_element is self.home_btn:
                self.pixel.state_mgr.set(GameState.MENU)
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.pixel.state_mgr.set(GameState.PLAY)
        return None
