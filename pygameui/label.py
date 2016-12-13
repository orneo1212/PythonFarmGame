from __future__ import absolute_import

import pygame

from pygameui.widget import Widget


class Label(Widget):
    """
    Label
    """
    def __init__(self, text, position, size=12,
                 color=(255, 255, 255), align="left"):
        self.text = text
        self.labelfont = pygame.font.Font("dejavusansmono.ttf", size)
        self.image = None
        self.color = color
        self.position = position
        self.orginal_position = position
        self.align = align

        # set width and height
        self.render_text()
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]
        self.setposition(self.position)
        Widget.__init__(self, self.position, self.width, self.height)

    def render_text(self):
        """render_text

        :return:
        """
        self.image = self.labelfont.render(self.text, 0, self.color)
        self.image = self.image.convert_alpha()
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]

    def setposition(self, position):
        """setposition

        :param position:
        :return:
        """
        if self.align == "center":
            position = position[0] - self.width / 2, position[1]
        if self.align == "right":
            position = position[0] - self.width, position[1]
        if self.align == "left":
            position = position[0], position[1]
        self.position = position

    def repaint(self):
        """repaint

        :return:
        """
        self.render_text()
        self.img = self.image
        self.mark_modified()

    def settext(self, newtext):
        """settext

        remove , repaint=True

        :param newtext:
        :param repaint:
        :return:
        """
        try:
            newtext = unicode(newtext)
        except NameError:
            newtext = str(newtext)
        self.text = newtext
        self.setposition(self.orginal_position)
        self.mark_modified()

    def gettext(self):
        """gettext

        :return:
        """
        return self.text
