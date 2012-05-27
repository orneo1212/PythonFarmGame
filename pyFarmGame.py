#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import pygame

from farmlib import __VERSION__
from farmlib.gamewindow import GameWindow

pygame.init()
pygame.key.set_repeat(100, 100)

class FarmGamePygame:
    def __init__(self):
        """Init game"""
        self.screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)
        pygame.display.set_caption("PyFarmGame " + "v. " + __VERSION__)
        #timer
        self.timer = pygame.time.Clock()
        #
        self.activescr = GameWindow()

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
        except:
            import traceback
            traceback.print_exc()
            self.remove_game_lock()
            exit(1)

    def check_game_lock(self):
        if os.path.isfile("game.lock"):
            raise Exception("Game is already running. If not manualy"\
                " remove game.lock file and try again")
            exit()
        else:
            open("game.lock", "w").close()

    def remove_game_lock(self):
        if os.path.isfile("game.lock"):
            os.remove("game.lock")

    def main(self):
        """Main"""
        #check for lock file
        self.check_game_lock()

        player = self.activescr.player

        #Load game
        result = self.activescr.farm.load_farmfield('field.json', player)
        if not result:
            self.start_new_game()
            print "No save game found. Starting new one"

        self.activescr.regenerate_groups()

        while self.activescr.running:
            self.events()
            self.update()
            self.redraw(self.screen)
            self.timer.tick(30)

        #Save game
        self.activescr.farm.save_farmfield('field.json', player)
        #remove lock
        self.remove_game_lock()

if __name__ == '__main__':
    f = FarmGamePygame()
    f.run()

