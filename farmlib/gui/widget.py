'''
Created on 22-05-2012

@author: orneo1212
'''
import pygame

class Widget:
    '''
    Widget for gui
    '''


    def __init__(self, position, (width, height)):
        #parent widget should inherit from Container
        self.parent = None

        self.position = position
        self.width = width
        self.height = height
        self.size = [self.width, self.height]

        self.visible = True
        self.active = False
        self.callbacks = {}  # key=signal name value= function
        #
        self.create_widget_image()
        self.repaint()

    def create_widget_image(self):
        self._img = pygame.surface.Surface(self.size)
        self._img.set_colorkey((255, 0, 255))
        self._img.fill((255, 0, 255))
        return self._img

    def _setsize(self, newsize):
        self.width = newsize[0]
        self.height = newsize[1]
        self.size = newsize[:]

    def repaint(self):
        """repaint internally"""
        pass

    def redraw(self, surface):
        if self._img:
            surface.blit(self._img, self.position)

    def update(self):
        pass

    def poll_event(self, event):
        pass

    def hide(self):
        self.visible = False

    def show(self):
        self.repaint()
        self.visible = True

    def pointinwidget(self, posx, posy):
        rect = pygame.Rect(self.position[0], self.position[1],
                           self.width, self.height)
        if rect.collidepoint((posx, posy)):
            return True
        else:return False

    def connect(self, signal, function, **data):
        self.callbacks[signal] = [function, data]
