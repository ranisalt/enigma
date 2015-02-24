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
        assert isinstance(message, str)

        message = message.upper()
        ciphered = ''

        for letter in message:
            if letter != ' ':
                self._rotate()

                for rotor in self.rotors:
                    letter = rotor.encode(letter)

                letter = reflector.encode(letter)

                for rotor in rotors[::-1]:
                    letter = rotor.encode_reverse(letter)

            ciphered += letter

        return ciphered

    def _rotate(self):
        wiring = self.rotors[0].wiring
        self.rotors[0].wiring = wiring[1:] + wiring[0]

        for index in range(len(self.rotors) - 1):
            if self.rotors[index].notch == self.rotors[index].wiring[0]:
                wiring = self.rotors[index + 1].wiring
                self.rotors[index + 1].wiring = wiring[1:] + wiring[0]


if __name__ == '__main__':
    rotors = (
        Walzen(wiring='EKMFLGDQVZNTOWYHXUSPAIBRCJ', notch='Q'),
        Walzen(wiring='AJDKSIRUXBLHWTMCQGZNPYFVOE', notch='E'),
        Walzen(wiring='BDFHJLCPRTXVZNYEIWGAKMUSQO', notch='V'),
    )

    reflector = Umkehrwalze(wiring='YRUHQSLDPXNGOKMIEBFZCWVJAT')

    machine = Enigma(rotors=rotors, reflector=reflector)
