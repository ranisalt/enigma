import unittest

from enigma import Enigma, Steckerbrett, Umkehrwalze, Walzen


class RotorTestCase(unittest.TestCase):
    def test_rotor_encoding(self):
        rotor = Walzen(wiring='EKMFLGDQVZNTOWYHXUSPAIBRCJ', notch='Q')
        self.assertEqual('E', rotor.encode('A'))

        # repeating key rotates rotors backwards. E -> J -> C...
        self.assertEqual('J', rotor.encode('A', 1))

    def test_rotor_reverse_encoding(self):
        rotor = Walzen(wiring='EKMFLGDQVZNTOWYHXUSPAIBRCJ', notch='Q')
        self.assertEqual('U', rotor.encode_reverse('A'))
        self.assertEqual('V', rotor.encode_reverse('A', 1))


class ReflectorTestCase(unittest.TestCase):
    def test_reflector(self):
        reflector = Umkehrwalze(wiring='YRUHQSLDPXNGOKMIEBFZCWVJAT')
        self.assertEqual('Y', reflector.encode('A'))

    def test_reflector_fails_on_invalid_wiring(self):
        self.assertRaises(KeyError, Umkehrwalze,
                          wiring='YRUHQSLDPXNGOKMIEBFZCWVJA')
        self.assertRaises(KeyError, Umkehrwalze,
                          wiring='YRYHQSLDPXNGOKMIEBFZCWVJAT')


class PlugboardTestCase(unittest.TestCase):
    def test_plugboard_swapping(self):
        plugboard = Steckerbrett('PO', 'ML', 'IU', 'KJ', 'NH', 'YT', 'GB',
                                 'VF', 'RE', 'DC')
        self.assertEqual('O', plugboard.swap('P'))
        self.assertEqual('M', plugboard.swap('L'))

    def test_plugboard_not_swap(self):
        plugboard = Steckerbrett('PO', 'ML', 'IU', 'KJ', 'NH', 'YT', 'GB',
                                 'VF', 'RE', 'DC')
        self.assertEqual('A', plugboard.swap('A'))

    def test_plugboard_fails_on_repeated_letter(self):
        self.assertRaises(KeyError, Steckerbrett, 'PO', 'PL')


class EnigmaTestCase(unittest.TestCase):
    def setUp(self):
        self.rotors = (
            Walzen(wiring='EKMFLGDQVZNTOWYHXUSPAIBRCJ', notch='Q'),
            Walzen(wiring='AJDKSIRUXBLHWTMCQGZNPYFVOE', notch='E'),
            Walzen(wiring='BDFHJLCPRTXVZNYEIWGAKMUSQO', notch='V'),
        )

        self.reflector = Umkehrwalze(wiring='YRUHQSLDPXNGOKMIEBFZCWVJAT')

        self.plugboard = Steckerbrett('PO', 'ML', 'IU', 'KJ', 'NH', 'YT', 'GB',
                                      'VF', 'RE', 'DC')

    def test_enigma_cipher(self):
        machine = Enigma(rotors=self.rotors[::-1], reflector=self.reflector)
        self.assertEqual('BDZGO', machine.cipher('AAAAA'))

    def test_enigma_decipher(self):
        machine = Enigma(rotors=self.rotors[::-1], reflector=self.reflector)
        self.assertEqual('AAAAA', machine.cipher('BDZGO'))

    def test_enigma_full_cycle(self):
        machine = Enigma(rotors=self.rotors[::-1], reflector=self.reflector)
        machine.cipher('A' * 16900)  # this should do a full cycle on rotors
        self.assertEqual('BDZGO', machine.cipher('AAAAA'))

    def test_enigma_uses_plugboard(self):
        machine = Enigma(rotors=self.rotors[::-1], reflector=self.reflector,
                         plugboard=self.plugboard)
        self.assertEqual('GCZBP', machine.cipher('AAAAA'))

    def test_enigma_different_ringstellung(self):
        self.rotors = (
            Walzen(wiring='EKMFLGDQVZNTOWYHXUSPAIBRCJ', notch='Q', ringstellung='B'),
            Walzen(wiring='AJDKSIRUXBLHWTMCQGZNPYFVOE', notch='E', ringstellung='B'),
            Walzen(wiring='BDFHJLCPRTXVZNYEIWGAKMUSQO', notch='V', ringstellung='B'),
        )

        machine = Enigma(rotors=self.rotors[::-1], reflector=self.reflector)
        self.assertEqual('EWTYX', machine.cipher('AAAAA'))

    def test_enigma_different_grundstellung(self):
        self.rotors = (
            Walzen(wiring='EKMFLGDQVZNTOWYHXUSPAIBRCJ', notch='Q'),
            Walzen(wiring='AJDKSIRUXBLHWTMCQGZNPYFVOE', notch='E'),
            Walzen(wiring='BDFHJLCPRTXVZNYEIWGAKMUSQO', notch='V'),
        )

        machine = Enigma(rotors=self.rotors[::-1], reflector=self.reflector, grundstellung='BBB')
        self.assertEqual('PGQPW', machine.cipher('AAAAA'))

    def test_enigma_different_ringstellung_and_grundstellung(self):
        self.rotors = (
            Walzen(wiring='EKMFLGDQVZNTOWYHXUSPAIBRCJ', notch='Q', ringstellung='B'),
            Walzen(wiring='AJDKSIRUXBLHWTMCQGZNPYFVOE', notch='E', ringstellung='B'),
            Walzen(wiring='BDFHJLCPRTXVZNYEIWGAKMUSQO', notch='V', ringstellung='B'),
        )

        machine = Enigma(rotors=self.rotors[::-1], reflector=self.reflector, grundstellung='BBB')
        self.assertEqual('BDZGO', machine.cipher('AAAAA'))


def run_tests():
    unittest.main()


if __name__ == '__main__':  # pragma: no cover
    run_tests()
