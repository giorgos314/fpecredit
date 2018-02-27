import unittest
from fpecredit import *


class FpeTests(unittest.TestCase):


    def test_output_length(self):
        decrypt = False
        cardnum = randint(1000000000000000, 9999999999999999)
        key = 32*"A"
        roundnum = randint(3,9)
        result = mainloop(cardnum, key, roundnum, decrypt)

        self.assertEqual(len(result), 16)


    def test_dec_output_length(self):
        decrypt = True
        cardnum = randint(1000000000000000, 9999999999999999)
        key = 32*"A"
        roundnum = randint(3,9)
        result = mainloop(cardnum, key, roundnum, decrypt)

        self.assertEqual(len(result), 16)


    def test_multiple_proper_decryptions(self):
        for x in range(50):
            decrypt = False
            cardnum = randint(1000000000000000, 9999999999999999)
            key = 32*"A"
            roundnum = randint(3,9)
            encrypted = mainloop(cardnum, key, roundnum, decrypt)

            decrypt = True
            decrypted = mainloop(int(encrypted), key, roundnum, decrypt)

            self.assertEqual(cardnum, int(decrypted))


if __name__ == '__main__':
    unittest.main()
