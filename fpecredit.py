#!/usr/bin/env python3

from Crypto.Cipher import AES

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
