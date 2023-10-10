from pygame import init, WINDOWCLOSE
from pygame.display import set_mode as display_set_mode, update as display_update
from pygame.time import Clock
from pygame.event import get as get_event
from pygame.transform import scale 

from const import SCREEN_SIZE, FRAMERATE, STANDARD_FRAMERATE
from serializer import Serializer
from plugin_loader import PluginLoader
from engine import Engine
from game import Game
from interpreter import Interpreter

class Main:
    def __init__(self):
        init()
        self.screen = display_set_mode(SCREEN_SIZE)
        self.is_running = True
        self.dt = 1
        self.clock = Clock()

        self.serializer = Serializer()
        self.plugin_loader = PluginLoader()
        self.interpreter = Interpreter()
        self.game = Game()
        self.engine = Engine()

        self.bot1 = self.plugin_loader.load("example_bot1.py")
        self.bot2 = self.plugin_loader.load("example_bot1.py")

        self.plugin_loader.run(self.bot1)
        self.plugin_loader.run(self.bot2)

        while self.is_running:
            self.check_events()
            self.check_keys()
            self.game.update(
                self.interpreter.get_action(self.plugin_loader.tick(self.bot1)),
                self.interpreter.get_action(self.plugin_loader.tick(self.bot2))
            )
            self.screen_update()

    def check_keys(self):
        pass

    def check_events(self):
        for e in get_event():
            if e.type == WINDOWCLOSE:
                self.is_running = False

    def screen_update(self):
        self.dt = self.clock.tick(FRAMERATE) * STANDARD_FRAMERATE / 1000
        self.screen.blit(scale(self.engine.render(self.game), SCREEN_SIZE), (0, 0))
        display_update()


if __name__ == "__main__":
    Main()
