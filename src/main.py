import pygame as pg

from src.scene import Scene
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
        self.scene: Scene = Scene(self.screen_size)
        self.running = True
        log.debug("Game is INIT !")

    def on_update(self, dt: float) -> None:
        """Update the Game"""
        self.scene.update(dt)

    def on_draw(self, screen: pg.Surface) -> None:
        # Clean the buffer
        _ = self.screen.fill((0, 0, 0))
        self.scene.draw(screen)
        # Render on the screen
        pg.display.flip()

    def on_events(self) -> bool:
        """Return always True except for pg.QUIT"""
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                self.running = False
                log.info("Game is stoped")
                return False
        if self.scene.handle_events(events):
            return True

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
