import pygame as pg

from src.map.grid import Grid
from src.utils import log


class App:
    def __init__(self, w: int, h: int, title: str, fps: float = 60.0) -> None:
        # Init pygame
        _ = pg.init()
        log.debug("Pygame INIT")

        # Init the screen
        self.screen_size: tuple[int, int] = w, h
        self.screen: pg.Surface = pg.display.set_mode((w, h))
        pg.display.set_caption(title)
        log.debug("Screen INIT")

        # Init the clock and fps
        self.clock: pg.Clock = pg.time.Clock()
        self.fps: float = fps
        log.debug("Time INIT")

        # Other utils properties
        self.running: bool = False
        self.grid: Grid = Grid(self.screen_size)

        log.info("App is correctly INIT")

    def on_init(self) -> None:
        self.running = True

    def on_update(self) -> None:
        self.grid.on_update()

    def on_draw(self, screen: pg.Surface) -> None:
        # Clean the buffer
        _ = self.screen.fill((0, 0, 0))

        # Draw on the screen
        self.grid.on_draw(screen)

        # Render on the screen
        pg.display.flip()

    def on_events(self) -> bool:
        """Return always True except for pg.QUIT"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                self.running = False
                log.info("App is stoped")
                return False
            if not self.grid.on_events():
                pass

        return True

    def run(self) -> None:
        self.on_init()
        # Start the loop
        while self.running:
            # Set the frame rate
            _ = self.clock.tick(self.fps) / 1000  # futur dt
            # Handle events
            if not self.on_events():
                continue
            # Update the App
            self.on_update()
            # Draw on the buffer
            self.on_draw(self.screen)

        log.debug(self.grid.on_finish())
        log.info("Program return 0")
