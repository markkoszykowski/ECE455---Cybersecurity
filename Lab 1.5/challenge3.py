#!/usr/bin/python3

# Mark Koszykowski
# ECE455 - Cybersecurity
# Lab 1.5 - Challenge 3
from challenge1 import hex_to_decimal
from challenge2 import decimal_to_hex

LETTER_FREQUENCIES = {
    "a": 0.0651738,
    "b": 0.0124248,
    "c": 0.0217339,
    "d": 0.0349835,
    "e": 0.1041442,
    "f": 0.0197881,
    "g": 0.0158610,
    "h": 0.0492888,
    "i": 0.0558094,
    "j": 0.0009033,
    "k": 0.0050529,
    "l": 0.0331490,
    "m": 0.0202124,
    "n": 0.0564513,
    "o": 0.0596302,
    "p": 0.0137645,
    "q": 0.0008606,
    "r": 0.0497563,
    "s": 0.0515760,
    "t": 0.0729357,
    "u": 0.0225134,
    "v": 0.0082903,
    "w": 0.0171272,
    "x": 0.0013692,
    "y": 0.0145984,
    "z": 0.0007836,
    " ": 0.1918182
}


def hex_to_string(hex_string):
    string = ""
    while len(hex_string) % 2 != 0:
        hex_string = "0" + hex_string

    for i in range(len(hex_string)//2):
        string += chr(hex_to_decimal(hex_string[2*i:2*i+2]))
    return string


def score_string(string):
    score = 0
    for char in string:
        if char.lower() in LETTER_FREQUENCIES:
            score += LETTER_FREQUENCIES[char.lower()]
    return score


def try_decode(encoded_string):
    decodes = []
    if len(encoded_string) % 2 != 0:
        encoded_string = "0" + encoded_string
    value = hex_to_decimal(encoded_string)
    for i in range(256):
        key = decimal_to_hex(i)
        while len(key) % 2 != 0:
            key = "0" + key

        key = key * (len(encoded_string) // len(key))

        decode_hex = decimal_to_hex(value ^ hex_to_decimal(key))
        decode_string = hex_to_string(decode_hex)
        decode_score = score_string(decode_string)
        decodes.append((i, decode_string, decode_score))
    return max(decodes, key=lambda item: item[2])


def main():
    encoded = input("Enter encoded hex string: ")
    key, decoded, _ = try_decode(encoded)
    print(F"Key: {key} ({chr(key)}), Message: '{decoded.strip()}'")


if __name__ == "__main__":
    main()
    
