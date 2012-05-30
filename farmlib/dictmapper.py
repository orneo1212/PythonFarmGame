import json

class DictMapper():
    def __init__(self, dicttomap = {}):
        self._dict = dicttomap

    def __str__(self):
        return repr(self._dict)

    def __iter__(self):
        return iter(self._dict.values())

    def __setitem__(self, name, value):
        self._dict[name] = value

    def keys(self):
        return self._dict.keys()

    def get(self, keyname, defaultvalue):
        if keyname in self._dict.keys():
            return self._dict[keyname]
        else:return defaultvalue

    def __getitem__(self, name):
        if isinstance(name, int):
            name = str(name)
        if name in self._dict:
            return self._dict[name]
        else:
            try:
                return self.__dict__[name]
            except:return None

    def save(self, filename):
        json.dump(self._dict, open(filename, "w"), indent = 2)

    def load(self, filename):
        self._dict = json.load(open(filename, "r"))
