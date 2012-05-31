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
        self.insidewidget = False

        self.callbacks = {}  # key=signal name value= function
        #
        self.create_widget_image()

    def create_widget_image(self):
        self._img = pygame.surface.Surface(self.size)
        self._img = self._img.convert_alpha()
        self._img.fill((255, 0, 255, 0))
        return self._img

    def _setsize(self, newsize):
        self.width = newsize[0]
        self.height = newsize[1]
        self.size = newsize[:]

    def repaint(self):
        """repaint internally"""
        pass

    def parent_repaint(self):
        if self.parent:self.parent.repaint()

    def redraw(self, surface):
        if self._img:
            surface.blit(self._img, self.position)

    def update(self):
        pass

    def poll_event(self, event):
        #Mouse motion
        if event.type == pygame.MOUSEMOTION:
            pos = (0, 0)
            #get relative mouse pos if there is parent container
            if self.parent:
                newpos = self.parent.get_relative_mousepos()
                if newpos:pos = newpos
            #on_leave event
            if self.insidewidget and not self.pointinwidget(pos[0], pos[1]):
                self.insidewidget = False
                self._call_callback("onleave")
                self.parent_repaint()
            #on_enter event
            if not self.insidewidget and self.pointinwidget(pos[0], pos[1]):
                self.insidewidget = True
                self._call_callback("onenter")
                self.parent_repaint()

    def hide(self):
        self.visible = False

    def show(self):
        self.needrepaint = True
        self.visible = True

    def pointinwidget(self, posx, posy):
        rect = pygame.Rect(self.position[0] + 2, self.position[1] + 2,
                           self.width - 2, self.height - 2)
        if rect.collidepoint((posx, posy)):
            return True
        else:return False

    def connect(self, signal, function, **data):
        self.callbacks[signal] = [function, data]

    def _call_callback(self, signal):
        if signal in self.callbacks:
            if self.callbacks[signal]:
                self.callbacks[signal][0](self, **self.callbacks[signal][1])
