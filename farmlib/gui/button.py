import pygame

from widget import Widget

class Button(Widget):
    def __init__(self, label, position, bgimage = None, labelsize = 12,
                 color = (255, 255, 0)):
        self.bgimage = bgimage
        self.label = label
        self.color = color
        #self.image = image
        self.position = position
        self.labelsize = labelsize
        self.labelfont = pygame.font.Font("droidsansmono.ttf", self.labelsize)

        self.insidewidget = False

        #Setup image
        if not self.bgimage:
            self._settextimage()
        else:
            self._setsize(self._calculate_size(self.bgimage))
        Widget.__init__(self, self.position, (self.width, self.height))

    def _render_text(self):
        return self.labelfont.render(self.label, 0, self.color)

    def _calculate_size(self, image):
        width = image.get_size()[0]
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
            self._img.blit(img, (0, 0))
            self._img.blit(self.bgimage, (0, 0))
        elif not self.bgimage:
            self._img.blit(self.image, (0, 0))
        elif not self.label and self.bgimage:
            self._img.blit(self.bgimage, (0, 0))
        #draw rectangle on hover
        if self.insidewidget:
            pygame.draw.line(self._img, self.color, (1, self.height - 1),
                             (self.width, self.height - 1))

    def settext(self, newtext):
        self.label = newtext
        self._settextimage()
        self.repaint()

    def _call_callback(self, signal):
        if signal in self.callbacks:
            if self.callbacks[signal]:
                self.callbacks[signal][0](self, **self.callbacks[signal][1])

    def poll_event(self, event):
        pos = self.parent.get_relative_mousepos()

        #mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #on_click event
            if pos != None:
                if self.pointinwidget(pos[0], pos[1]):
                    self._call_callback("clicked")
                    #make button active
                    if self.parent:
                        self.parent.makeactive(self)

        #Mouse motion
        if event.type == pygame.MOUSEMOTION and pos:
            #on_enter event
            if not self.insidewidget and self.pointinwidget(pos[0], pos[1]):
                self.insidewidget = True
                self._call_callback("onenter")
                self.repaint()
            #on_leave event
            elif self.insidewidget and not self.pointinwidget(pos[0], pos[1]):
                self.insidewidget = False
                self._call_callback("onleave")
                self.repaint()
