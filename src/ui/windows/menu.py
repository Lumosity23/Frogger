"""
The MENU window.

Features:
- "CHICKKER" pixel-art title logo from assets.
- 3 buttons at the bottom center:
  - LEADERBOARD (square, light blue, with logo_leaderboard.png) on the left
  - PLAY (orange, with play.png) in the center
  - QUIT (square, soft red, with quit.png) on the right
"""

import glob
import os

import pygame as pg
import pygame_gui as ui

from src.state import GameState
from src.ui.windows.base import Window

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_PROJECT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ASSETS = os.path.join(ROOT_PROJECT, "assets")

# Harmonious colors matching the game sprites (chicken, terrain, etc.)
COLOR_PLAY = (240, 135, 40)  # Warm arcade orange (matches chicken beak/palette)
COLOR_LEADERBOARD = (85, 175, 230)  # Soft light blue
COLOR_QUIT = (217, 87, 99)  # Soft light red (matches chicken crest palette)

MOVES: dict[int, tuple[int, int]] = {
    pg.K_LEFT: (-1, 0),
    pg.K_RIGHT: (1, 0),
    pg.K_UP: (0, -1),
    pg.K_DOWN: (0, 1),
    pg.K_a: (-1, 0),
    pg.K_d: (1, 0),
    pg.K_w: (0, -1),
    pg.K_s: (0, 1),
}


def load_asset_logo(name: str) -> pg.Surface:
    """Load a logo image from assets/assets_logo."""
    direct = os.path.join(ASSETS, "assets_logo", f"{name}.png")
    if os.path.exists(direct):
        return pg.image.load(direct)
    # Search recursively in assets_logo if organized in subdirectories
    pattern = os.path.join(ASSETS, "assets_logo", "**", f"{name}.png")
    matches = glob.glob(pattern, recursive=True)
    if matches:
        return pg.image.load(matches[0])
    raise FileNotFoundError(
        f"Logo '{name}.png' not found in {os.path.join(ASSETS, 'assets_logo')}"
    )


class MenuWindow(Window):
    name = "MENU"

    def build(self) -> None:
        screen_rect = pg.Rect((0, 0), self.pixel.manager.window_resolution)
        cx, cy = screen_rect.centerx, screen_rect.centery
        w, h = screen_rect.width, screen_rect.height

        # Calculate responsive scale based on default 600x1000 resolution
        scale_x = w / 600.0
        scale_y = h / 1000.0

        # Background panel (transparent overlay)
        self.pixel.panel(
            "MENU_BKG",
            pg.Rect(
                cx - int(320 * scale_x),
                cy - int(450 * scale_y),
                int(640 * scale_x),
                int(900 * scale_y),
            ),
            color="#694420",
            alpha=0,
            container=self.panel,
        )

        # Title: "chickker" logo from assets
        title_path = os.path.join(ASSETS, "chickker.png")
        if os.path.exists(title_path):
            raw_title = pg.image.load(title_path)
            title_scale = max(1, int(round(3 * scale_x)))
            title_surf = pg.transform.scale_by(raw_title, title_scale)
            title_rect = title_surf.get_rect(center=(cx, cy - int(340 * scale_y)))
            self.title_img = self.pixel.image(
                "TITLE", title_surf, title_rect, container=self.panel
            )
        else:
            # Fallback to text if chickker.png is missing
            self.pixel.text_image(
                "TITLE",
                center=(cx, cy - int(340 * scale_y)),
                size=int(48 * scale_x),
                color=self.pixel.colors["title"],
                outline=self.pixel.colors["outline"],
                width=3,
                container=self.panel,
            )

        # Button dimensions (multiples of RESOLUTION = 4 for sharp pixel borders)
        def to_res_multiple(v: float) -> int:
            return max(4, int(round(v / 4.0) * 4))

        icon_scale = max(1, int(round(3 * scale_x)))
        btn_h = to_res_multiple(88 * scale_y)
        sq_btn_w = to_res_multiple(88 * scale_x)  # Square side buttons
        play_btn_w = to_res_multiple(180 * scale_x)  # Center play button
        gap = to_res_multiple(16 * scale_x)

        # Bottom-center Y position
        btn_y = cy + int(340 * scale_y)

        # Total width of the 3-button group
        total_group_width = sq_btn_w + gap + play_btn_w + gap + sq_btn_w
        start_x = cx - total_group_width // 2

        # 1. Leaderboard button (left, square, light blue, logo_leaderboard)
        lead_x = start_x
        lead_logo = pg.transform.scale_by(
            load_asset_logo("logo_leaderboard"), icon_scale
        )
        self.leaderboard_btn = self.pixel.create_button(
            pg.Rect(lead_x, btn_y, sq_btn_w, btn_h),
            COLOR_LEADERBOARD,
            "LEADERBOARD",
            content=lead_logo,
            container=self.panel,
        )

        # 2. Play button (center, orange, play logo)
        play_x = lead_x + sq_btn_w + gap
        play_logo = pg.transform.scale_by(load_asset_logo("play"), icon_scale)
        self.play_btn = self.pixel.create_button(
            pg.Rect(play_x, btn_y, play_btn_w, btn_h),
            COLOR_PLAY,
            "PLAY",
            content=play_logo,
            container=self.panel,
        )

        # 3. Quit button (right, square, soft red, quit logo)
        quit_x = play_x + play_btn_w + gap
        quit_logo = pg.transform.scale_by(load_asset_logo("quit"), icon_scale)
        self.quit_btn = self.pixel.create_button(
            pg.Rect(quit_x, btn_y, sq_btn_w, btn_h),
            COLOR_QUIT,
            "QUIT",
            content=quit_logo,
            container=self.panel,
        )

    def handle_event(self, event: pg.Event) -> str | None:
        if event.type == ui.UI_BUTTON_PRESSED:
            if event.ui_element is self.play_btn:
                self.pixel.state_mgr.set(GameState.PLAY)
            if event.ui_element is self.leaderboard_btn:
                self.pixel.state_mgr.set(GameState.LEADERBOARD)
            if event.ui_element is self.quit_btn:
                return "QUIT"
        elif event.type == pg.KEYDOWN and event.key in MOVES:
            _ = pg.event.post(event)
            self.pixel.state_mgr.set(GameState.PLAY)
        return None
