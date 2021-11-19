#!/usr/bin/python3

# Mark Koszykowski
# ECE455 - Cybersecurity
# Lab 1.5 - Challenge 6
from challenge1 import BASE64_CHAR, hex_to_decimal
from challenge2 import decimal_to_hex
from challenge3 import hex_to_string, try_decode
from challenge5 import string_to_hex, repeating_key_xor
import re

BASE64_VALUE = {v: k for k, v in BASE64_CHAR.items()}


def base64_to_binary(string):
    binary_string = ""
    for char in string:
        if char in BASE64_VALUE:
            base64_byte = decimal_to_binary(BASE64_VALUE[char])
            while len(base64_byte) % 6 != 0:
                base64_byte = "0" + base64_byte
            binary_string += base64_byte

    dont_count = string.count("=")
    return binary_string[:-2*dont_count]


def binary_to_decimal(string):
    value = 0
    power = 0
    for char in string[::-1]:
        value += int(char) * (2 ** power)
        power += 1
    return value


def decimal_to_binary(value):
    binary_string = "0" if value == 0 else ""
    while value != 0:
        binary_string = str(value % 2) + binary_string
        value = value // 2
    return binary_string


def hamming_distance(string1, string2):
    distance = 0
    for char1, char2 in zip(string1, string2):
        if char1 != char2:
            distance += 1
    return distance


def test_hamming_distance():
    string1 = input("Hamming distance test string 1: ")
    string2 = input("Hamming distance test string 2: ")

    binary1 = decimal_to_binary(hex_to_decimal(string_to_hex(string1)))
    binary2 = decimal_to_binary(hex_to_decimal(string_to_hex(string2)))

    while len(binary1) % 8 != 0:
        binary1 = "0" + binary1

    while len(binary2) % 8 != 0:
        binary2 = "0" + binary2

    print(F"The Hamming distance is: {hamming_distance(binary1, binary2)}")


def main():
    do_test = input("Perform Hamming distance test? (Y | N): ")
    while do_test not in "YyNn":
        do_test = input("Perform Hamming distance test? (Y | N): ")
    if do_test in "Yy":
        test_hamming_distance()

    ciphertext_base64 = ""
    with open("6.txt", "r") as file:
        ciphertext_base64 = "".join(file.readlines())

    ciphertext_binary = base64_to_binary(ciphertext_base64)

    keysizes = []
    for keysize in range(2, 41):
        blocks = [ciphertext_binary[i:i + 8*keysize] for i in range(0, len(ciphertext_binary), keysize*8)][0:4]
        pairs = []
        for i in range(len(blocks)):
            for j in range(i+1, len(blocks)):
                pairs.append((blocks[i], blocks[j]))

        scores = [hamming_distance(pair[0], pair[1]) / float(keysize) for pair in pairs]
        keysizes.append((keysize, sum(scores) / len(scores)))

    keysizes = sorted(keysizes, key=lambda item: item[1])

    keysize = keysizes[0][0]

    ciphertext_hex = decimal_to_hex(binary_to_decimal(ciphertext_binary))
    while len(ciphertext_hex) % 2 != 0:
        ciphertext_hex = "0" + ciphertext_hex

    padded_ciphertext = ciphertext_hex
    while len(padded_ciphertext) % (2*keysize) != 0:
        padded_ciphertext += "0"
    blocks = [re.findall("..", padded_ciphertext[i:i+2*keysize]) for i in range(0, len(padded_ciphertext), 2*keysize)]
    transposed_blocks = list(map(list, zip(*blocks)))

    repeated_key = [decimal_to_hex(try_decode("".join(transposed_block))[0]) for transposed_block in transposed_blocks]
    for i, digit in enumerate(repeated_key):
        if len(digit) % 2 != 0:
            repeated_key[i] = "0" + repeated_key[i]
    repeated_key = "".join(repeated_key)

    repeated_key = hex_to_string(repeated_key)

    plaintext = repeating_key_xor(hex_to_string(ciphertext_hex), repeated_key)
    while len(plaintext) % 2 != 0:
        plaintext = "0" + plaintext

    print(F"\nKey: '{repeated_key}'\n")
    print("Plaintext:")
    print(hex_to_string(plaintext))


if __name__ == "__main__":
    main()
    
