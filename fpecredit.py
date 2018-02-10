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

# Test value, TODO: multiple rounds
round = 1

# Turn the card number into a binary number with exactly 54 digits
cardnum = format(cardnum, '054b')
# Split the number into two 27-bit numbers
left = cardnum[:27]
right = cardnum[27:]

# This is the AES encryption used for each round in the Feistel network
# We use ECB with no problem since we encrypt only one block with it
def aes_enc(cardnum, round):
    # Each round we get the AES-128 key by padding the initial right number with
    # zeroes and appending the 8-bit, binary representation of the round number
    key = right.zfill(120) + format(round, '08b')

    encrypter = AS.new(key, AES.MODE_ECB)
    cardnum = encrypter.encrypt(cardnum)

    return cardnum;

# This is the AES decryption used for each round in the Feistel network
# For decryption we just need to reverse the encryption key schedule
def aed_dec(cardnum, round):
    decrypter = AES.new(key, AES.MODE_ECB)
    cardnum = decrypter.decrypt(cardnum)

    return cardnum;
