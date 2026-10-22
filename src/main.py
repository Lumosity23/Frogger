import pygame as pg
from src.utils import log


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

    def on_update(self, dt: float) -> None:
        pass

    def on_draw(self, screen: pg.Surface) -> None:
        
        # ...

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

        log.info("Program return 0")
            
