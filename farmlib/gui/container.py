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
        self.create_widget_image()
        self.repaint_widgets()

    def repaint_widgets(self):
        for widget in self.widgets:
            if widget.visible:
                widget.redraw(self._img)

    def redraw(self, surface):
        if not self.visible:return

        #Repaint if any widget modified
        dorepaint = False
        for widget in self.widgets:
            if widget.modified:
                if not dorepaint:dorepaint = True
        if dorepaint:self.repaint()
        surface.blit(self._img, self.position)

    def update_size(self, newsize):
        self.width = newsize[0]
        self.height = newsize[1]
        self.size = newsize

    def hide(self):
        self.visible = False
        for widget in self.widgets:
            widget._call_callback("onleave")
            widget.hide()

    def show(self):
        self.repaint()
        self.visible = True
        for widget in self.widgets:
            widget.show()

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

    def create_widget_image(self):
        self._img = pygame.surface.Surface(self.size).convert_alpha()
        self._img.fill((255, 0, 255, 0))
        return self._img

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
        if widget.visible:
            widget.repaint()
        self.widgets.append(widget)

    def remove_all_widgets(self):
        self.widgets = []
