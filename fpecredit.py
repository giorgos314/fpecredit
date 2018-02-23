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

# Test value, TODO: multiple rounds
round = Bits(int = 1, length = 101)

# Turn the card number into a binary number with exactly 54 digits
cardnum = Bits(int = cardnum, length = 54)

# Split the number into two 27-bit numbers
left = cardnum[:27]
right = cardnum[27:]

# bin > SHA256 > hexdigest

# This is the AES encryption used for each round in the Feistel network
# We use ECB with no problem since we encrypt only one block with it
def aes_enc(cardnum, round):
    # TODO: Each round we get the AES-128 key by padding the initial right number with
    # zeroes and appending the 8-bit, binary representation of the round number

    key = cardnum + round
    print(key)
    print(key.hex)
    print(len(key))

    encrypter = AES.new(key.hex, AES.MODE_ECB)
    output = encrypter.encrypt(Bits().join([cardnum, '0b00000']).bin)
    output = Bits(output)[:27]

    return output

# This is the AES decryption used for each round in the Feistel network
# For decryption we just need to reverse the encryption key schedule
def aes_dec(cardnum, round):
    decrypter = AES.new(key, AES.MODE_ECB)
    cardnum = decrypter.decrypt(key)

    return cardnum
