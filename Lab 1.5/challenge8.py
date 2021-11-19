#!/usr/bin/python3

# Mark Koszykowski
# ECE455 - Cybersecurity
# Lab 1.5 - Challenge 8
from challenge1 import hex_to_decimal
from challenge6 import decimal_to_binary
import re


def find_ecb(lines):
    scores = []
    for line in lines:
        while len(line) % 8 != 0:
            line = "0" + line
        line_bytes = re.findall("........", line)
        counts = dict()
        for byte in line_bytes:
            counts[byte] = counts.get(byte, 0) + 1

        scores.append((len(counts), counts))

    ecb_line = min(scores, key=lambda binary_line: binary_line[0])
    return scores.index(ecb_line), ecb_line[1]


def main():
    lines = []
    with open("8.txt", "r") as file:
        lines = file.readlines()

    binary_lines = [decimal_to_binary(hex_to_decimal(line.replace("\n", ""))) for line in lines]

    line_index, repeated_bytes = find_ecb(binary_lines)

    repeated_bytes = {k: v for k, v in sorted(repeated_bytes.items(), key=lambda item: item[1], reverse=True) if v > 1}

    print(F"Index of line encrypted with ECB: {line_index+1}")
    print()
    print("Line:")
    print(lines[line_index])
    print("Repeated bytes:")
    print("{")
    for k, v in repeated_bytes.items():
        print(F"\t'{k}' - Occurrences: {v}")
    print("}")


if __name__ == "__main__":
    main()
    
