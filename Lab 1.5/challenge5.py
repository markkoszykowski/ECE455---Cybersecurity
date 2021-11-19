#!/usr/bin/python3

# Mark Koszykowski
# ECE455 - Cybersecurity
# Lab 1.5 - Challenge 5
from challenge1 import hex_to_decimal
from challenge2 import decimal_to_hex

PLAINTEXT = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""


def string_to_hex(string):
    hex = ""
    for char in string:
        hex_val = decimal_to_hex(ord(char))
        while len(hex_val) % 2 != 0:
            hex_val = "0" + hex_val
        hex += hex_val
    return hex


def repeating_key_xor(plaintext, key):
    hex_plaintext = string_to_hex(plaintext)
    hex_key = string_to_hex(key)

    full_key = hex_key * (len(hex_plaintext) // len(hex_key))
    for i in range(len(key)):
        if len(full_key) >= len(hex_plaintext):
            break
        full_key += hex_key[2*i:2*i+2]

    ciphertext = decimal_to_hex(hex_to_decimal(hex_plaintext) ^ hex_to_decimal(full_key))
    if len(ciphertext) % 2 != 0:
        ciphertext = "0" + ciphertext
    return ciphertext


def main():
    repeating_key = input("Enter repeating key: ")
    ciphertext = repeating_key_xor(PLAINTEXT, repeating_key)
    print(F"Repeating-key XOR ciphertext: {ciphertext}")


if __name__ == "__main__":
    main()
    
