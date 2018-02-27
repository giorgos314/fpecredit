# fpecredit
Format Preserving Encryption for Credit Card Numbers. For when you need to encrypt a 16-digit number into a 16-digit number using AES.

This script was created for a **University of Piraeus** project.

Inspired from [this blog post](https://blog.cryptographyengineering.com/2011/11/10/format-preserving-encryption-or-how-to/) by M.Green.

## Requirements

 - Python 3.4 or newer
 - PyCrypto
	 - `sudo pip3 install pycrypto`
 -	Bitstring
	 -	sudo pip3 install bitstring

## Usage
There are multiple ways you can use fpecredit.py:

For encryption, use the following command. You will be asked for a card number, AES encryption key and the desired amount of Feistel rounds. 

    python3 fpecredit.py enc
 
Similarly, for the decryption. Keep in mind that **you need to use the same key and amount of rounds for encryption and decryption**.
 

    python3 fpecredit.py dec

<br>
You can also use testing mode by running one of the following:

Runs encryption with random input:

> python3 fpecredit.py test

Runs encryption/decryption with a default key, for a default amount of 5 rounds:

> python3 fpecredit.py testenc

> python3 fpecredit.py testdec
