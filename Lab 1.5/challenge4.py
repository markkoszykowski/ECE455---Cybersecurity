#!/usr/bin/python3

# Mark Koszykowski
# ECE455 - Cybersecurity
# Lab 1.5 - Challenge 4
from challenge3 import try_decode


def find_line(lines):
    decodes = []
    for line in lines:
        decodes.append(try_decode(line))

    max_score_line = max(decodes, key=lambda item: item[2])
    index = decodes.index(max_score_line) + 1
    return index, max_score_line


def main():
    lines = []
    with open("4.txt", "r") as file:
        lines = file.readlines()

    lines = [line.replace("\n", "") for line in lines]

    line, info = find_line(lines)

    print(F"Single-character XOR encryption on line: {line}")
    print(F"Key: {info[0]} ({chr(info[0])}), Message: '{info[1].strip()}'")


if __name__ == "__main__":
    main()
    
