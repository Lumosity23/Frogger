"""
The LEADERBOARD window.

Features:
- "logo_leaderboard.png" + title
- Top 5 rankings with medals:
  - 1st: Gold medal (assets/gold_medal.png)
  - 2nd: Silver medal (assets/argent_medal.png)
  - 3rd: Bronze medal (assets/bronze_medal.png)
  - 4th & 5th: Text ranks
  - Scores rendered using tiny_digits.png
- HOME button at the bottom to return to MENU
"""

import os

import pygame as pg
import pygame_gui as ui

from src.state import GameState
from src.ui.digits import render_digits, slice_spritesheet
from src.ui.windows.base import Window
from src.utils.score import score as ScoreManager

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_PROJECT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ASSETS = os.path.join(ROOT_PROJECT, "assets")

COLOR_HOME = (217, 87, 99)          # Soft light red
TINY_DIGITS_PATH = os.path.join(ASSETS, "tiny_digits.png")
SCORE_FILE = os.path.join(ROOT_PROJECT, "src", "score.jsonc")


def load_asset_img(path: str) -> pg.Surface:
    full = os.path.join(ASSETS, path)
    if os.path.exists(full):
        return pg.image.load(full).convert_alpha()
    raise FileNotFoundError(f"Asset '{path}' not found")


class LeaderboardWindow(Window):
    name = "LEADERBOARD"
    background_alpha = 0

    def __init__(self, pixel, scene=None) -> None:
        self.scene = scene
        self.row_images: list[ui.elements.UIImage] = []
        super().__init__(pixel)

    def build(self) -> None:
        screen_rect = pg.Rect((0, 0), self.pixel.manager.window_resolution)
        cx, cy = screen_rect.centerx, screen_rect.centery
        w, h = screen_rect.width, screen_rect.height

        scale_x = w / 600.0
        scale_y = h / 1000.0

        def to_res_multiple(v: float) -> int:
            return max(4, int(round(v / 4.0) * 4))

        # 1. Background panel
        self.pixel.panel(
            "LEAD_BKG",
            pg.Rect(
                cx - int(270 * scale_x),
                cy - int(450 * scale_y),
                int(540 * scale_x),
                int(900 * scale_y),
            ),
            color="#2a1e16",
            alpha=190,
            container=self.panel,
        )

        # 2. Header: Logo + "LEADERBOARD"
        lead_logo = load_asset_img(os.path.join("assets_logo", "logo_leaderboard.png"))
        logo_scale = max(1, int(round(3 * scale_x)))
        logo_surf = pg.transform.scale_by(lead_logo, logo_scale)
        logo_rect = logo_surf.get_rect(center=(cx, cy - int(380 * scale_y)))
        self.pixel.image("LEAD_LOGO_ICON", logo_surf, logo_rect, container=self.panel)

        self.pixel.texts["LEAD_TITLE"] = "TOP CHICKENS"
        self.pixel.text_image(
            "LEAD_TITLE",
            center=(cx, cy - int(320 * scale_y)),
            size=int(24 * scale_x),
            color=self.pixel.colors["title"],
            outline=self.pixel.colors["outline"],
            width=3,
            container=self.panel,
        )

        # 3. Load Medals
        medal_scale = max(1, int(round(2.5 * scale_x)))
        self.gold_surf = pg.transform.scale_by(load_asset_img("gold_medal.png"), medal_scale)
        self.silver_surf = pg.transform.scale_by(load_asset_img("argent_medal.png"), medal_scale)
        self.bronze_surf = pg.transform.scale_by(load_asset_img("bronze_medal.png"), medal_scale)

        # 4. Digits
        self.digit_scale = max(1.0, 2.0 * scale_x)
        self.digits = slice_spritesheet(TINY_DIGITS_PATH, 10, self.digit_scale)

        # 5. Populate Rows
        self.populate_scores(cx, cy, scale_x, scale_y)

        # 6. Home Button (bottom center)
        icon_scale = max(1, int(round(3 * scale_x)))
        btn_h = to_res_multiple(80 * scale_y)
        sq_btn_w = to_res_multiple(88 * scale_x)
        btn_y = cy + int(340 * scale_y)
        home_x = cx - sq_btn_w // 2

        home_logo = pg.transform.scale_by(
            load_asset_img(os.path.join("assets_logo", "home.png")), icon_scale
        )
        self.home_btn = self.pixel.create_button(
            pg.Rect(home_x, btn_y, sq_btn_w, btn_h),
            COLOR_HOME,
            "LEAD_HOME",
            content=home_logo,
            container=self.panel,
        )

    def populate_scores(self, cx: int, cy: int, scale_x: float, scale_y: float) -> None:
        # Load scores
        board_data: dict[int, dict] = {}
        try:
            sm = ScoreManager(SCORE_FILE)
            board_data = sm.get_leaderboard()
        except Exception:
            board_data = {}

        # Default fallbacks if empty
        default_names = ["HEN_SOLO", "CLUCK_NORRIS", "EGG_HEAD", "ROOSTER", "NUGGET"]
        default_scores = [1500, 1200, 900, 600, 300]

        start_y = cy - int(240 * scale_y)
        row_gap = int(105 * scale_y)
        row_w = int(480 * scale_x)
        row_h = int(85 * scale_y)

        for i in range(1, 6):
            ry = start_y + (i - 1) * row_gap
            rx = cx - row_w // 2

            # Background strip for each rank
            bg_color = "#3d2d22" if i % 2 == 1 else "#34261c"
            self.pixel.panel(
                f"LEAD_ROW_BG_{i}",
                pg.Rect(rx, ry, row_w, row_h),
                color=bg_color,
                alpha=220,
                container=self.panel,
            )

            # Medal / Rank badge
            badge_x = rx + int(30 * scale_x)
            badge_y = ry + row_h // 2
            if i == 1:
                b_rect = self.gold_surf.get_rect(center=(badge_x, badge_y))
                self.pixel.image(f"LEAD_MEDAL_{i}", self.gold_surf, b_rect, container=self.panel)
            elif i == 2:
                b_rect = self.silver_surf.get_rect(center=(badge_x, badge_y))
                self.pixel.image(f"LEAD_MEDAL_{i}", self.silver_surf, b_rect, container=self.panel)
            elif i == 3:
                b_rect = self.bronze_surf.get_rect(center=(badge_x, badge_y))
                self.pixel.image(f"LEAD_MEDAL_{i}", self.bronze_surf, b_rect, container=self.panel)
            else:
                self.pixel.texts[f"RANK_{i}"] = f"#{i}"
                self.pixel.text_image(
                    f"RANK_{i}",
                    center=(badge_x, badge_y),
                    size=int(18 * scale_x),
                    color=(180, 180, 180),
                    container=self.panel,
                )

            # Player Name
            entry = board_data.get(i)
            name = entry.get("name") if entry else default_names[i - 1]
            score_val = entry.get("score") if entry else default_scores[i - 1]

            name_key = f"LEAD_NAME_{i}"
            self.pixel.texts[name_key] = str(name)[:10]
            name_surf = self.pixel.render_text(
                self.pixel.texts[name_key],
                size=int(16 * scale_x),
                color=(255, 255, 255),
                outline=(0, 0, 0),
                width=2,
            )
            name_rect = name_surf.get_rect(midleft=(rx + int(70 * scale_x), badge_y))
            self.pixel.image(name_key, name_surf, name_rect, container=self.panel)

            # Score with tiny_digits
            score_surf = render_digits(score_val, self.digits, self.digit_scale)
            score_rect = score_surf.get_rect(midright=(rx + row_w - int(25 * scale_x), badge_y))
            self.pixel.image(f"LEAD_SCORE_{i}", score_surf, score_rect, container=self.panel)

    def handle_event(self, event: pg.Event) -> str | None:
        if event.type == ui.UI_BUTTON_PRESSED:
            if event.ui_element is self.home_btn:
                self.pixel.state_mgr.set(GameState.MENU)
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.pixel.state_mgr.set(GameState.MENU)
        return None
