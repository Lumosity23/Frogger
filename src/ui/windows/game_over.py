"""
The GAME_OVER window.

Features:
- Semi-transparent dark overlay over the frozen game
- Central arcade card frame (#2a1e16) matching LEADERBOARD
- Pixel-art "game_over.png" title logo
- Dynamic status banner ("★ NEW HIGH SCORE! ★", "★ TOP 5 QUALIFIED! ★", etc.)
- Final score display with tiny_digits.png
- Best score display with gold_medal.png and tiny_digits.png
- Retro name entry box (UITextEntryLine) & SAVE button to save to leaderboard
- 3 arcade navigation buttons at bottom:
  - HOME (square, soft red) to return to menu
  - PLAY / REPLAY (wide, orange) to restart run
  - LEADERBOARD (square, light blue) to check rankings
- Full integration with Scene.score (auto-saving on exit or enter, seed preservation)
"""

import os

import pygame as pg
import pygame_gui as ui

from src.state import GameState
from src.ui import make_button as mb
from src.ui.digits import render_digits, slice_spritesheet
from src.ui.windows.base import Window

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_PROJECT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ASSETS = os.path.join(ROOT_PROJECT, "assets")

COLOR_PLAY = (240, 135, 40)  # Warm arcade orange
COLOR_LEADERBOARD = (85, 175, 230)  # Soft light blue
COLOR_HOME = (217, 87, 99)  # Soft light red
COLOR_SAVE = (90, 185, 100)  # Arcade green for save action

TINY_DIGITS_PATH = os.path.join(ASSETS, "tiny_digits.png")
GOLD_MEDAL_PATH = os.path.join(ASSETS, "gold_medal.png")


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
        self.last_best: int = -1
        self.is_saved: bool = False
        self.player_name: str = "PLAYER"
        super().__init__(pixel)

    def build(self) -> None:
        screen_rect = pg.Rect((0, 0), self.pixel.manager.window_resolution)
        cx, cy = screen_rect.centerx, screen_rect.centery
        w, h = screen_rect.width, screen_rect.height

        scale_x = w / 600.0
        scale_y = h / 1000.0

        def to_res_multiple(v: float) -> int:
            return max(4, int(round(v / 4.0) * 4))

        # 1. Dark overlay across the entire screen
        self.pixel.panel(
            "GO_BKG",
            screen_rect,
            color="#000000",
            alpha=185,
            container=self.panel,
        )

        # 2. Main Central Arcade Card Frame
        card_w = to_res_multiple(520 * scale_x)
        card_h = to_res_multiple(940 * scale_y)
        card_rect = pg.Rect(cx - card_w // 2, cy - card_h // 2, card_w, card_h)
        self.card = self.pixel.panel(
            "GO_CARD",
            card_rect,
            color="#2a1e16",
            alpha=235,
            container=self.panel,
        )

        # 3. Game Over Title Logo
        go_path = os.path.join(ASSETS, "game_over.png")
        if os.path.exists(go_path):
            raw_go = pg.image.load(go_path).convert_alpha()
            go_scale = max(1.0, 2.0 * scale_x)
            go_surf = pg.transform.scale_by(raw_go, go_scale)
            go_rect = go_surf.get_rect(center=(cx, cy - int(400 * scale_y)))
            self.pixel.image("GO_TITLE", go_surf, go_rect, container=self.panel)

        # 4. Dynamic Banner / Subtitle Text
        self.pixel.texts["GO_BANNER"] = "GAME OVER"
        self.banner_img = self.pixel.text_image(
            "GO_BANNER",
            center=(cx, cy - int(360 * scale_y)),
            size=int(15 * scale_x),
            color=self.pixel.colors["title"],
            outline=self.pixel.colors["outline"],
            width=2,
            container=self.panel,
        )

        # 5. Final Score Section Box
        box_w = to_res_multiple(440 * scale_x)
        box_h = to_res_multiple(135 * scale_y)
        score_box_rect = pg.Rect(cx - box_w // 2, cy - int(305 * scale_y), box_w, box_h)
        self.pixel.panel(
            "GO_SCORE_BOX",
            score_box_rect,
            color="#3d2d22",
            alpha=230,
            container=self.panel,
        )

        # Label "FINAL SCORE"
        self.pixel.texts["GO_SCORE_LABEL"] = "FINAL SCORE"
        self.pixel.text_image(
            "GO_SCORE_LABEL",
            center=(cx, cy - int(290 * scale_y)),
            size=int(14 * scale_x),
            color=self.pixel.colors["title"],
            outline=self.pixel.colors["outline"],
            width=2,
            container=self.panel,
        )

        # Digits spritesheet for scores
        self.score_digit_scale = max(1.5, 4.8 * scale_x)
        self.score_digits = slice_spritesheet(
            TINY_DIGITS_PATH, 10, self.score_digit_scale
        )

        initial_score_surf = render_digits(0, self.score_digits, self.score_digit_scale)
        self.score_rect = initial_score_surf.get_rect(
            center=(cx, cy - int(67 * scale_y))
        )
        self.score_img = self.pixel.image(
            "GO_SCORE_DIGITS", initial_score_surf, self.score_rect, container=self.panel
        )

        # 6. Best Score Section Box
        best_box_h = to_res_multiple(64 * scale_y)
        best_box_rect = pg.Rect(
            cx - box_w // 2, cy - int(155 * scale_y), box_w, best_box_h
        )
        self.pixel.panel(
            "GO_BEST_BOX",
            best_box_rect,
            color="#34261c",
            alpha=230,
            container=self.panel,
        )

        # Gold medal icon
        if os.path.exists(GOLD_MEDAL_PATH):
            medal_scale = max(1.0, 2.0 * scale_x)
            medal_surf = pg.transform.scale_by(
                load_asset_img("gold_medal.png"), medal_scale
            )
            medal_rect = medal_surf.get_rect(
                midleft=(cx - box_w // 2 + int(20 * scale_x), cy - int(123 * scale_y))
            )
            self.pixel.image(
                "GO_BEST_MEDAL", medal_surf, medal_rect, container=self.panel
            )

        # "BEST SCORE" Label
        self.pixel.texts["GO_BEST_LABEL"] = "BEST SCORE"
        best_label_surf = self.pixel.render_text(
            self.pixel.texts["GO_BEST_LABEL"],
            size=int(13 * scale_x),
            color=(210, 210, 210),
            outline=(0, 0, 0),
            width=2,
        )
        best_label_rect = best_label_surf.get_rect(
            midleft=(cx - box_w // 2 + int(65 * scale_x), cy - int(123 * scale_y))
        )
        self.pixel.image(
            "GO_BEST_LABEL", best_label_surf, best_label_rect, container=self.panel
        )

        # Best score digits
        self.best_digit_scale = max(1.0, 2.0 * scale_x)
        self.best_digits = slice_spritesheet(
            TINY_DIGITS_PATH, 10, self.best_digit_scale
        )
        initial_best_surf = render_digits(0, self.best_digits, self.best_digit_scale)
        self.best_rect = initial_best_surf.get_rect(
            midright=(cx + box_w // 2 - int(20 * scale_x), cy - int(123 * scale_y))
        )
        self.best_img = self.pixel.image(
            "GO_BEST_DIGITS", initial_best_surf, self.best_rect, container=self.panel
        )

        # 7. Name Entry & Save Section
        name_section_y = cy + int(25 * scale_y)
        self.pixel.texts["GO_NAME_LABEL"] = "ENTER NAME:"
        self.name_label_img = self.pixel.text_image(
            "GO_NAME_LABEL",
            center=(cx, name_section_y + int(10 * scale_y)),
            size=int(12 * scale_x),
            color=(230, 230, 230),
            outline=(0, 0, 0),
            width=2,
            container=self.panel,
        )

        # Style retro theme for UITextEntryLine
        self.pixel.set_style(
            "#go_name_entry",
            colours={
                "dark_bg": "#1c140e",
                "normal_bg": "#221912",
                "hovered_bg": "#2e2118",
                "active_bg": "#2e2118",
                "normal_border": "#553a26",
                "hovered_border": "#8f5b35",
                "active_border": "#f08728",
                "text": "#ffffff",
                "selected_text": "#ffffff",
                "selected_bg": "#f08728",
            },
            font={
                "name": "PublicPixel",
                "size": str(max(10, int(12 * scale_x))),
                "regular_path": "assets/font/PublicPixel.ttf",
            },
            misc={"border_width": "2", "shadow_width": "0"},
        )

        name_w = to_res_multiple(230 * scale_x)
        name_h = to_res_multiple(44 * scale_y)
        save_w = to_res_multiple(84 * scale_x)
        gap_input = to_res_multiple(12 * scale_x)
        total_input_w = name_w + gap_input + save_w
        input_start_x = cx - total_input_w // 2

        entry_rect = pg.Rect(
            input_start_x, name_section_y + int(30 * scale_y), name_w, name_h
        )
        self.name_entry = ui.elements.UITextEntryLine(
            relative_rect=entry_rect,
            manager=self.pixel.manager,
            container=self.panel,
            object_id="#go_name_entry",
            initial_text=self.player_name,
        )
        self.name_entry.set_text_length_limit(10)

        # Save Button
        save_btn_rect = pg.Rect(
            input_start_x + name_w + gap_input,
            name_section_y + int(30 * scale_y),
            save_w,
            name_h,
        )
        save_content = mb.render_text("SAVE")
        self.save_btn = self.pixel.create_button(
            save_btn_rect,
            COLOR_SAVE,
            "GO_SAVE",
            content=save_content,
            container=self.panel,
        )

        # Status text below name entry
        self.pixel.texts["GO_STATUS"] = ""
        self.status_img = self.pixel.text_image(
            "GO_STATUS",
            center=(cx, name_section_y + int(95 * scale_y)),
            size=int(12 * scale_x),
            color=(100, 230, 100),
            outline=(0, 0, 0),
            width=2,
            container=self.panel,
        )

        # 8. Navigation Buttons at Bottom
        icon_scale = max(1, int(round(3 * scale_x)))
        btn_h = to_res_multiple(80 * scale_y)
        sq_btn_w = to_res_multiple(88 * scale_x)
        play_btn_w = to_res_multiple(220 * scale_x)
        gap = to_res_multiple(16 * scale_x)

        btn_y = cy + int(365 * scale_y)
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
            load_asset_img(os.path.join("assets_logo", "logo_leaderboard.png")),
            icon_scale,
        )
        self.leaderboard_btn = self.pixel.create_button(
            pg.Rect(lead_x, btn_y, sq_btn_w, btn_h),
            COLOR_LEADERBOARD,
            "GO_LEADERBOARD",
            content=lead_logo,
            container=self.panel,
        )

    def show(self) -> None:
        super().show()
        self.refresh()

    def hide_entry_name(self, yes: bool = True):
        element = [self.save_btn, self.name_entry, self.status_img, self.name_label_img]
        for e in element:
            if yes:
                e.hide()
            else:
                e.show()

    def refresh(self) -> None:
        """Re-reads the score from Scene and updates all UI components."""
        score_mgr = getattr(self.scene, "score", None)
        current = score_mgr.score if score_mgr else 0
        best = score_mgr.highest_score if score_mgr else 0

        self.last_score = current
        self.last_best = max(best, current)
        self.is_saved = getattr(score_mgr, "saved", False)

        screen_rect = pg.Rect((0, 0), self.pixel.manager.window_resolution)
        cx, cy = screen_rect.centerx, screen_rect.centery
        scale_x = screen_rect.width / 600.0
        scale_y = screen_rect.height / 1000.0

        # Update Final Score Digits
        surf = render_digits(current, self.score_digits, self.score_digit_scale)
        self.score_img.set_image(surf)
        self.score_img.set_dimensions(surf.get_size())
        rect = surf.get_rect(center=(cx, cy - int(222 * scale_y)))
        self.score_img.set_relative_position((rect.x, rect.y))

        # Update Best Score Digits
        best_surf = render_digits(
            self.last_best, self.best_digits, self.best_digit_scale
        )
        self.best_img.set_image(best_surf)
        self.best_img.set_dimensions(best_surf.get_size())
        box_w = max(4, int(round((440 * scale_x) / 4.0) * 4))
        b_rect = best_surf.get_rect(
            midright=(cx + box_w // 2 - int(20 * scale_x), cy - int(123 * scale_y))
        )
        self.best_img.set_relative_position((b_rect.x, b_rect.y))

        # Update Banner & Colors
        # is_high = score_mgr.is_high_score if (score_mgr and current > 0) else False
        #  = score_mgr.is_better if (score_mgr and current > 0) else False

        if score_mgr.is_high_score:
            banner_text = "★ NEW HIGH SCORE! ★"
            banner_color = (255, 215, 0)  # Gol
            self.hide_entry_name(False)
        elif score_mgr.is_better:
            banner_text = f"★ TOP {score_mgr.get_rank()} QUALIFIED! ★"
            banner_color = (100, 230, 100)  # Vibrant green
            self.hide_entry_name(False)
        else:
            banner_text = self.scene.dead_state
            banner_color = (255, 20, 20)  # self.pixel.colors["title"]
            self.hide_entry_name()

        self.pixel.texts["GO_BANNER"] = banner_text
        b_surf = self.pixel.render_text(
            banner_text,
            size=int(15 * scale_x),
            color=banner_color,
            outline=(0, 0, 0),
            width=2,
        )
        self.banner_img.set_image(b_surf)
        self.banner_img.set_dimensions(b_surf.get_size())
        b_rect = b_surf.get_rect(center=(cx, cy - int(340 * scale_y)))
        self.banner_img.set_relative_position((b_rect.x, b_rect.y))

        # Status text update
        self._update_status_display(scale_x, cx, cy, scale_y)

    def _update_status_display(
        self, scale_x: float, cx: int, cy: int, scale_y: float
    ) -> None:
        score_mgr = getattr(self.scene, "score", None)
        current = score_mgr.score if score_mgr else 0

        if self.is_saved:
            status_text = "SCORE SAVED IN TOP 5!"
            status_color = (100, 230, 100)
        elif current <= 0:
            status_text = "NO POINTS SCORED"
            status_color = (180, 180, 180)
        elif score_mgr and not score_mgr.is_better:
            status_text = "RECORD NOT BEATEN"
            status_color = (200, 180, 140)
        else:
            status_text = "TYPE NAME & PRESS ENTER"
            status_color = (230, 230, 120)

        self.pixel.texts["GO_STATUS"] = status_text
        st_surf = self.pixel.render_text(
            status_text,
            size=int(12 * scale_x),
            color=status_color,
            outline=(0, 0, 0),
            width=2,
        )
        self.status_img.set_image(st_surf)
        self.status_img.set_dimensions(st_surf.get_size())
        name_section_y = cy + int(25 * scale_y)
        st_rect = st_surf.get_rect(center=(cx, name_section_y + int(95 * scale_y)))
        self.status_img.set_relative_position((st_rect.x, st_rect.y))

    def save_current_score(self) -> bool:
        """Saves current score using the text in the name entry line."""
        score_mgr = getattr(self.scene, "score", None)
        if not score_mgr or self.is_saved or score_mgr.score <= 0:
            return False

        name = self.name_entry.get_text().strip() or self.player_name
        self.player_name = name
        seed = getattr(self.scene, "seed", 0)

        saved = score_mgr.save_score(name=name, seed=seed)
        if saved:
            self.is_saved = True
            screen_rect = pg.Rect((0, 0), self.pixel.manager.window_resolution)
            self._update_status_display(
                screen_rect.width / 600.0,
                screen_rect.centerx,
                screen_rect.centery,
                screen_rect.height / 1000.0,
            )
            return True
        return False

    def update(self, dt: float) -> None:
        score_mgr = getattr(self.scene, "score", None)
        if score_mgr:
            current = score_mgr.score
            if current != self.last_score:
                self.refresh()

    def handle_event(self, event: pg.Event) -> str | None:
        if event.type == ui.UI_BUTTON_PRESSED:
            if event.ui_element is self.save_btn:
                self.save_current_score()
            elif event.ui_element is self.replay_btn:
                self.save_current_score()
                self.pixel.state_mgr.set(GameState.PLAY)
            elif event.ui_element is self.home_btn:
                self.save_current_score()
                self.pixel.state_mgr.set(GameState.MENU)
            elif event.ui_element is self.leaderboard_btn:
                self.save_current_score()
                self.pixel.state_mgr.set(GameState.LEADERBOARD)

        elif event.type == ui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element is self.name_entry:
                self.save_current_score()

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.save_current_score()
                self.pixel.state_mgr.set(GameState.MENU)
            elif event.key == pg.K_RETURN:
                if not self.is_saved and getattr(self.scene, "score", None):
                    self.save_current_score()

        return None
