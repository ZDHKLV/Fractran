#!/usr/bin/env python3

import fractran
import pretty

COUNT = 0

def test(prog: str, inp: int, expected: int):
    global COUNT
    out = fractran.run_from_file(f"programs/{prog}", inp)
    try:
        assert out == expected
    except AssertionError:
        print(f"Test failed on programe {prog}")
        print(f"Input: {pretty.int_to_pretty_registers(inp)}")
        print(f"Expected outcome: {pretty.int_to_pretty_registers(expected)}")
        print(f"Received outcome: {pretty.int_to_pretty_registers(out)}")
        exit(0)
    COUNT += 1

if __name__ == "__main__":

    # accumulate:
    for dst in range(10):
        for src in range(10):
            inp = 2**dst * 3**src * 5
            expected = 2**(dst + src) * 3**src
            test("accumulate", inp, expected)

    # accumulate_and_destroy:
    for dst in range(10):
        for src in range(10):
            inp = 2**dst * 3**src * 5
            expected = 2**(dst + src)
            test("accumulate_and_destroy", inp, expected)
    
    # add
    for dst in range(5):
        for x in range(10):
            for y in range(10):
                inp = 2**dst * 3**x * 5**y * 7
                expected = 2**(x + y) * 3**x * 5**y
                test("add", inp, expected)
    
    # copy
    for dst in range(10):
        for src in range(10):
            inp = 2**dst * 3**src * 5
            expected = 2**src * 3**src
            test("copy", inp, expected)
    
    # increments
    for i in [1, 2, 5]:
        for x in range(10):
            inp = 2**x * 3
            expected = 2**(x+i)
            test(f"increment_{i}", inp, expected)

    # branch_then_decrement
    # How?

    # branch
    # How?

    # goto
    test("goto", 2**1, 3**1)

    # clear
    for x in range(20):
        inp = 2**x * 3
        expected = 1
        test("clear", inp, expected)
    
    # euclidian_division
    for n in range(20):
        for d in range(1, n):
            for o1 in range(3):
                for o2 in range(3):
                    inp = 2**n * 3**d * 5**o1 * 7**o2 * 11
                    exp_q = n // d
                    exp_r = n % d
                    expected = 2**n * 3**d * 5**exp_q * 7**exp_r
                    test("euclidian_division", inp, expected)
    
    # multiply
    for x in range(10):
        for y in range(10):
            for o in range(3):
                inp = 2**x * 3**y * 5**o * 7
                expected = 2**x * 3**y * 5**(x*y)
                test("multiply", inp, expected)
    
    # multiply_on
    for x in range(10):
        for y in range(10):
            inp = 2**x * 3**y * 5
            expected = 2**(x*y) * 3**y
            test("multiply_on", inp, expected)

    # sum
    for i in range(20):
        inp = 2**i * 5
        expected = 3**(i * (i + 1) // 2)
        test("sum", inp, expected)
    
    # fibonacci

    def fib(n):
        a = 0
        b = 1
        while n > 0:
            c = a + b
            a = b
            b = c
            n -= 1
        return b

    for n in range(10):
        for o in range(3):
            inp = 2**n * 3**o * 5
            expected = 3**fib(n)
            test("fibonacci", inp, expected)

    # collatz

    def collatz(n):
        i = 0
        while n > 1:
            i += 1
            if n % 2 == 0:
                n //= 2
            else:
                n = 3 * n + 1
        return i

    for n in range(10):
        for o in range(3):
            inp = 2**n * 3**o * 5
            expected = 3**collatz(n)
            test("collatz", inp, expected)

    print(f"Success! ({COUNT} tests)")