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

import unittest
import pep8


class TestCodeFormat(unittest.TestCase):

    def test_pep8_conformance(self):
        """Test that we conform to PEP8."""
        pep8style = pep8.StyleGuide(quiet=False)
        result = pep8style.check_files(['pyFarmGame.py',
                                        'test/test_pep8.py',
                                        'farmlib/__init__.py',
                                        'farmlib/coreplugin.py',
                                        'farmlib/dictmapper.py',
                                        'farmlib/expbar.py',
                                        'farmlib/farm.py',
                                        'farmlib/gamemanager.py',
                                        'farmlib/gamewindow.py',
                                        'farmlib/helpwindow.py',
                                        'farmlib/imageloader.py',
                                        'farmlib/inventorywindow.py',
                                        'farmlib/marketwindow.py',
                                        'farmlib/menuwindow.py',
                                        'farmlib/player.py',
                                        'farmlib/pluginsystem.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_pygameui(self):
        """Test that we conform to PEP8."""
        pep8style = pep8.StyleGuide(quiet=False)
        result = pep8style.check_files(['pygameui/__init__.py',
                                        'pygameui/button.py',
                                        'pygameui/container.py',
                                        'pygameui/image.py',
                                        'pygameui/label.py',
                                        'pygameui/widget.py',
                                        'pygameui/window.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

if __name__ == '__main__':
    unittest.main()
