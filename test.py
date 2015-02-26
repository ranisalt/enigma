import unittest


class EnigmaTestCase(unittest.TestCase):
    pass


def run_tests():
    runner = unittest.TextTestRunner()
    suite = unittest.TestLoader().loadTestsFromTestCase(EnigmaTestCase)
    runner.run(suite)


if __name__ == '__main__':  # pragma: no cover
    run_tests()