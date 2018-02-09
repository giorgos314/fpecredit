#!/usr/bin/env python3

from Crypto.Cipher import AES

def encrypt(cardnum, key, iv):
    encrypter = AES.new(key, AES.MODE_CBC, iv)
    cardnum = encrypter.encrypt(cardnum)

    return cardnum;

def decrypt(cardnum, key, iv):
    decrypter = AES.new(key, AES.MODE_CBC, iv)
    cardnum = decrypter.decrypt(cardnum)

    return cardnum;
