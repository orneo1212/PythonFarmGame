'''
Created on 31-05-2012

@author: orneo1212
'''
from pygameui import Label, Window

class Tooltip(Window):
    def __init__(self, position, data):
        """
            create tooltip window. data must be list of pairs ["label", "value"]
        """
        Window.__init__(self, (0, 0), position)
        self.data = data
        self.alphavalue = 200
        #
        self.crete_widgets()

    def crete_widgets(self):
        rowid = 0
        fontsize = 13
        spaceing = 4
        marginleft = 5
        for data in self.data:
            if len(data) < 2:continue

            #Label
            labelwidth = marginleft
            labelheight = rowid * (fontsize + 2)
            label = Label(data[0], (labelwidth, labelheight), size = fontsize)
            self.addwidget(label)

            #Value
            valuewidth = marginleft + label.size[0] + spaceing
            valueheight = rowid * (fontsize + 2)
            value = Label(data[1], (valuewidth, valueheight),
                           color = (255, 255, 150),
                           size = fontsize
                          )
            self.addwidget(value)
            #total width
            totalwidth = label.size[0] + value.size[0]
            if self.width < totalwidth:self.width = totalwidth + 5
            #increase row
            rowid += 1
        #update height
        totalheight = len(self.data) * (fontsize + 2)
        if self.height < totalheight:self.height = totalheight + 5
        #update window size
        self.size = [self.width, self.height]
