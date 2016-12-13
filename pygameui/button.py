from __future__ import absolute_import

import os
import pygame

from pygameui.widget import Widget

buttonbgpath = os.path.join("images", "gui", "buttonbg.png")


class Button(Widget):
    """Button Widget

    """
    def __init__(self, label, position, bgimage=None, labelsize=12,
                 color=(255, 255, 0)):
        self.bgimage = bgimage
        self.label = label
        self.color = color
        self.position = position
        self.labelsize = labelsize
        self.labelfont = pygame.font.Font("dejavusansmono.ttf", self.labelsize)
        self.buttonbgorg = pygame.image.load(buttonbgpath).convert_alpha()
        self.buttonbg = self.buttonbgorg.copy()
        # Setup image
        if not self.bgimage:
            self._settextimage()
        else:
            self._setsize(self._calculate_size(self.bgimage))
        Widget.__init__(self, self.position, self.width, self.height)

    def _render_text(self):
        """_render_text

        :return:
        """
        img = self.labelfont.render(self.label, 0, self.color)
        return img.convert_alpha()

    @staticmethod
    def _calculate_size(image):
        """_calculate_size

        :param image:
        :return:
        """
        width = image.get_size()[0] + 4
        height = image.get_size()[1]
        return (width, height)

    def _settextimage(self):
        """_set text image

        :return:
        """
        self.image = self._render_text()
        self._setsize(self._calculate_size(self.image))

    def setimage(self, newimage):
        """set image

        :param newimage:
        :return:
        """
        self.image = newimage
        self._setsize(self._calculate_size(self.image))
        self.repaint()

    def repaint(self):
        """repaint

        :return:
        """
        self.create_widget_image()
        if self.label and self.bgimage:
            img = self._render_text()
            self.img.blit(img, (2, 0))
            self.img.blit(self.bgimage, (0, 0))
        elif not self.bgimage:
            img = pygame.transform.smoothscale(self.buttonbgorg, self.size)
            self.buttonbg = img
            self.img.blit(self.buttonbg, (0, 0))
            self.img.blit(self.image, (2, 0))
        elif not self.label and self.bgimage:
            self.img.blit(self.bgimage, (0, 0))
        # draw rectangle on hover
        if self.insidewidget:
            pygame.draw.line(self.img, self.color, (1, self.height - 1),
                             (self.width, self.height - 1))
        # mark modified
        self.mark_modified()

    def settext(self, newtext):
        """settext

        :param newtext:
        :return:
        """
        self.label = newtext
        self._settextimage()
        self.repaint()

    def poll_event(self, event):
        """poll_event

        :param event:
        :return:
        """
        Widget.poll_event(self, event)
        pos = self.parent.get_relative_mousepos()

        # mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pos\
                and self.pointinwidget(pos[0], pos[1]):
            # on_click event
            self.call_callback("clicked")
            self.call_callback("onclick")
            # make button active
            if self.parent:
                self.parent.makeactive(self)
