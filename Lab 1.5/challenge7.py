#!/usr/bin/python3

# Mark Koszykowski
# ECE455 - Cybersecurity
# Lab 1.5 - Challenge 7
from Crypto.Cipher import AES
import base64


def aes_128_ecb_decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ciphertext).decode()


def main():
    key = input("Enter AES-128 ECB key: ")
    key = str.encode(key)

    ciphertext = None
    with open("7.txt", "r") as file:
        ciphertext = base64.b64decode(file.read())

    plaintext = aes_128_ecb_decrypt(ciphertext, key)
    print("Plaintext:")
    print(plaintext)


if __name__ == "__main__":
    main()
    
