import pygame as pg

from src.scene import Scene
from src.state import GameState, StateManager
from src.ui.pixelUI import PixelUI
from src.ui.windows.game_over import GameOverWindow
from src.ui.windows.hud import HudWindow
from src.ui.windows.leaderboard import LeaderboardWindow
from src.ui.windows.menu import MenuWindow
from src.ui.windows.pause import PauseWindow
from src.utils import log


class App:
    def __init__(
        self, w: int, h: int, title: str, fps: float = 60.0, scale: float = 1.0
    ) -> None:

        _ = pg.init()
        log.debug("Pygame INIT")

        self.screen_size: tuple[int, int] = int(w * scale), int(h * scale)
        self.screen: pg.Surface = pg.display.set_mode(self.screen_size)
        pg.display.set_caption(title)
        log.debug("Screen INIT")

        self.clock: pg.Clock = pg.time.Clock()
        self.fps: float = fps
        log.debug("Time INIT")

        # Other utils properties
        self.running: bool = False
        self.scale: float = scale

        log.info("App is correctly INIT")

    def on_init(self) -> None:
        # creation des manager
        self.state_mgr = StateManager(GameState.MENU)
        self.scene: Scene = Scene(self.screen_size, self.state_mgr, self.scale)
        self.pixel: PixelUI = PixelUI(self.screen, self.state_mgr)

        # Creation et ajout des fentre du jeu
        self.pixel.add_window(MenuWindow(self.pixel))
        self.pixel.add_window(HudWindow(self.pixel, scene=self.scene, scale=self.scale))
        self.pixel.add_window(PauseWindow(self.pixel))
        self.pixel.add_window(GameOverWindow(self.pixel, scene=self.scene))
        self.pixel.add_window(LeaderboardWindow(self.pixel, scene=self.scene))

        # Lancement du jeu
        self.pixel.open("MENU")
        self.running = True
        log.debug("App is INIT !")

    def on_update(self, dt: float) -> None:
        """Update the Game"""
        self.scene.update(dt)
        self.pixel.update(dt)

    def on_draw(self, screen: pg.Surface) -> None:
        # Clean the buffer
        _ = self.screen.fill((0, 0, 0))

        # Draw on screen
        self.scene.draw(screen)
        self.pixel.draw(screen)

        # Render on the screen
        pg.display.flip()

    def on_events(self) -> bool:
        """Return always True except for pg.QUIT"""
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                self.running = False
                log.info("App is stoped")
                return False

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                if self.state_mgr.current == GameState.PLAY:
                    self.state_mgr.set(GameState.PAUSE)
                    continue
                elif self.state_mgr.current == GameState.PAUSE:
                    self.state_mgr.set(GameState.PLAY)
                    continue
                elif self.state_mgr.current in (
                    GameState.LEADERBOARD,
                    GameState.GAME_OVER,
                ):
                    self.state_mgr.set(GameState.MENU)
                    continue

            if not self.pixel.handle_event(event):
                _ = self.scene.handle_events(event)

        return True

    def run(self) -> None:
        self.on_init()
        while self.running:
            dt = self.clock.tick(self.fps) / 1000
            if not self.on_events():
                continue
            self.on_update(dt)
            self.on_draw(self.screen)

        # log.debug(self.grid.on_finish())
        log.info("App is correctly closed")
