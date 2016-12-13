'''
Created on 22-05-2012

@author: orneo1212
'''
from __future__ import absolute_import

import pygame
from pygameui.widget import Widget


class Container(Widget):
    '''
    Container for gui
    '''

    def __init__(self, width, height, position):
        Widget.__init__(self, position, width, height)
        self.widgets = []
        self.visible = True
        # last active widget
        self._lastactivewidget = None

    def repaint(self):
        """Repaint internally"""
        self.repaint_container()
        self.repaint_widgets()

    def repaint_container(self):
        """repaint container

        :return:
        """
        self.create_widget_image()

    def repaint_widgets(self):
        """repaint widgets

        :return:
        """
        for widget in self.widgets:
            if widget.visible:
                widget.repaint()
                widget.draw(self.img)

    def draw(self, surface):
        """draw

        :param surface:
        :return:
        """
        if not self.visible:
            return

        needrepaint = False
        for widget in self.widgets:
            if widget.modified:
                widget.mark_modified(False)
                needrepaint = True
                break
        #
        if needrepaint:
            self.repaint()
        surface.blit(self.img, self.position)

    def update_size(self, newsize):
        """update size

        :param newsize:
        :return:
        """
        self.width = newsize[0]
        self.height = newsize[1]
        self.size = newsize

    def hide(self):
        """hide

        :return:
        """
        self.visible = False
        for widget in self.widgets:
            widget.call_callback("onleave")
            widget.hide()

    def show(self):
        """show

        :return:
        """
        self.repaint()
        self.visible = True
        for widget in self.widgets:
            widget.show()

    def makeactive(self, widget=None):
        """make active and repaint

        :param widget:
        :return:
        """
        for widg in self.widgets:
            if widget and widg == widget:
                widg.active = True
            else:
                widg.active = False
            # Repaint
            widg.repaint()

    def update(self):
        """update

        :return:
        """
        for widget in self.widgets:
            widget.update()

    def poll_event(self, event):
        """poll event

        :param event:
        :return:
        """
        if not self.visible:
            return
        for widget in self.widgets:
            if not widget.visible:
                continue
            widget.poll_event(event)

    def get_relative_mousepos(self):
        """Return mouse position relative to window position and size
        return None when mouse is not under window
        """
        mx, my = pygame.mouse.get_pos()
        mx -= self.position[0]
        my -= self.position[1]
        if mx > self.width or my > self.height:
            return None
        return (mx, my)

    def addwidget(self, widget):
        """add widget

        :param widget:
        :return:
        """
        widget.parent = self
        widget.mark_modified()
        self.widgets.append(widget)

    def remove_all_widgets(self):
        """remove all widgets

        :return:
        """
        self.widgets = []
