#!/usr/bin/env python3
import re
import argparse

from Crypto.Cipher import AES
from bitstring import Bits
from random import randint
from sys import byteorder

cycles = 0

def rounds(right, left, key, roundnum, decrypt):
# Implementation of FPE
    print("\n-----------------")
    print("Right Key: " + right.bin)
    print("Left Key:  " + left.bin)
    print("-----------------\n")
    print("Starting AES Rounds..")

    if decrypt == True:
        for r in range(roundnum-1, -1, -1):
            print("Decrypting Round: " + repr(r+1))
            round = Bits(uint = r, length = 101)
            print("THIS Right Key: " + right.bin + "         " + repr(right.int))
            print("THIS Left Key:  " + left.bin + "         " + repr(left.int))
            print("-----------------")

            temp = left
            left = aes_enc(left, key, round) ^ right
            right = temp
            print("NEXT Right Key: " + right.bin + "         " + repr(right.int))
            print("NEXT Left Key:  " + left.bin + "         " + repr(left.int))
            print("-----------------")
    else:
        for r in range(0, roundnum):
            print("Round Number: " + repr(r+1))
            round = Bits(uint = r, length = 101)
            print("THIS Right Key: " + right.bin + "         " + repr(right.int))
            print("THIS Left Key:  " + left.bin + "         " + repr(left.int))
            print("-----------------")

            temp = right
            right = aes_enc(right, key, round) ^ left
            left = temp
            print("NEXT Right Key: " + right.bin + "         " + repr(right.int))
            print("NEXT Left Key:  " + left.bin + "         " + repr(left.int))
            print("-----------------")

    pad = Bits(bin="0000000000")
    whole = pad + left + right

    return whole.int


# This is the AES encryption used for each round in the Feistel network
# We use ECB with no problem since we encrypt only one block with it
def aes_enc(half, key, round):

    encrypter = AES.new(key, AES.MODE_ECB)
    block = half + round
    print(block.bin)
    output = encrypter.encrypt(block.bin)
    output = ''.join([str(x) for x in output])
    output = bin(int(output))
    output = output[2:29]

    return Bits(bin = output)


def mainloop(cardnum, key, roundnum, decrypt):
    global cycles
    card = re.findall('\d{4}', repr(cardnum))
    if cycles == 0:
        print("Card Number: " + ' '.join(num for num in card))
    # Turn the card number into a binary number with exactly 54 digits
    cardnum = Bits(uint = cardnum, length = 54)

    # Split the number into two 27-bit numbers
    left = cardnum[:27]
    right = cardnum[27:]

    while True:
        result = rounds(right, left, key, roundnum, decrypt)

        if len(repr(result)) > 16:
            print("\nThe result is more than 16 digits, cycling...")
            cycles += 1
            result = Bits(uint = result, length = 54)

            left = result[:27]
            right = result[27:]
        else:
            result = format(result, "016d")
            output = re.findall('\d{4}', repr(result))
            print("Result: " + ' '.join(num for num in output) + "\n")
            print("Cycled " + repr(cycles) + " times!")
            return result

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="Choose between enc, dec, testenc, testdec")
    args = parser.parse_args()
    decrypt = False

    if args.mode == "test":
        print("\n---Test Mode---\n")
        cardnum = randint(1000000000000000, 9999999999999999)
        key = 32*"A"
        roundnum = randint(3,9)
    elif args.mode == "testdec":
        print("\n---Test Decryption Mode, KEY=32*\"A\"---\n")
        cardnum = int(input("What is the card number?\n"))
        key = 32*"A"
        roundnum = int(input("How many rounds should the Feistel do?\n"))
        decrypt = True
    elif args.mode == "testenc":
        print("\n---Test Encryption Mode, KEY=32*\"A\"---\n")
        cardnum = int(input("What is the card number?\n"))
        key = 32*"A"
        roundnum = int(input("How many rounds should the Feistel do?\n"))
    else:
        if args.mode == "enc":
            print("\n---Encryption Mode---\n")
        elif args.mode == "dec":
            print("\n---Decryption Mode---\n")
            decrypt = True
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

    mainloop(cardnum, key, roundnum, decrypt)
