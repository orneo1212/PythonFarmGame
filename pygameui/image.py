from __future__ import absolute_import

from pygameui.widget import Widget


class Image(Widget):
    """
    Image
    """
    def __init__(self, image, position):
        self.image = image
        self.position = position

        # set width and height
        if self.image:
            self.width = self.image.get_size()[0]
            self.height = self.image.get_size()[1]
        else:
            self._setsize((0, 0))
        Widget.__init__(self, self.position, self.width, self.height)

    def setimage(self, newimage):
        """setimage

        :param newimage:
        :return:
        """
        self.image = newimage
        self.repaint()

    def repaint(self):
        """repaint

        :return:
        """
        self.mark_modified()
        self.img = self.image
