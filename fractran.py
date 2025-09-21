#!/usr/bin/env python3

from typing import Callable
from collections import Counter
import primes
import pretty
import sys

type Fraction = tuple[int, int]

def evaluate(program: list[Fraction],
             n: int,
             action: Callable[[int], None] = lambda _ : ()) -> int:

    while True:
        action(n)
        for num, den in program:
            if (num * n) % den == 0:
                n = (num * n) // den
                break
        else:
            return n

def evaluate2(program: list[Fraction],
              n: int,
              action: Callable[[Counter], None] = lambda _ : ()) -> int:

    registers = Counter(primes.prime_factors(n))
    counters = [
        (Counter(primes.prime_factors(num)), Counter(primes.prime_factors(den)))
        for num, den in program
    ]

    while True:
        action(registers)
        for c_num, c_den in counters:

            for k_den in c_den:
                if registers[k_den] < c_den[k_den]:
                    break
            else:
                for k_den in c_den:
                    registers[k_den] -= c_den[k_den]

                for k_num in c_num:
                    registers[k_num] += c_num[k_num]

                break
        else:
            output = 1
            for key in registers:
                output *= (key**registers[key])
            return output

def program_from_file(filename: str) -> list[Fraction]:
    program = []

    with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                num, den = map(int, line.replace(" ", "").split("/"))
                program.append((num, den))
    
    return program

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

        print("Input:")
        n = pretty.pretty_prime_factors_to_int(input())

        debug = ("-D" in sys.argv)

        if debug:
            names = {}
            for i in range(sys.argv.index("-D"), len(sys.argv)):
                a, b = sys.argv[i].split("=")
                names[int(b)] = a

            action = lambda n : print(pretty.int_to_pretty_registers(n, names, True))
        else:
            action = lambda _ : ()

        if "-O" not in sys.argv:
            output = evaluate(program_from_file(filename), n, action)
        else:
            output = evaluate2(program_from_file(filename), n)

        if output == 1:
            print(1)
        else:
            print(pretty.int_to_pretty_prime_factors(output))

    else:
        print("Retry with the filename of the program as an argument.")