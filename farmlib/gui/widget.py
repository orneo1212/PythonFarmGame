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
        self.callbacks = {}  # key=signal name value= function
        #
        self._img = pygame.surface.Surface(self.size)
        self.repaint()

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

    def connect(self, signal, function, **data):
        self.callbacks[signal] = [function, data]
