'''
Created on 31-05-2012

@author: orneo1212
'''
from farmlib.gui import Container, Label

class Tooltip(Container):
    def __init__(self, position, data):
        """
            create tooltip window. data must be list of pairs ["label", "value"]
        """
        Container.__init__(self, (100, 100), position)
        self.position = position
        self.data = data

    def crete_widgets(self):
        rowid = 0
        for data in self.data:
            if len(data) < 2:continue
            label = Label(data[0], 10, rowid * 20)
            self.addwidget(label)
            value = Label(data[1], 10 + label.size[0], rowid * 20)
            self.addwidget(value)
            #increase row
            rowid += 1
