#!/usr/bin/env python3
from Crypto.Cipher import AES

# Credit card numbers must be of type int
try:
    cardnum = int(input("What is the card number?"))
except ValueError as err:
    print("Credit Card number must be a number!\n", err)
    raise
else:
    # Credit cards must have 16 digits
    if len(repr(cardnum)) != 16:
        raise ValueError("Credit Card number must have exactly 16 digits")

# Turn the card number into a binary number with exactly 54 digits
cardnum = format(cardnum, '054b')
# Split the number into two 27-bit numbers
left = cardnum[:27]
right = cardnum[27:]

# We use ECB with no problem since we encrypt only one block with it
def encrypt(cardnum, key):
    encrypter = AS.new(key, AES.MODE_ECB)
    cardnum = encrypter.encrypt(cardnum)

    return cardnum;

# For decryption we just need to reverse the encryption key schedule
def decrypt(cardnum, key):
    decrypter = AES.new(key, AES.MODE_ECB)
    cardnum = decrypter.decrypt(cardnum)

    return cardnum;
