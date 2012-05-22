import pygame

from widget import Widget

class Label(Widget):
    def __init__(self, text, position, size = 12,
            color = (255, 255, 255), align = "left"):
        self.labelfont = pygame.font.Font("droidsansmono.ttf", size)
        self.image = self.labelfont.render(text, 1, color)

        width = self.image.get_size()[0]
        height = self.image.get_size()[1]
        if align == "center":
            position = position[0] - width / 2, position[1]

        Widget.__init__(self, (width, height))
        self.position = position

    def redraw(self, surface):
        surface.blit(self.image, self.position)
