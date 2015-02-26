import unittest

from enigma import Enigma, Umkehrwalze, Walzen


class EnigmaTestCase(unittest.TestCase):
    def setUp(self):
        # Rotors go from right to left, so I reverse the tuple to make Rotor
        # I be the leftmost. I may change this behavior in the future.
        rotors = (
            Walzen(wiring='EKMFLGDQVZNTOWYHXUSPAIBRCJ', notch='Q'),
            Walzen(wiring='AJDKSIRUXBLHWTMCQGZNPYFVOE', notch='E'),
            Walzen(wiring='BDFHJLCPRTXVZNYEIWGAKMUSQO', notch='V'),
        )[::-1]

        reflector = Umkehrwalze(wiring='YRUHQSLDPXNGOKMIEBFZCWVJAT')

        self.machine = Enigma(rotors=rotors, reflector=reflector)


def run_tests():
    runner = unittest.TextTestRunner()
    suite = unittest.TestLoader().loadTestsFromTestCase(EnigmaTestCase)
    runner.run(suite)


if __name__ == '__main__':  # pragma: no cover
    run_tests()