'''
Created on 22-05-2012

@author: orneo1212
'''
import pygame
from widget import Widget

class Container(Widget):
    '''
    Container for gui
    '''


    def __init__(self, (width, height), position):
        Widget.__init__(self, position, (width, height))
        self.widgets = []
        self.visible = True
        #last active widget
        self._lastactivewidget = None

    def repaint(self):
        """Repaint internally"""
        self.repaint_container()
        self.repaint_widgets()
        #print ("repaint container", self)

    def repaint_container(self):
        self.create_widget_image()

    def repaint_widgets(self):
        for widget in self.widgets:
            if widget.visible:
                widget.repaint()
                widget.draw(self.img)

    def draw(self, surface):
        if not self.visible:return

        needrepaint = False
        for widget in self.widgets:
            if widget.modified:
                widget.mark_modified(False)
                needrepaint = True
                break
        #
        if needrepaint:self.repaint()
        surface.blit(self.img, self.position)

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
        widget.mark_modified()
        self.widgets.append(widget)

    def remove_all_widgets(self):
        self.widgets = []
