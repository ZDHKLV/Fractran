#!/usr/bin/env python3

from typing import Callable
import pretty
import sys

type Fraction = tuple[int, int]

def run(program: list[Fraction],
        n: int,
        action: Callable[[int], None] = lambda _ : ()):

    while True:
        action(n)
        for num, den in program:
            if (num * n) % den == 0:
                n = (num * n) // den
                break
        else:
            return n

def run_from_file(filename: str,
                  n: int,
                  action: Callable[[int], None] = lambda _ : ()):

    program = []

    with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                num, den = map(int, line.replace(" ", "").split("/"))
                program.append((num, den))

    return run(program, n, action)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

        print("Input:")
        n = pretty.pretty_prime_factors_to_int(input())

        debug = (len(sys.argv) >= 3 and sys.argv[2] == "-D")

        if debug:
            names = {}
            for i in range(3, len(sys.argv)):
                a, b = sys.argv[i].split("=")
                names[int(b)] = a

            action = lambda n : print(pretty.int_to_pretty_registers(n, names, True))
        else:
            action = lambda _ : ()

        output = run_from_file(filename, n, action)

        if output == 1:
            print(1)
        else:
            print(pretty.int_to_pretty_prime_factors(output))

    else:
        print("Retry with the filename of the program as an argument.")