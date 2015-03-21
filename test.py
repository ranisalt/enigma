import unittest

from enigma import Enigma, Steckerbrett, Umkehrwalze, Walzen


class RotorTestCase(unittest.TestCase):
    def test_rotor_encoding(self):
        rotor = Walzen(wiring='EKMFLGDQVZNTOWYHXUSPAIBRCJ', notch='Q')
        self.assertEqual('E', rotor.encode('A'))

    def test_rotor_reverse_encoding(self):
        rotor = Walzen(wiring='EKMFLGDQVZNTOWYHXUSPAIBRCJ', notch='Q')
        self.assertEqual('U', rotor.encode_reverse('A'))

    def test_rotor_different_setting(self):
        rotor = Walzen(wiring='EKMFLGDQVZNTOWYHXUSPAIBRCJ', notch='Q',
                       ringstellung='B')
        self.assertEqual('J', rotor.encode('A'))
        self.assertEqual('V', rotor.encode_reverse('A'))

    def test_rotor_different_offset(self):
        rotor = Walzen(wiring='EKMFLGDQVZNTOWYHXUSPAIBRCJ', notch='Q',
                       offset='B')
        self.assertEqual('D', rotor.encode('A'))
        self.assertEqual('W', rotor.encode_reverse('A'))

    def test_rotor_different_setting_and_offset(self):
        rotor = Walzen(wiring='EKMFLGDQVZNTOWYHXUSPAIBRCJ', notch='Q',
                       ringstellung='B', offset='B')
        self.assertEqual('I', rotor.encode('A'))
        self.assertEqual('X', rotor.encode_reverse('A'))

    def test_rotor_turnover(self):
        rotor = Walzen(wiring='EKMFLGDQVZNTOWYHXUSPAIBRCJ', notch='Q')
        rotor.advance()
        self.assertEqual('J', rotor.encode('A'))
        self.assertEqual('V', rotor.encode_reverse('A'))


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
        machine.cipher('A' * 16900) # this should do a full cycle on rotors
        self.assertEqual('B', machine.cipher('A'))


def run_tests():
    unittest.main()


if __name__ == '__main__':  # pragma: no cover
    run_tests()
