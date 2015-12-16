import json


class DictMapper(object):
    """DictMapper

    """
    def __init__(self, dicttomap=None):
        self._dict = dicttomap or {}

    def __str__(self):
        return repr(self._dict)

    def __iter__(self):
        return iter(self._dict.values())

    def __setitem__(self, name, value):
        self._dict[name] = value

    def keys(self):
        """keys

        :return:
        """
        return self._dict.keys()

    def get(self, keyname, defaultvalue):
        """get

        :param keyname:
        :param defaultvalue:
        :return:
        """
        if keyname in self._dict.keys():
            return self._dict[keyname]
        else:
            return defaultvalue

    def __getitem__(self, name):
        if isinstance(name, int):
            name = str(name)
        if name in self._dict:
            return self._dict[name]
        else:
            if name in self.__dict__:
                return self.__dict__[name]
            else:
                return None

    def save(self, filename):
        """save

        :param filename:
        :return:
        """
        json.dump(self._dict, open(filename, "w"), indent=2)

    def load(self, filename):
        """load

        :param filename:
        :return:
        """
        self._dict = json.load(open(filename, "r"))
