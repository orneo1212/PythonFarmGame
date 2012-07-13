import os
import pygame

from widget import Widget

buttonbgpath = os.path.join("images", "gui", "buttonbg.png")

class Button(Widget):
    def __init__(self, label, position, bgimage = None, labelsize = 12,
                 color = (255, 255, 0)):
        self.bgimage = bgimage
        self.label = label
        self.color = color
        self.position = position
        self.labelsize = labelsize
        self.labelfont = pygame.font.Font("dejavusansmono.ttf", self.labelsize)
        self.buttonbg = pygame.image.load(buttonbgpath).convert_alpha()

        #Setup image
        if not self.bgimage:
            self._settextimage()
        else:
            self._setsize(self._calculate_size(self.bgimage))
        Widget.__init__(self, self.position, (self.width, self.height))

    def _render_text(self):
        img = self.labelfont.render(self.label, 0, self.color)
        return img.convert_alpha()

    def _calculate_size(self, image):
        width = image.get_size()[0] + 4
        height = image.get_size()[1]
        return (width, height)

    def _settextimage(self):
        self.image = self._render_text()
        self._setsize(self._calculate_size(self.image))


    def setimage(self, newimage):
        self.image = newimage
        self._setsize(self._calculate_size(self.image))
        self.repaint()

    def repaint(self):
        self.create_widget_image()
        if self.label and self.bgimage:
            img = self._render_text()
            self.img.blit(img, (2, 0))
            self.img.blit(self.bgimage, (0, 0))
        elif not self.bgimage:
            self.img.blit(self.buttonbg, (0, 0))
            self.img.blit(self.image, (2, 0))
        elif not self.label and self.bgimage:
            self.img.blit(self.bgimage, (0, 0))
        #draw rectangle on hover
        if self.insidewidget:
            pygame.draw.line(self.img, self.color, (1, self.height - 1),
                             (self.width, self.height - 1))
        #mark modified
        self.mark_modified()

    def settext(self, newtext):
        self.label = newtext
        self._settextimage()
        self.repaint()

    def poll_event(self, event):
        Widget.poll_event(self, event)
        pos = self.parent.get_relative_mousepos()

        #mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #on_click event
            if pos != None:
                if self.pointinwidget(pos[0], pos[1]):
                    self._call_callback("clicked") # old
                    self._call_callback("onclick") # old
                    #make button active
                    if self.parent:
                        self.parent.makeactive(self)
