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
        Container.__init__(self, (width, height), position)
        self.alphavalue = 196
        #border
        self.showborder = True
        self.bordercolor = (128, 128, 0)
        self.bordersize = 2
        self.backgroundcolor = (80, 80, 80, self.alphavalue)

    def create_background(self):
        img = pygame.surface.Surface(self.size).convert_alpha()
        img.fill(self.backgroundcolor)
        if self.showborder:
            pygame.draw.rect(img, self.bordercolor,
                             (0, 0, self.width, self.height),
                             self.bordersize)
        return img

    def repaint_container(self):
        self.create_widget_image()
        img = self.create_background()
        self.img.blit(img, (0, 0))

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
