#!/usr/bin/python3

# Mark Koszykowski
# ECE455 - Cybersecurity
# Lab 1.5 - Challenge 1

HEX_VALUE = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "a": 10,
    "b": 11,
    "c": 12,
    "d": 13,
    "e": 14,
    "f": 15
}

BASE64_CHAR = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E",
    5: "F",
    6: "G",
    7: "H",
    8: "I",
    9: "J",
    10: "K",
    11: "L",
    12: "M",
    13: "N",
    14: "O",
    15: "P",
    16: "Q",
    17: "R",
    18: "S",
    19: "T",
    20: "U",
    21: "V",
    22: "W",
    23: "X",
    24: "Y",
    25: "Z",
    26: "a",
    27: "b",
    28: "c",
    29: "d",
    30: "e",
    31: "f",
    32: "g",
    33: "h",
    34: "i",
    35: "j",
    36: "k",
    37: "l",
    38: "m",
    39: "n",
    40: "o",
    41: "p",
    42: "q",
    43: "r",
    44: "s",
    45: "t",
    46: "u",
    47: "v",
    48: "w",
    49: "x",
    50: "y",
    51: "z",
    52: "0",
    53: "1",
    54: "2",
    55: "3",
    56: "4",
    57: "5",
    58: "6",
    59: "7",
    60: "8",
    61: "9",
    62: "+",
    63: "/"
}


def hex_to_decimal(string):
    value = 0
    power = 0
    for char in string[::-1]:
        value += (HEX_VALUE[char] * (16 ** power))
        power += 1
    return value


def decimal_to_base64(value):
    base64_string = ""
    while value != 0:
        base64_string = BASE64_CHAR[value % 64] + base64_string
        value = value // 64
    return base64_string


def hex_to_base64(string):
    value = hex_to_decimal(string)
    base64_string = decimal_to_base64(value)
    return base64_string


def main():
    hex_string = input("Enter hex string to convert to base64: ")
    print(F"base64 string: {hex_to_base64(hex_string)}")
    

if __name__ == "__main__":
    main()
    
