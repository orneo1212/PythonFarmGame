'''
Created on 22-05-2012

@author: orneo1212
'''
import pygame

from container import Container

class Window(Container):
    '''
    Window for gui
    '''

    def __init__(self, (width, height), position):
        self.width = width
        self.height = height
        self.size = [self.width, self.height]
        self.widgets = []
        self.position = position
        self.visible = True
        self.alphavalue = 255
        #border
        self.showborder = True
        self.bordercolor = (128, 128, 0)
        self.bordersize = 2
        self.backgroundcolor = (80, 80, 80)

    def render(self):
        img = pygame.surface.Surface((self.width, self.height))
        img.set_alpha(self.alphavalue)
        img.fill(self.backgroundcolor)
        if self.showborder:
            pygame.draw.rect(img, self.bordercolor,
                             (0, 0, self.width, self.height), self.bordersize)
        #render widgets
        for widget in self.widgets:
            widget.redraw(img)
        return img

    def redraw(self, surface):
        if not self.visible:return
        img = self.render()
        surface.blit(img, self.position)

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
