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
        self.modified = True
        self.insidewidget = False

        self.callbacks = {}  # key=signal name value= function
        #
        self.create_widget_image()

    def create_widget_image(self):
        self.img = pygame.surface.Surface(self.size)
        self.img = self.img.convert_alpha()
        self.img.fill((255, 0, 255, 0))
        return self.img

    def _setsize(self, newsize):
        self.width = newsize[0]
        self.height = newsize[1]
        self.size = newsize[:]

    def mark_modified(self, modified = True):
        self.modified = modified

    def repaint(self):
        """repaint internally"""
        pass

    def draw(self, surface):
        self.mark_modified(False)
        if self.img:
            surface.blit(self.img, self.position)

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
                self.repaint()
            #on_enter event
            if not self.insidewidget and self.pointinwidget(pos[0], pos[1]):
                self.insidewidget = True
                self._call_callback("onenter")
                self.repaint()

    def togglevisible(self):
        if self.visible:
            self.hide()
        else:
            self.show()

    def hide(self):
        self.visible = False
        self.active = False
        self._call_callback("onhide")

    def show(self):
        self.repaint()
        self.visible = True
        self._call_callback("onshow")

    def pointinwidget(self, posx, posy):
        rect = pygame.Rect(self.position[0] + 2, self.position[1] + 2,
                           self.width - 2, self.height - 2)
        if rect.collidepoint((posx, posy)):
            return True
        else:return False

    def connect(self, signal, function, **data):
        self.callbacks[signal] = [function, data]

    def _call_callback(self, signal):
        """Call internal callback connected to widget and repaint"""
        if signal in self.callbacks:
            if self.callbacks[signal]:
                self.callbacks[signal][0](self, **self.callbacks[signal][1])
                self.repaint()
