from builtins import KeyError
import string


class Steckerbrett:
    def __init__(self, *args):
        self.map = {}

        for arg in args:
            if arg[0] in self.map or arg[1] in self.map:
                raise KeyError('Same letter used twice in plugboard')

            self.map[arg[0]] = arg[1]
            self.map[arg[1]] = arg[0]

    def swap(self, letter):
        if letter in self.map:
            return self.map[letter]
        return letter


class Umkehrwalze:
    def __init__(self, wiring):
        self.wiring = wiring

    def encode(self, letter):
        return self.wiring[string.ascii_uppercase.index(letter)]


class Walzen:
    def __init__(self, notch, wiring, setting='A', offset='A'):
        assert isinstance(notch, str)
        assert isinstance(wiring, str)
        assert len(wiring) == len(string.ascii_uppercase)

        self.notch = notch

        if isinstance(setting, str) and len(setting) == 1:
            self.setting = string.ascii_uppercase.index(setting)
        elif isinstance(setting, int) and 0 <= setting < len(wiring):
            self.setting = setting
        else:
            raise ValueError('setting must be character or integer')

        if isinstance(offset, str) and len(offset) == 1:
            self.offset = string.ascii_uppercase.index(offset)
        elif isinstance(offset, int) and 0 <= offset < len(wiring):
            self.offset = offset
        else:
            raise ValueError('offset must be character or integer')

        self.wiring = wiring

    def encode(self, letter):
        index = (string.ascii_uppercase.index(letter) - self.setting) % len(
            self.wiring)
        letter = self.wiring[index]

        index = (string.ascii_uppercase.index(letter) + self.setting -
                 self.offset) % len(self.wiring)
        letter = string.ascii_uppercase[index]

        return letter

    def encode_reverse(self, letter):
        index = (string.ascii_uppercase.index(letter) - self.setting +
                 self.offset) % len(self.wiring)
        letter = string.ascii_uppercase[index]

        index = (self.wiring.index(letter) + self.setting) % len(
            self.wiring)
        letter = string.ascii_uppercase[index]

        return letter


class Enigma:
    def __init__(self, rotors, reflector, plugboard=None):
        # Assert that plugboard is a Steckerbrett if not None
        assert plugboard is None or isinstance(plugboard, Steckerbrett)

        # Assert that rotors is a tuple and each tuple element is a Walzen
        assert isinstance(rotors, tuple)
        for index in range(len(rotors)):
            assert isinstance(rotors[index], Walzen)

        # Assert that reflector is an Umkehrwalze
        assert isinstance(reflector, Umkehrwalze)

        self.plugboard = plugboard
        self.rotors = rotors
        self.reflector = reflector

    def cipher(self, message):
        assert isinstance(message, str)

        message = message.upper()
        ciphered = ''

        for letter in message:
            if letter in string.ascii_uppercase:
                self._rotate()

                if self.plugboard is not None:
                    letter = self.plugboard.swap(letter)

                for rotor in self.rotors:
                    letter = rotor.encode(letter)

                letter = self.reflector.encode(letter)

                for rotor in self.rotors[::-1]:
                    letter = rotor.encode_reverse(letter)

                if self.plugboard is not None:
                    letter = self.plugboard.swap(letter)

            ciphered += letter

        return ciphered

    def _rotate(self):
        wiring = self.rotors[0].wiring
        self.rotors[0].wiring = wiring[1:] + wiring[0]

        for index in range(len(self.rotors) - 1):
            if self.rotors[index].notch == self.rotors[index].wiring[0]:
                if index == 1:
                    wiring = self.rotors[index].wiring
                    self.rotors[index].wiring = wiring[1:] + wiring[0]

                wiring = self.rotors[index + 1].wiring
                self.rotors[index + 1].wiring = wiring[1:] + wiring[0]



if __name__ == '__main__':
    plugboard = Steckerbrett('PO', 'ML', 'IU', 'KJ', 'NH', 'YT', 'GB', 'VF',
                             'RE', 'DC')

    rotors = (
        Walzen(wiring='EKMFLGDQVZNTOWYHXUSPAIBRCJ', notch='Q'),
        Walzen(wiring='AJDKSIRUXBLHWTMCQGZNPYFVOE', notch='E'),
        Walzen(wiring='BDFHJLCPRTXVZNYEIWGAKMUSQO', notch='V'),
    )

    reflector = Umkehrwalze(wiring='YRUHQSLDPXNGOKMIEBFZCWVJAT')

    machine = Enigma(rotors=rotors, reflector=reflector)