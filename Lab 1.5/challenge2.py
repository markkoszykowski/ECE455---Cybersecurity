#!/usr/bin/python3

# Mark Koszykowski
# ECE455 - Cybersecurity
# Lab 1.5 - Challenge 2
from challenge1 import HEX_VALUE, hex_to_decimal

HEX_CHAR = {v: k for k, v in HEX_VALUE.items()}


def decimal_to_hex(value):
    hex_string = "0" if value == 0 else ""
    while value != 0:
        hex_string = HEX_CHAR[value % 16] + hex_string
        value = value // 16
    return hex_string


def hex_xor(hex1, hex2):
    value1 = hex_to_decimal(hex1)
    value2 = hex_to_decimal(hex2)
    xor_hex = decimal_to_hex(value1 ^ value2)
    return xor_hex


def main():
    hex1 = input("Enter first string to XOR: ")
    hex2 = input("Enter second string to XOR: ")
    xor_string = hex_xor(hex1, hex2)
    print(F"Fixed XOR string: {xor_string}")


if __name__ == "__main__":
    main()
    
