import unittest
from skatzero.game.utils import compare_cards

class TestCompareCards(unittest.TestCase):
    def test_compare_cards(self):
        # Test case 1: Two Jacks, same suit
        self.assertFalse(compare_cards('DJ', 'CJ', 'D', 'D'))
        self.assertTrue(compare_cards('CJ', 'DJ', 'D', 'D'))
        self.assertFalse(compare_cards('DJ', 'CJ', 'J', 'J'))
        self.assertTrue(compare_cards('CJ', 'DJ', 'J', 'J'))
        self.assertTrue(compare_cards('DJ', 'CJ', None, 'D'))
        self.assertTrue(compare_cards('CJ', 'DJ', None, 'C'))

        # Test case 2: One Jack, different suits
        self.assertTrue(compare_cards('DJ', 'C7', 'D', 'D'))
        self.assertFalse(compare_cards('C7', 'DJ', 'D', 'C'))
        self.assertTrue(compare_cards('DJ', 'C7', 'J', 'J'))
        self.assertFalse(compare_cards('C7', 'DJ', 'J', 'C'))
        self.assertTrue(compare_cards('DJ', 'C7', None, 'D'))
        self.assertTrue(compare_cards('C7', 'DJ', None, 'C'))

        # Test case 3: Different suites no trump
        self.assertTrue(compare_cards('H7', 'C8', 'D', 'H'))
        self.assertTrue(compare_cards('C8', 'H7', 'D', 'C'))
        self.assertTrue(compare_cards('H7', 'C8', 'J', 'H'))
        self.assertTrue(compare_cards('C8', 'H7', 'J', 'C'))
        self.assertTrue(compare_cards('H7', 'C8', None, 'H'))
        self.assertTrue(compare_cards('C8', 'H7', None, 'C'))

        # Test case 4: Different suites with trump
        self.assertTrue(compare_cards('D7', 'C8', 'D', 'D'))
        self.assertFalse(compare_cards('C8', 'D7', 'D', 'C'))
        self.assertTrue(compare_cards('HJ', 'C8', 'J', 'D'))
        self.assertFalse(compare_cards('C8', 'HJ', 'J', 'C'))

        # Test case 5: Same suit no trump
        self.assertFalse(compare_cards('HK', 'HT', 'D', 'H'))
        self.assertTrue(compare_cards('HT', 'HK', 'D', 'H'))
        self.assertFalse(compare_cards('HK', 'HT', 'J', 'H'))
        self.assertTrue(compare_cards('HT', 'HK', 'J', 'H'))
        self.assertTrue(compare_cards('HK', 'HT', None, 'H'))
        self.assertFalse(compare_cards('HT', 'HK', None, 'H'))

        # Test case 6: Same suit with trump
        self.assertFalse(compare_cards('DK', 'DT', 'D', 'D'))
        self.assertTrue(compare_cards('DT', 'DK', 'D', 'D'))

if __name__ == '__main__':
    unittest.main()
