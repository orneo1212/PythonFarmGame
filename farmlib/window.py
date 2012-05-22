'''
Created on 22-05-2012

@author: orneo1212
'''
import pygame

class Window:
    '''
    Window for gui
    '''


    def __init__(self, (width, height)):
        self.width = width
        self.height = height
        self.size = [self.width, self.height]
        self.widgets = []
        self.visible = True

    def render(self, surface, position):
        if not self.visible:return
        img = pygame.surface.Surface((self.width, self.height))
        img.fill((80, 80, 80))
        pygame.draw.rect(img, (255, 255, 0), (0, 0, self.width, self.height), 1)
        for widget in self.widgets:
            widget.redraw(img)
        surface.blit(img, position)

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def update(self):
        for widget in self.widgets:
            widget.update()

    def poll_event(self, event):
        for widget in self.widgets:
            if not widget.visible:
                continue
            widget.poll_event(event)
