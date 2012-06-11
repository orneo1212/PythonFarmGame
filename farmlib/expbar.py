'''
Created on 31-05-2012

@author: orneo1212
'''
import pygame

from pygameui import Label

class ExpBar(Label):
    def __init__(self, player):
        self.player = player
        self.oldexp = -1.0
        Label.__init__(self, "", (9, 58))

    def update_text(self):
        #get data
        exp = self.player.exp
        nextlvlexp = self.player.nextlvlexp
        level = self.player.level
        self.oldexp = self.player.exp
        #calculate progress and set text
        progress = int(exp / nextlvlexp * 100)
        self.settext("Level: " + str(level) + " Exp: %s/%s (%s %%)" % \
                     (int(exp), int(nextlvlexp), progress), repaint = False)

    def update(self):
        if self.oldexp != self.player.exp:
            self.repaint()

    def repaint(self):
        self.update_text()

        self.size = self.width, self.height = ((48 + 2) * 6 - 1, 16)
        self.create_widget_image()
        #draw background
        pygame.draw.rect(self.img, (0, 32, 0),
                         (1, 1, self.width - 1 , self.height - 1))
        #draw background (progress)
        progresswidth = self.width / self.player.nextlvlexp * self.player.exp
        pygame.draw.rect(self.img, (0, 100, 0),
                         (1, 1, int(progresswidth) - 1 , self.height - 1))
        #draw border
        pygame.draw.rect(self.img, (0, 255, 0),
                         (1, 1, self.width - 1 , self.height - 1), 1)
        #draw text
        text = self.gettext()
        txtimg = self.labelfont.render(text, 0, (64, 255, 100), (255, 0, 255))
        txtimg.set_colorkey((255, 0, 255))

        #Draw centered
        px = self.width / 2 - txtimg.get_size()[0] / 2
        py = self.height / 2 - txtimg.get_size()[1] / 2
        self.img.blit(txtimg, (px, py))

    def redraw(self, surface):
        surface.blit(self.img, self.position)
