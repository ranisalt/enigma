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
                       setting='B')
        self.assertEqual('K', rotor.encode('A'))
        self.assertEqual('K', rotor.encode_reverse('A'))

    def test_rotor_different_offset(self):
        rotor = Walzen(wiring='EKMFLGDQVZNTOWYHXUSPAIBRCJ', notch='Q',
                       offset='B')
        self.assertEqual('D', rotor.encode('A'))
        self.assertEqual('W', rotor.encode_reverse('A'))


def run_tests():
    runner = unittest.TextTestRunner()
    suite = unittest.TestLoader().loadTestsFromTestCase(RotorTestCase)
    runner.run(suite)


if __name__ == '__main__':  # pragma: no cover
    run_tests()