#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import pygame

from farmlib import __VERSION__
from farmlib import PluginSystem
from farmlib.menuwindow import MenuWindow

pygame.init()
pygame.key.set_repeat(100, 100)

class FarmGamePygame:
    def __init__(self):
        """Init game"""
        self.screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)
        pygame.display.set_caption("PyFarmGame " + "v. " + __VERSION__)
        #timer
        self.timer = pygame.time.Clock()

        self.activescr = None

        self.ingame = False
        self.inmenu = True

    def set_active_screen(self, activescreen):
        self.activescr = activescreen
        self.activescr.parent = self

    def update(self):
        self.activescr.update()

    def events(self):
        self.activescr.events()

    def redraw(self, surface):
        self.activescr.redraw(surface)


    def run(self):
        """
            Run game. Remove lock when error
        """
        try:
            self.main()
        except Exception:
            import traceback
            traceback.print_exc()
            self.remove_game_lock()
            exit(1)

    def check_game_lock(self):
        if os.path.isfile("game.lock"):
            print("Game is already running. If not manualy"\
                " remove game.lock file and try again")
            exit(0)
        else:
            open("game.lock", "w").close()

    def remove_game_lock(self):
        if os.path.isfile("game.lock"):
            os.remove("game.lock")

    def main(self):
        """Main"""
        #check for lock file
        self.check_game_lock()

        #IN GAME
        if self.ingame:
            self.activescr.init()
        elif not self.ingame and self.inmenu:
            pass

        while self.activescr.running:
            self.events()
            self.update()
            self.redraw(self.screen)
            PluginSystem.run()
            self.timer.tick(30)
            pygame.display.flip()

        #Save game
        if self.ingame:
            self.activescr.deinit()

        #remove lock
        self.remove_game_lock()

if __name__ == '__main__':
    f = FarmGamePygame()
    f.set_active_screen(MenuWindow())
    f.run()

