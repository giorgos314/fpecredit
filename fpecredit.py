#!/usr/bin/env python3
import re

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from bitstring import Bits


# Credit card numbers must be of type int
try:
    cardnum = int(input("What is the card number?\n"))
    key = str(input("What is the encryption key?\n"))
    roundnum = int(input("How many rounds should the Feistel do?\n"))
except ValueError as err:
    print("Credit Card number must be a number!\n", err)
    raise
else:
    # Credit cards must have 16 digits
    if len(repr(cardnum)) != 16:
        raise ValueError("Credit Card number must have exactly 16 digits")
    if len(key) != 32:
        raise ValueError("Key for AES-128 must be 32 characters long")


def rounds(right, left, key, roundnum):
# Implementation of FPE
    print("\n-----------------")
    print("Right Key: " + right.bin)
    print("Left Key:  " + left.bin)
    print("Starting AES Rounds..")

    for r in range(0, roundnum):
        print("Round Number: " + repr(r+1))
        round = Bits(int = r, length = 101)

        temp = right
        right = aes_enc(right, key, round) ^ left
        left = temp
        print("Right Key: " + right.bin)
        print("Left Key:  " + left.bin)
        print("-----------------")

    whole = left + right
    return abs(whole.int)


def cycle(result):
# This function makes sure that if the result of the Feistel Network is longer
# than 16 digits, the number goes again through the Feistel
    if len(repr(result)) > 16:
        return -1
    else:
        return result


# This is the AES encryption used for each round in the Feistel network
# We use ECB with no problem since we encrypt only one block with it
def aes_enc(half, key, round):

    encrypter = AES.new(key, AES.MODE_ECB)
    block = half + round
    output = encrypter.encrypt(block.bin)

    return Bits(output)[:27]

# This is the AES decryption used for each round in the Feistel network
# For decryption we just need to reverse the encryption key schedule


#TODO: decrypt
def aes_dec(half, key, round):
    decrypter = AES.new(key, AES.MODE_ECB)
    block = half + round
    output = decrypter.decrypt(block.bin)

    return Bits(output)


def mainloop(cardnum, key, roundnum):
    # Turn the card number into a binary number with exactly 54 digits
    cardnum = Bits(int = cardnum, length = 54)

    # Split the number into two 27-bit numbers
    left = cardnum[:27]
    right = cardnum[27:]

    while True:
        result = rounds(right, left, key, roundnum)
        if cycle(result) == -1:
            print("The result is more than 16 digits, cycling...")
            mainloop(result, key, roundnum)
        else:
            result = format(result, "016d")
            output = re.findall('\d{4}', repr(result))
            print("Result: " + ' '.join(num for num in output))
            return result


mainloop(cardnum, key, roundnum)
