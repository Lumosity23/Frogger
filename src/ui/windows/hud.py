import pygame as pg
from pygame.math import Vector2

from src.ui.windows.base import Window

# ==============================================================================
# PARAMÈTRES ET TAILLES PAR DÉFAUT DU HUD
# Vous pouvez modifier les valeurs ici pour ajuster la taille de vos éléments,
# ou passer ces arguments lors de l'instanciation de HudWindow (ex dans main.py).
# ==============================================================================
DEFAULT_SCALE: float = 1.0  # Échelle globale du HUD
DEFAULT_SCORE_SCALE: float = 3.0  # Échelle spécifique des chiffres du score
DEFAULT_TIME_SCALE: float = 2.0  # Échelle spécifique des chiffres du temps
DEFAULT_CLOCK_SCALE: float = 2.0
DEFAULT_LIVES_SCALE: float = 3.0  # Échelle spécifique des crêtes de vie (comb.png)
DEFAULT_LIVES_SPACING: int = 4  # Espace en pixels entre chaque crête séparée
DEFAULT_MARGIN: int = 20  # Marge en pixels depuis les bords de l'écran

DIGITS_PATH = "assets/big_digits.png"
TIME_DIGITS_PATH = "assets/tiny_digits.png"
COMB_PATH = "assets/comb.png"
DEAD_COMB_PATH = "assets/dead_comb.png"
CLOCK_PATH = "assets/assets_logo/clock.png"


def slice_spritesheet(path: str, n: int, scale: float = 1.0) -> dict[int, pg.Surface]:
    """Découpe une spritesheet horizontale en n frames (comme dans entity.py).

    w = image.width // n
    h = image.height
    """
    image = pg.image.load(path).convert_alpha()
    if scale != 1.0:
        new_size = (round(image.get_width() * scale), round(image.get_height() * scale))
        image = pg.transform.scale(image, new_size)
    w = image.get_width() // n
    h = image.get_height()
    return {x: image.subsurface(pg.Rect(x * w, 0, w, h)).copy() for x in range(n)}


class HudWindow(Window):
    """Fenêtre HUD pour le jeu, intégrée au système de fenêtres PixelUI.

    Disposition :
    - Temps affiché en haut à gauche avec les digits pixel-art
    - Score affiché en haut à droite avec les digits pixel-art
    - Vies affichées en bas à gauche : crêtes (comb.png) séparées côte à côte,
      avec dead_comb.png pour les crêtes utilisées / perdues.
    """

    name: str = "HUD"
    background_alpha: int = 0  # 0 = panneau complètement transparent

    def __init__(
        self,
        pixel,
        scene=None,
        scale: float = DEFAULT_SCALE,
        score_scale: float | None = None,
        time_scale: float | None = None,
        clock_scale: float | None = None,
        lives_scale: float | None = None,
        lives_spacing: int = DEFAULT_LIVES_SPACING,
        margin: int = DEFAULT_MARGIN,
        digit_path: str = DIGITS_PATH,
        time_digit_path: str | None = TIME_DIGITS_PATH,
        comb_path: str = COMB_PATH,
        dead_comb_path: str = DEAD_COMB_PATH,
        clock_path: str = CLOCK_PATH,
        max_lives: int = 5,
        time_format: str = "SS",
    ) -> None:
        self.scene = scene
        self.scale = scale
        # Échelles effectives (combinaison de scale globale * échelle spécifique)
        self.score_scale: float = (
            score_scale if score_scale is not None else DEFAULT_SCORE_SCALE
        ) * scale
        self.time_scale: float = (
            time_scale if time_scale is not None else DEFAULT_TIME_SCALE
        ) * scale
        self.clock_scale: float = (
            clock_scale if clock_scale is not None else DEFAULT_CLOCK_SCALE
        ) * scale
        self.lives_scale: float = (
            lives_scale if lives_scale is not None else DEFAULT_LIVES_SCALE
        ) * scale
        self.lives_spacing: int = lives_spacing
        self.margin_val: int = margin

        self.digit_path = digit_path
        self.time_digit_path = time_digit_path or digit_path
        self.comb_path = comb_path
        self.dead_comb_path = dead_comb_path
        self.clock_path = clock_path
        self.max_lives: int = max_lives
        self.time_format: str = time_format

        # Valeurs logiques
        self.score_val: int = 0
        self.lives_val: int = max_lives
        self.time_val: float = 0.0

        # Cache pour éviter les recalculs inutiles à chaque frame
        self._last_score: int | None = None
        self._last_lives_state: tuple[int, int] | None = None
        self._last_time_str: str | None = None

        super().__init__(pixel)

    def build(self) -> None:
        res = self.pixel.manager.window_resolution
        self.screen_w, self.screen_h = res[0], res[1]
        self.margin = max(5, round(self.margin_val * self.scale))

        # 1. Chiffres pour le score
        self.score_digits = slice_spritesheet(self.digit_path, 10, self.score_scale)

        # 2. Chiffres et séparateur ':' pour le temps
        self.time_digits = slice_spritesheet(self.time_digit_path, 10, self.time_scale)
        time_digit_h = self.time_digits[0].get_height()
        self.time_colon = self._create_colon_surface(time_digit_h, self.time_scale)
        self.clock = pg.image.load(self.clock_path).convert_alpha()
        clock_w, clock_h = Vector2(self.clock.get_size()) * self.clock_scale
        self.clock = pg.transform.scale(self.clock, (clock_w, clock_h))

        # 3. Crêtes de vie (actives et mortes) avec lives_scale
        comb_raw = pg.image.load(self.comb_path).convert_alpha()
        dead_raw = pg.image.load(self.dead_comb_path).convert_alpha()

        if self.lives_scale != 1.0:
            comb_w = round(comb_raw.get_width() * self.lives_scale)
            comb_h = round(comb_raw.get_height() * self.lives_scale)
            self.comb_img = pg.transform.scale(comb_raw, (comb_w, comb_h))
            self.dead_comb_img = pg.transform.scale(dead_raw, (comb_w, comb_h))
        else:
            self.comb_img = comb_raw
            self.dead_comb_img = dead_raw

        # Création des éléments d'image pygame_gui (surfaces factices initiales)
        dummy = pg.Surface((1, 1), pg.SRCALPHA)
        self.time_img = self.pixel.image(
            f"HUD_TIME_{self.name}",
            dummy,
            pg.Rect(self.margin, self.margin, 1, 1),
            container=self.panel,
        )
        self.clock_img = self.pixel.image(
            f"HUD_CLOCK_{self.name}",
            self.clock,
            pg.Rect(self.margin - 10, self.margin - 4, clock_w, clock_h),
            container=self.panel,
        )
        self.score_img = self.pixel.image(
            f"HUD_SCORE_{self.name}",
            dummy,
            pg.Rect(self.screen_w - self.margin - 1, self.margin, 1, 1),
            container=self.panel,
        )
        self.lives_img = self.pixel.image(
            f"HUD_LIVES_{self.name}",
            dummy,
            pg.Rect(self.margin, self.screen_h - self.margin - 1, 1, 1),
            container=self.panel,
        )

        # Premier rafraîchissement
        self.refresh()

    def _create_colon_surface(self, digit_h: int, scale: float) -> pg.Surface:
        """Génère le symbole ':' avec le même style rétro (blanc avec contour noir)."""
        w = max(4, round(10 * scale))
        h = digit_h
        surf = pg.Surface((w, h), pg.SRCALPHA)
        dot_size = max(2, round(4 * scale))
        cx = (w - dot_size) // 2
        y1 = round(h * 0.30)
        y2 = round(h * 0.65)
        for y in (y1, y2):
            pg.draw.rect(surf, (0, 0, 0), (cx - 1, y - 1, dot_size + 2, dot_size + 2))
            pg.draw.rect(surf, (255, 255, 255), (cx, y, dot_size, dot_size))
        return surf

    def _render_digits(
        self,
        text: str,
        digits: dict[int, pg.Surface],
        colon_surf: pg.Surface | None = None,
        scale: float = 1.0,
    ) -> pg.Surface:
        """Compose une surface contenant la suite de chiffres (et ':')."""
        spacing = max(1, round(2 * scale))
        surfaces: list[pg.Surface] = []
        for char in text:
            if char.isdigit():
                surfaces.append(digits[int(char)])
            elif char == ":" and colon_surf is not None:
                surfaces.append(colon_surf)

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

    def _render_lives(self, count: int, max_count: int) -> pg.Surface:
        """Affiche les crêtes séparées avec un espacement (comme sur le modèle).

        - Les crêtes actives (comb.png) sont affichées pour les vies restantes.
        - Les crêtes mortes (dead_comb.png) complètent jusqu'à max_count.
        - Chaque crête est séparée par self.lives_spacing pixels.
        """
        total_slots = max(count, max_count)
        if total_slots <= 0:
            return pg.Surface((1, 1), pg.SRCALPHA)

        cw, ch = self.comb_img.get_size()
        spacing = max(0, round(self.lives_spacing * self.scale))
        step_x = cw + spacing
        total_w = total_slots * cw + (total_slots - 1) * spacing
        res = pg.Surface((total_w, ch), pg.SRCALPHA)

        for i in range(total_slots):
            img = self.comb_img if i < count else self.dead_comb_img
            res.blit(img, (i * step_x, 0))

        return res

    def set_score(self, score: int) -> None:
        self.score_val = score

    def set_lives(self, lives: int, max_lives: int | None = None) -> None:
        self.lives_val = max(0, lives)
        if max_lives is not None:
            self.max_lives = max(0, max_lives)

    def set_time(self, time_val: float | int | str) -> None:
        self.time_val = time_val

    def update(self, dt: float) -> None:
        """Met à jour les données depuis Scene si elle est fournie, puis actualise le HUD."""
        if self.scene is not None:
            # Récupération du score
            self.score_val = f"{self.scene.score.score}"

            # Récupération des vies
            if hasattr(self.scene, "max_lives"):
                self.max_lives = self.scene.max_lives
            if hasattr(self.scene, "lives"):
                self.lives_val = self.scene.lives
            elif hasattr(self.scene, "round"):
                self.lives_val = self.scene.round

            # Récupération ou progression du temps
            if hasattr(self.scene, "time"):
                self.time_val = self.scene.time
            elif hasattr(self.scene, "timer"):
                self.time_val = self.scene.timer
            elif isinstance(self.time_val, (int, float)):
                self.time_val += dt
        elif isinstance(self.time_val, (int, float)):
            self.time_val += dt

        self.refresh()

    def refresh(self) -> None:
        """Met à jour les surfaces uniquement lorsque les valeurs changent."""
        # 1. Temps (en haut à gauche)
        if isinstance(self.time_val, (int, float)):
            secs = max(0, int(self.time_val))
            if self.time_format == "MM:SS":
                time_str = f"{secs // 60:02d}:{secs % 60:02d}"
            else:
                time_str = str(secs)
        else:
            time_str = str(self.time_val)

        if time_str != self._last_time_str:
            self._last_time_str = time_str
            t_surf = self._render_digits(
                time_str, self.time_digits, self.time_colon, self.time_scale
            )
            w, h = t_surf.get_size()
            self.time_img.set_image(t_surf)
            self.time_img.set_dimensions((w, h))
            self.time_img.set_relative_position(
                (self.margin + self.clock.width, self.margin)
            )

        # 2. Score (en haut à droite)
        if self.score_val != self._last_score:
            self._last_score = self.score_val
            s_surf = self._render_digits(
                str(self.score_val), self.score_digits, scale=self.score_scale
            )
            w, h = s_surf.get_size()
            self.score_img.set_image(s_surf)
            self.score_img.set_dimensions((w, h))
            self.score_img.set_relative_position(
                (self.screen_w - self.margin - w, self.margin)
            )

        # 3. Vies (en bas à gauche, crêtes actives + mortes séparées)
        lives_state = (self.lives_val, self.max_lives)
        if lives_state != self._last_lives_state:
            self._last_lives_state = lives_state
            l_surf = self._render_lives(self.lives_val, self.max_lives)
            w, h = l_surf.get_size()
            self.lives_img.set_image(l_surf)
            self.lives_img.set_dimensions((w, h))
            self.lives_img.set_relative_position(
                (self.margin, self.screen_h - self.margin - h)
            )
