'''
Created on 22-05-2012

@author: orneo1212
'''
import pygame

class Container:
    '''
    Container for gui
    '''


    def __init__(self, (width, height), position):
        self.width = width
        self.height = height
        self.size = [self.width, self.height]
        self.widgets = []
        self.position = position
        self.visible = True

    def repaint(self):
        """Repaint internally"""
        pass

    def redraw(self, surface):
        if not self.visible:return
        for widget in self.widgets:
            if widget.visible:
                widget.redraw(surface)


    def hide(self):
        self.visible = False

    def show(self):
        self.repaint()
        self.visible = True

    def togglevisible(self):
        if self.visible:
            self.hide()
        else:
            self.show()

    def makeactive(self, widget = None):
        for widg in self.widgets:
            if widget and widg == widget:
                widg.active = True
            else:
                widg.active = False
            #Repaint
            widg.repaint()

    def update(self):
        for widget in self.widgets:
            widget.update()

    def poll_event(self, event):
        if not self.visible:return
        for widget in self.widgets:
            if not widget.visible:
                continue
            widget.poll_event(event)

    def get_relative_mousepos(self):
        """
            Return mouse position relative to window position and size
            return None when mouse is not under window
        """
        mx, my = pygame.mouse.get_pos()
        mx -= self.position[0]
        my -= self.position[1]
        if mx > self.width or my > self.height:return None
        return (mx, my)

    def addwidget(self , widget):
        widget.parent = self
        self.widgets.append(widget)
