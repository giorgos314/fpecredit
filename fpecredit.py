#!/usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from bitstring import Bits

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

# 101 bits so that we can have a 128 bit key, TODO: multiple rounds
round = Bits(int = 1, length = 101)

# Turn the card number into a binary number with exactly 54 digits
cardnum = Bits(int = cardnum, length = 54)

# Split the number into two 27-bit numbers
left = cardnum[:27]
right = cardnum[27:]


# This is the AES encryption used for each round in the Feistel network
# We use ECB with no problem since we encrypt only one block with it
def aes_enc(half, key, round):

    encrypter = AES.new(key, AES.MODE_ECB)
    block = half + round
    output = encrypter.encrypt(block.bin)
    output = output[:27]

    return Bits(output)

# This is the AES decryption used for each round in the Feistel network
# For decryption we just need to reverse the encryption key schedule

#TODO: decrypt
def aes_dec(half, key, round):
    decrypter = AES.new(key, AES.MODE_ECB)
    block = half + round
    output = decrypter.decrypt(block.bin)

    return Bits(output)
