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
    """
    Default interpreter for a fractran program.
    It "simulates" it without any clever trick, simply by following the rules.

    The action parameter (by default the function doing nothing) is an arbitrary function
    which can (for instance) be used to debug a fractran program.
    """

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
    """
    Another interpreter for a fractran program.
    It views the input n as well as the fractions as their decomposition in prime factors
    and uses them to maintain registers, hence mimicking some kind of CPU.

    It is slower on "simple programs with simple inputs" because we are dealing with
    more complex datastructures (hashmaps) instead of O(1) arithmetic operations.
    However, this becomes way faster than the other version whenever the programs are trickier,
    and when n becomes very large ; because at that point the "O(1) arithmetic operations"
    proposition becomes false.
    """

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
    """Reads a fractran file (which contains only fractions of integers) and returns the fractions"""
    program = []

    with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                num, den = map(int, line.replace(" ", "").split("/"))
                program.append((num, den))
    
    return program

if __name__ == "__main__":
    """
    How to run this program:

    1) ./fractran.py <filename>        <- uses the main interpreter
    2) ./fractran.py <filename> -E     <- uses the secondary interpreter
    3) ./fractran.py <filename> -D     <- uses the debug mode (main interpreter unless -E is written before -D)
    
    Other arguments can be writter after -D to name some prime integers
    which can be useful if you "know" a fractran program and would like to debug it.

    For instance,
    4) ./fractran.py <filename> -D a=2 b=3 c=5
    activates the debug mode and in the debug prints
    you can see the variables "2" renamed to "a" instead of "v2" (and so on).
    """

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