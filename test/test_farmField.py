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

from unittest import TestCase
import os
import pygame
import farmlib
from farmlib.imageloader import ImageLoader
from farmlib.gamemanager import GameManager
from farmlib.inventorywindow import InventoryWindow
from farmlib.farm import FarmField, FarmObject

pygame.init()

w = 640
h = 480
screen_size = w, h

screen = pygame.display.set_mode(screen_size)


class TestFarmField(TestCase):
    """
    Test Class Farmfield

    """
    def setUp(self):
        '''Creates the instance'''
        imagesdata = farmlib.images["imagesdata"]
        self.images = ImageLoader(imagesdata)
        self.gamemanager = GameManager()
        self.farm = FarmField(self.gamemanager)

    def test_get_farm_checksum(self):
        """get farm checksum

        :return:
        """
        self.assertEqual(self.farm.get_farm_checksum(), b'')
        self.test_set_farmtile()
        self.assertEqual(
            self.farm.get_farm_checksum(),
            b'MC4wPEZhcm1PYmplY3Q6IGlkOjgsIG5hbWU6V2lsdGVkIHBsYW50LCB0eXBlOj4='
        )

    def test_set_farmtile(self):
        """set a farmtile

        :return:
        """
        self.assertEqual(self.farm.farmtiles, {})
        print_farm = self.farm.get_farmtile(1, 1)
        self.assertEqual(print_farm.posx, -1)
        self.assertEqual(print_farm.posy, -1)
        self.farm.wilt_plant(1, 1)
        self.assertEqual(self.farm.farmtiles['1x1'].farmobject.id, 8)

    def test_create_anthill(self):
        """create a anthill

        :return:
        """
        objects = farmlib.DictMapper()
        objects.load(os.path.join("data", "objects.json"))
        fobject = FarmObject()
        fobject.id = 2
        fobject.apply_dict(objects[fobject.id])
        # self.farm.plant(2, 2, fobject)
        self.farm.set_farmobject(3, 2, fobject)
        self.farm.set_farmobject(3, 3, self.farm.create_anthill())
        self.assertEqual(self.farm.get_farmobject(3, 3).name, 'Anthill')
        self.assertEqual(self.farm.get_farmobject(3, 2).name, 'Bean')
        self.farm.update()
        print(self.farm.farmtiles)

    def test_update(self):
        """update sequenze

        :return:
        """
        objects = farmlib.DictMapper()
        objects.load(os.path.join("data", "objects.json"))
        for x in range(12):
            fobject = FarmObject()
            fobject.id = x
            fobject.apply_dict(objects[fobject.id])
            self.farm.set_farmobject(1, x, fobject)
        self.farm.update()
        self.assertEqual(self.farm.get_farmobject(1, 2).name, 'Bean')

    def test_check_wilted(self):
        """check wilted, class farmlib.farm.FarmTile test

        :return:
        """
        self.farm.set_farmobject(3, 3, self.farm.create_anthill())
        self.farm.plant(3, 3, self.farm.create_anthill())
        self.assertEqual(str(type(self.farm.farmtiles['3x3'])),
                         "<class 'farmlib.farm.FarmTile'>")
        self.farm.check_wilted(self.farm.farmtiles['3x3'])

    def test_generate_random_stones(self):
        """check generate random stones more than 6 ans less then 16

        :return:
        """
        self.farm.generate_random_stones()
        self.assertTrue(self.farm.count_objects(6) > 6)
        self.assertTrue(self.farm.count_objects(6) < 16)
