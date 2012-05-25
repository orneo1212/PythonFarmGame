'''
Created on 22-05-2012

@author: orneo1212
'''
import pygame

class Window:
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

    def render(self, surface):
        if not self.visible:return
        img = pygame.surface.Surface((self.width, self.height))
        img.fill((80, 80, 80))
        pygame.draw.rect(img, (255, 255, 0), (0, 0, self.width, self.height), 1)
        for widget in self.widgets:
            widget.redraw(img)
        surface.blit(img, self.position)

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

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
