# -*- coding: utf-8 -*-

# Python farm game

# Copyright (C) <2015> Markus Hackspacher

# This file is part of Python farm game.

# Python farm game is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Python farm game is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Python farm game.  If not, see <http://www.gnu.org/licenses/>.

import pygame
import base64
from unittest import TestCase
from farmlib.inventorywindow import InventoryWindow
from farmlib.imageloader import ImageLoader
from farmlib.gamemanager import GameManager
import farmlib

pygame.init()

w = 640
h = 480
screen_size = w, h

screen = pygame.display.set_mode(screen_size)


class TestInventoryWindow(TestCase):
    """
    Test Python3 base64.b64encode
    """

    def setUp(self):
        '''Creates the QApplication instance'''
        imagesdata = farmlib.images["imagesdata"]
        self.images = ImageLoader(imagesdata)
        self.gamemanager = GameManager()
        self.player = self.gamemanager.getplayer()
        self.inventor = InventoryWindow(self.images, self.player)

    def test_ismodified(self):
        """test ismodified

        :return:
        """
        self.inventor.lchecksum = b'ABC'
        self.assertEqual(self.inventor.ismodified(), True)
        print(self.player.inventory, bytes(self.player.inventory))
        print(self.player.itemscounter)
        print(bytes(str(self.player.itemscounter).encode()))
        base64.b64encode(bytes(self.player.inventory))

        checksum = base64.b64encode(bytes(self.player.inventory))
        print(checksum)
        checksum = base64.b64encode(
                checksum +
                bytes(str(self.player.itemscounter).encode()))
        self.inventor.lchecksum = checksum
        print(checksum)
        self.assertEqual(self.inventor.ismodified(), False)
        self.assertEqual(self.inventor.lchecksum, checksum)
        print(checksum)
