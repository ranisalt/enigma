import string

alphabet = string.ascii_uppercase


class Steckerbrett:
    def __init__(self, *args):
        map = {}

        for arg in args:
            if arg[0] in map or arg[1] in map:
                raise KeyError('Same letter used twice in plugboard')

            map[arg[0]] = arg[1]
            map[arg[1]] = arg[0]

        self.swap = lambda letter: map[letter] if letter in map else letter


class Umkehrwalze:
    def __init__(self, wiring):
        assert isinstance(wiring, str)
        if (sorted(wiring) != list(alphabet)):
            raise KeyError('Plugboard should contain every letter only once')

        self.encode = lambda letter: wiring[alphabet.index(letter)]


class Walzen:
    def __init__(self, notch, wiring, ringstellung='A'):
        self.notch = alphabet.index(notch)  # n
        self.ringstellung = alphabet.index(ringstellung)  # r
        self.perm = str.maketrans(string.ascii_uppercase, wiring)
        self.rev_perm = str.maketrans(wiring, string.ascii_uppercase)

        self._shift_up = lambda letter, j: alphabet[
            (alphabet.index(letter) + j) % 26]
        self._shift_down = lambda letter, j: alphabet[
            (alphabet.index(letter) - j) % 26]

    def encode(self, letter, j=0):
        return self._shift_down(
            str.translate(
                self._shift_up(letter, j),
                self.perm),
            j)

    def encode_reverse(self, letter, j=0):
        return self._shift_down(
            str.translate(
                self._shift_up(letter, j),
                self.rev_perm),
            j)


class Enigma:
    def __init__(self, rotors, reflector, plugboard=Steckerbrett(),
                 grundstellung='AAA'):
        # Assert that plugboard is a Steckerbrett if not None
        assert isinstance(plugboard, Steckerbrett)

        # Assert that rotors is a tuple and each tuple element is a Walzen
        assert isinstance(rotors, tuple)
        for index in range(len(rotors)):
            assert isinstance(rotors[index], Walzen)

        # Assert that reflector is an Umkehrwalze
        assert isinstance(reflector, Umkehrwalze)

        self.plugboard = plugboard
        self.rotors = rotors
        self.reflector = reflector
        self.grundstellung = tuple(alphabet.index(l) for l in grundstellung)

    def cipher(self, message):
        assert isinstance(message, str)

        message = message.upper()
        ciphered = ''

        # pode pegar esses valores no __init__ também
        # essas funções lambda são puro charme.
        p = lambda n: self.grundstellung[n]
        r = lambda n: self.rotors[n].ringstellung
        n = lambda n: self.rotors[n].notch
        encode = lambda i, letter, exp: self.rotors[i].encode(letter, exp)
        rencode = lambda i, letter, exp: self.rotors[i].encode_reverse(letter,
                                                                       exp)

        m1 = (n(0) - p(0)) % 26
        m2 = m1 + 26 * ((n(1) - p(1) - 1) % 26) + 1

        i1 = p(0) - r(0) + 1

        for j, letter in enumerate(message):
            if letter in string.ascii_uppercase:
                # usando int() pra arredondar
                k1, k2 = int((j - m1 + 26) / 26), int((j - m2 + 650) / 650)
                i2, i3 = p(1) - r(1) + k1 + k2, p(2) - r(2) + k2

                letter = self.plugboard.swap(letter)
                letter = encode(2, encode(1, encode(0, letter, i1 + j), i2), i3)
                letter = self.reflector.encode(letter)
                letter = rencode(0, rencode(1, rencode(2, letter, i3), i2),
                                 i1 + j)
                letter = self.plugboard.swap(letter)

            ciphered += letter

        return ciphered


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
