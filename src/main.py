import pygame as pg
from src.utils import log
from src.map.grid import Grid


class App:

    def __init__(self, w: int, h: int, title: str, fps: float = 60.0) -> None:
        # Init pygame
        pg.init()
        log.debug("Pygame INIT")

        # Init the screen
        self.screen_size = w, h
        self.screen = pg.display.set_mode((w, h))
        pg.display.set_caption(title)
        log.debug("Screen INIT")

        # Init the clock and fps
        self.clock = pg.time.Clock()
        self.fps = fps
        log.debug("Time INIT")

        # Other utils properties
        self.running = False

        log.info("App is correctly INIT")

    
    def on_init(self) -> None:
        self.running = True
        self.grid = Grid(self.screen_size)

    def on_update(self, dt: float) -> None:
        self.grid.on_update(dt)

    def on_draw(self, screen: pg.Surface) -> None:
        # Clean the buffer
        self.screen.fill((0,0,0))
        
        # Draw on the screen
        self.grid.on_draw(screen)

        # Render on the screen
        pg.display.flip()
    
    def on_events(self) -> bool:
        '''Return always True except for pg.QUIT'''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                self.running = False
                log.info("App is stoped")
                return False
            if not self.grid.on_events(event):
                pass
            
        return True
    
    def run(self) -> None:
        self.on_init()    
        # Start the loop
        while self.running:
            # Set the frame rate
            dt = self.clock.tick(self.fps) / 1000
            # Handle events
            if not self.on_events():
                continue
            # Update the App
            self.on_update(dt)
            # Draw on the buffer
            self.on_draw(self.screen)

        log.debug(self.grid.on_finish())
        log.info("Program return 0")
            
