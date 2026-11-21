"""
The GAME_OVER window.

Features:
- Semi-transparent dark overlay
- "game_over.png" pixel-art logo
- Final score display using digits
- 3 buttons at bottom:
  - HOME (square, red) to return to menu
  - PLAY / REPLAY (wide, orange) to restart run
  - LEADERBOARD (square, light blue) to check rankings
"""

import os

import pygame as pg
import pygame_gui as ui

from src.state import GameState
from src.ui.digits import render_digits, slice_spritesheet
from src.ui.windows.base import Window

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_PROJECT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ASSETS = os.path.join(ROOT_PROJECT, "assets")

COLOR_PLAY = (240, 135, 40)         # Warm arcade orange
COLOR_LEADERBOARD = (85, 175, 230)   # Soft light blue
COLOR_HOME = (217, 87, 99)          # Soft light red
TINY_DIGITS_PATH = os.path.join(ASSETS, "tiny_digits.png")


def load_asset_img(path: str) -> pg.Surface:
    full = os.path.join(ASSETS, path)
    if os.path.exists(full):
        return pg.image.load(full).convert_alpha()
    raise FileNotFoundError(f"Asset '{path}' not found")


class GameOverWindow(Window):
    name = "GAME_OVER"
    background_alpha = 0

    def __init__(self, pixel, scene=None) -> None:
        self.scene = scene
        self.last_score: int = -1
        super().__init__(pixel)

    def build(self) -> None:
        screen_rect = pg.Rect((0, 0), self.pixel.manager.window_resolution)
        cx, cy = screen_rect.centerx, screen_rect.centery
        w, h = screen_rect.width, screen_rect.height

        scale_x = w / 600.0
        scale_y = h / 1000.0

        def to_res_multiple(v: float) -> int:
            return max(4, int(round(v / 4.0) * 4))

        # 1. Dark overlay
        self.pixel.panel(
            "GAMEOVER_BKG",
            screen_rect,
            color="#000000",
            alpha=180,
            container=self.panel,
        )

        # 2. Game Over Title Logo
        go_path = os.path.join(ASSETS, "game_over.png")
        if os.path.exists(go_path):
            raw_go = pg.image.load(go_path).convert_alpha()
            go_scale = max(1.0, 2.3 * scale_x)
            go_surf = pg.transform.scale_by(raw_go, go_scale)
            go_rect = go_surf.get_rect(center=(cx, cy - int(240 * scale_y)))
            self.go_img = self.pixel.image(
                "GAMEOVER_TITLE", go_surf, go_rect, container=self.panel
            )

        # 3. Score Section
        self.pixel.texts["SCORE_LABEL"] = "SCORE"
        self.pixel.text_image(
            "SCORE_LABEL",
            center=(cx, cy - int(120 * scale_y)),
            size=int(22 * scale_x),
            color=self.pixel.colors["title"],
            outline=self.pixel.colors["outline"],
            width=3,
            container=self.panel,
        )

        # Digits spritesheet for score
        digit_scale = max(1.0, 2.5 * scale_x)
        self.digits = slice_spritesheet(TINY_DIGITS_PATH, 10, digit_scale)
        initial_score_surf = render_digits(0, self.digits, digit_scale)
        self.score_rect = initial_score_surf.get_rect(center=(cx, cy - int(60 * scale_y)))
        self.score_img = self.pixel.image(
            "GAMEOVER_SCORE", initial_score_surf, self.score_rect, container=self.panel
        )

        # 4. Buttons at bottom
        icon_scale = max(1, int(round(3 * scale_x)))
        btn_h = to_res_multiple(88 * scale_y)
        sq_btn_w = to_res_multiple(88 * scale_x)
        play_btn_w = to_res_multiple(180 * scale_x)
        gap = to_res_multiple(16 * scale_x)

        btn_y = cy + int(240 * scale_y)
        total_group_width = sq_btn_w + gap + play_btn_w + gap + sq_btn_w
        start_x = cx - total_group_width // 2

        # Home button (left)
        home_logo = pg.transform.scale_by(
            load_asset_img(os.path.join("assets_logo", "home.png")), icon_scale
        )
        self.home_btn = self.pixel.create_button(
            pg.Rect(start_x, btn_y, sq_btn_w, btn_h),
            COLOR_HOME,
            "GO_HOME",
            content=home_logo,
            container=self.panel,
        )

        # Replay button (center)
        play_x = start_x + sq_btn_w + gap
        play_logo = pg.transform.scale_by(
            load_asset_img(os.path.join("assets_logo", "play.png")), icon_scale
        )
        self.replay_btn = self.pixel.create_button(
            pg.Rect(play_x, btn_y, play_btn_w, btn_h),
            COLOR_PLAY,
            "GO_REPLAY",
            content=play_logo,
            container=self.panel,
        )

        # Leaderboard button (right)
        lead_x = play_x + play_btn_w + gap
        lead_logo = pg.transform.scale_by(
            load_asset_img(os.path.join("assets_logo", "logo_leaderboard.png")), icon_scale
        )
        self.leaderboard_btn = self.pixel.create_button(
            pg.Rect(lead_x, btn_y, sq_btn_w, btn_h),
            COLOR_LEADERBOARD,
            "GO_LEADERBOARD",
            content=lead_logo,
            container=self.panel,
        )

    def update(self, dt: float) -> None:
        if self.scene is not None and hasattr(self.scene, "score"):
            current = self.scene.score.score + getattr(self.scene.score, "current_score", 0)
            if current != self.last_score:
                self.last_score = current
                screen_rect = pg.Rect((0, 0), self.pixel.manager.window_resolution)
                cx = screen_rect.centerx
                cy = screen_rect.centery
                scale_y = screen_rect.height / 1000.0
                scale_x = screen_rect.width / 600.0
                digit_scale = max(1.0, 2.5 * scale_x)
                surf = render_digits(current, self.digits, digit_scale)
                self.score_img.set_image(surf)
                self.score_img.set_dimensions(surf.get_size())
                rect = surf.get_rect(center=(cx, cy - int(60 * scale_y)))
                self.score_img.set_relative_position((rect.x, rect.y))

    def handle_event(self, event: pg.Event) -> str | None:
        if event.type == ui.UI_BUTTON_PRESSED:
            if event.ui_element is self.replay_btn:
                self.pixel.state_mgr.set(GameState.PLAY)
            elif event.ui_element is self.home_btn:
                self.pixel.state_mgr.set(GameState.MENU)
            elif event.ui_element is self.leaderboard_btn:
                self.pixel.state_mgr.set(GameState.LEADERBOARD)
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.pixel.state_mgr.set(GameState.MENU)
        return None
