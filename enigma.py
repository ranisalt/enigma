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
        assert isinstance(wiring, str)
        if (sorted(wiring) != list(string.ascii_uppercase)):
            raise KeyError('Plugboard should contain every letter only once')

        self.wiring = wiring

    def encode(self, letter):
        return self.wiring[string.ascii_uppercase.index(letter)]


class Walzen:
    def __init__(self, notch, wiring, ringstellung='A', offset='A'):
        assert isinstance(notch, str)
        assert isinstance(wiring, str)
        assert len(wiring) == len(string.ascii_uppercase)

        self.notch = notch

        if isinstance(ringstellung, str) and len(ringstellung) == 1:
            self.ringstellung = string.ascii_uppercase.index(ringstellung)
        elif isinstance(ringstellung, int) and 0 <= ringstellung < len(wiring):
            self.ringstellung = ringstellung
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
        index = string.ascii_uppercase.index(letter) - self.ringstellung
        letter = self.wiring[index % len(self.wiring)]

        index = string.ascii_uppercase.index(letter) - self.offset
        letter = string.ascii_uppercase[index % len(self.wiring)]

        return letter

    def encode_reverse(self, letter):
        index = string.ascii_uppercase.index(letter) + self.offset
        letter = string.ascii_uppercase[index % len(self.wiring)]

        index = self.wiring.index(letter) + self.ringstellung
        letter = string.ascii_uppercase[index % len(self.wiring)]

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
        self.rotors[0].ringstellung += 1

        for index in range(len(self.rotors) - 1):
            rotor = self.rotors[index]
            if rotor.notch == rotor.wiring[rotor.ringstellung]:
                if index == 1:
                    rotor.ringstellung+= 1

                self.rotors[index + 1].ringstellung += 1


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