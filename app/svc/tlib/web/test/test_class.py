class BaseClass:
    words = 'abc'
    def __init__(self):
        pass

    def set_words(self, words):
        BaseClass.words = words

    def get_words(self):
        return BaseClass.words


class SubClass(BaseClass):
    def __init__(self, name):
        self._name = name
        super().__init__()

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name


if __name__ == '__main__':
    a = SubClass('a')
    b = SubClass('b')

    print("--before--")
    print("%s: %s" % (a.get_name(), a.get_words()))
    print("%s: %s" % (b.get_name(), b.get_words()))

    print("--end--")
    a.set_words('efg')
    a.set_name('c')
    b.set_name('d')

    print("%s: %s" % (a.get_name(), a.get_words()))
    print("%s: %s" % (b.get_name(), b.get_words()))
