import unittest

from enigma import Enigma, Steckerbrett, Umkehrwalze, Walzen


class RotorTestCase(unittest.TestCase):
    def test_rotor_encoding(self):
        rotor = Walzen(wiring='EKMFLGDQVZNTOWYHXUSPAIBRCJ', notch='Q')
        self.assertEqual('E', rotor.encode('A'))


def run_tests():
    runner = unittest.TextTestRunner()
    suite = unittest.TestLoader().loadTestsFromTestCase(RotorTestCase)
    runner.run(suite)


if __name__ == '__main__':  # pragma: no cover
    run_tests()