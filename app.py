# ui/app.py
"""Main application object: owns the pygame loop and screen stack."""
import pygame

from ui import colors, config


class App:
    """Owns the window, the clock and the current screen.

    Screens are swappable objects with `handle_event`, `update` and `draw`.
    For now we only have an empty placeholder screen.
    """

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption(config.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0  # seconds
            self._handle_events()
            self._update(dt)
            self._draw()

        pygame.quit()

    # ----------------------------------------------------- internal steps
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update(self, dt: float) -> None:
        # Future: tick the simulation engine here.
        pass

    def _draw(self) -> None:
        self.screen.fill(colors.BACKGROUND)
        pygame.display.flip()