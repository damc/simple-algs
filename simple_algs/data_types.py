class Int:
    def __init__(self, data=0):
        self.data = data

    def type(self, digit: int):
        self.data = self.data * 10 + digit

    def reset(self):
        self.data = 0

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self)


class Str:
    def __init__(self, data=''):
        self.data = data

    def type(self, character):
        self.data += character

    def reset(self):
        self.data = ''

    def __str__(self):
        return self.data

    def __repr__(self):
        return str(self)
