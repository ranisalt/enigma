import string


class Steckerbrett:
    def __init__(self):
        pass


class Umkehrwalze:
    def __init__(self, wiring):
        self.wiring = wiring

    def encode(self, letter):
        return self.wiring[string.ascii_uppercase.index(letter)]


class Walzen:
    def __init__(self, notch, wiring):
        assert isinstance(notch, str)
        assert isinstance(wiring, str)
        assert len(wiring) == len(string.ascii_uppercase)

        self.notch = notch
        self.wiring = wiring

    def encode(self, letter):
        return self.wiring[string.ascii_uppercase.index(letter)]


class Enigma:
    def __init__(self):
        pass

    def cipher(self, message):
        pass