import pygame as pg

from src.entities.chicken import Chicken
from src.map.grid import Grid
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
        self.grid: Grid = Grid(self.screen_size, scale=self.scale, mode="PROD")
        self.chicken = Chicken(self.screen_size[0] / 2, self.screen_size[1] / 2, self.grid.cell_size)

        self.running = True
        log.debug("Game is Launch !")

    def on_update(self) -> None:
        self.grid.on_update()

    def on_draw(self, screen: pg.Surface) -> None:
        # Clean the buffer
        _ = self.screen.fill((0, 0, 0))

        self.grid.on_draw(screen)
        self.chicken.draw(screen)

        # Render on the screen
        pg.display.flip()

    def on_events(self) -> bool:
        """Return always True except for pg.QUIT"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                self.running = False
                log.info("Game is stoped")
                return False
            if not self.chicken.process_event():
                pass
            if not self.grid.on_events():
                pass


        return True

    def run(self) -> None:
        self.on_init()
        while self.running:
            _ = self.clock.tick(self.fps) / 1000  # futur dt

            if not self.on_events():
                continue
            self.on_update()
            self.on_draw(self.screen)

        log.debug(self.grid.on_finish())
        log.info("App is correctly closed")
