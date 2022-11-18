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

import base64
import os
from unittest import skip, TestCase

import pygame

import farmlib
from farmlib.farm import objects
from farmlib.gamemanager import GameManager
from farmlib.imageloader import ImageLoader
from farmlib.inventorywindow import InventoryWindow

pygame.init()

w = 640
h = 480
screen_size = w, h

screen = pygame.display.set_mode(screen_size)
# Images data
imagesdata = farmlib.images["imagesdata"]

# merge objects images data (objects image have objects/objects+id.png)
for gobject in objects:
    name = "object" + str(gobject['id']) + ".png"
    objectsimagepath = os.path.join("images", os.path.join("objects", name))
    imagesdata["object" + str(gobject['id'])] = objectsimagepath


class TestInventoryWindow(TestCase):
    """
    Test Python3 base64.b64encode
    """

    def setUp(self):
        '''Creates the instance'''
        self.images = ImageLoader(imagesdata)
        self.gamemanager = GameManager()
        self.gamemanager.start_new_game()
        self.player = self.gamemanager.getplayer()
        self.inventor = InventoryWindow(self.images, self.player)

    @skip("different checksum")
    def test_ismodified(self):
        """test ismodified

        :return:
        """
        self.inventor.lchecksum = b'ABC'
        self.assertEqual(self.inventor.ismodified(), True)
        base64.b64encode(bytes(self.player.inventory))

        checksum = base64.b64encode(bytes(self.player.inventory))
        print(checksum)
        checksum = base64.b64encode(
                checksum +
                bytes(str(self.player.itemscounter).encode()))
        self.inventor.lchecksum = checksum
        self.assertEqual(self.inventor.ismodified(), False)
        self.assertEqual(self.inventor.lchecksum, checksum)

    def test_get_index_inventory_under_mouse(self):
        print(self.inventor.get_index_inventory_under_mouse())

    def test_create_gui(self):
        self.inventor.create_gui()

    def test_repaint(self):
        self.inventor.repaint()
