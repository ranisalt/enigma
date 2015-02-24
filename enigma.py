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

    def encode_reverse(self, letter):
        return string.ascii_uppercase[self.wiring.index(letter)]


class Enigma:
    def __init__(self, rotors, reflector):
        # Assert that rotors is a tuple and each tuple element is a Walzen
        assert isinstance(rotors, tuple)
        for index in range(len(rotors)):
            assert isinstance(rotors[index], Walzen)

        # Assert that reflector is an Umkehrwalze
        assert isinstance(reflector, Umkehrwalze)

        self.rotors = rotors
        self.reflector = reflector

    def cipher(self, message):
        pass