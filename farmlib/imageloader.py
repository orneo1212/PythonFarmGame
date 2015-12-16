import pygame


class ImageLoader(object):
    """Image Loader
    """

    def __init__(self, imagesdict):
        self.config = imagesdict
        self.loaded = {}
        self.empty = pygame.Surface((64, 32))

    def __getitem__(self, name):
        return self.loadimage(name)

    def loadimages(self):
        """Load all images"""
        for item in self.config.keys():
            self.loadimage(item)
        return self.loaded

    def loadimage(self, name, scale=True):
        """Load image by name"""
        # wrong name
        if name not in self.config:
            return self.empty.copy()
        # check loaded images
        if name in self.loaded:
            return self.loaded[name]

        # load file
        filename = self.config[name]
        try:
            # return scaled image
            img = pygame.image.load(filename)
            img.set_colorkey((255, 0, 255))
            img = img.convert_alpha()
        except Exception as e:
            print("Error: Exception in imageloader "
                  "Check your data!\nDetails: {0}".format(e))
            img = self.empty.copy()
        self.loaded[name] = img
        return img
