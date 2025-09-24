#!/usr/bin/env python3

from fractran import Fraction
import primes
import sys

HEAD = 0

type Prime = int
type State = Prime
type Var = Prime

def uniques(amount: int) -> list[Prime]:
    global HEAD
    output = primes.PRIMES[HEAD:HEAD+amount]
    HEAD += amount
    return output

def unique() -> Prime:
    return uniques(1)[0]

def accumulate(begin: State,
               end: State,
               dst: Var,
               src: Var) -> list[Fraction]:
    """ [begin] (dst, src) -> [end] (dst + src, src) """
    E1, E2, E3 = uniques(3)
    x, y, z = dst, src, unique()
    A, B = begin, end

    return [
        (z * E1, y * A),
        (A, E1),
        (E2, A),
        (x * y * E3, z * E2),
        (E2, E3),
        (B, E2)
    ]

def accumulate_and_destroy(begin: State,
                           end: State,
                           dst: Var,
                           src: Var) -> list[Fraction]:
    """ [begin] (dst, src) -> [end] (dst + src, 0) """
    E = unique()
    return [
        (dst * E, src * begin),
        (begin, E),
        (end, begin)
    ]

def add(begin: State,
        end: State,
        dst: Var,
        x: Var,
        y: Var) -> list[Fraction]:
    """ [begin] (dst, x, y) -> [end] (x + y, x, y) """
    E1, E2, E3, E4, E5 = uniques(5)
    A, B = begin, end
    u, v = uniques(2)

    return [
        (E1, dst * A),
        (u * E1, x * A),
        (v * E1, y * A),
        (A, E1),
        (E2, A),
        (x * dst * E3, u * E2),
        (y * dst * E3, v * E2),
        (E2, E3),
        (B, E2)
    ]

def copy(begin: State,
         end: State,
         dst: Var,
         src: Var) -> list[Fraction]:
    """ [begin] (dst, src) -> [end] (src, src) """
    E1, E2, E3 = uniques(3)
    x, y, z = dst, src, unique()
    A, B = begin, end
    
    return [
        (E1, x * A),
        (z * E1, y * A),
        (A, E1),
        (E2, A),
        (x * y * E3, z * E2),
        (E2, E3),
        (B, E2)
    ]

def increment_times(begin: State,
                    end: State,
                    x: Var,
                    times: int) -> list[Fraction]:
    """ [begin] (x) -> [end] (x+times) """
    return [
        ((x**times) * end, begin)
    ]

def increment(begin: State, end: State, x: Var) -> list[Fraction]:
    """ [begin] (x) -> [end] (x+1) """
    return increment_times(begin, end, x, 1)

def decrement(begin: State, end: State, x: Var) -> list[Fraction]:
    """ [begin] (x) -> [end] (max(0, x-1)) """
    return [
        (end, x * begin),
        (end, begin)
    ]

def branch_then_decrement(begin: State,
                          end_true: State,
                          end_false: State,
                          x: Var) -> list[Fraction]:
    """ [begin] (x) -> [end_true] (x-1) if i > 0 and [end_false] (0) otherwise """
    return [
        (end_true, x * begin),
        (end_false, begin)
    ]

def branch(begin: State,
           end_true: State,
           end_false: State,
           x: Var) -> list[Fraction]:
    """ [begin] (x) -> [end_true] (x) if i > 0 and [end_false] (0) otherwise """
    E = unique()
    return [
        (E, x * begin),
        (end_false, begin),
        (x * end_true, E)
    ]

def branch_gt(begin: State,
              end_true: State,
              end_false: State,
              x: Var,
              y: Var) -> list[Fraction]:
    """ [begin] (x, y) -> [end_true] (x-y-1 , 0) if x > y and [end_false] (0, y-x) otherwise """
    E = unique()
    return [
        (E, x * y * begin),
        (begin, E),
        (end_true, x * begin),
        (end_false, begin)
    ]

def goto(begin: State, end: State) -> list[Fraction]:
    """ [begin] -> [end] / if the starting state is not [begin] then it will not go anywhere """
    return [
        (end, begin)
    ]

def clear(begin: State, end: State, x: Var) -> list[Fraction]:
    """ [begin] (x) -> [end] (0) """
    E = unique()
    return [
        (E, x * begin),
        (begin, E),
        (end, begin)
    ]

def destroy(x: Var) -> list[Fraction]:
    """ [?0] (x) -> [?0] (0) """
    return [ (1, x) ]

def euclidian_division(begin: State,
                       end: State,
                       n: Var,
                       d: Var,
                       o1: Var,
                       o2: Var) -> list[Fraction]:
    """ [begin] (n, d, o1, o2) -> [end] (n, d, q, r) """
    A, B = begin, end
    Z1, Z2, Z3, A0, A2, X1, X2, T1, T2 = uniques(9)
    n2, d2 = uniques(2)

    pre1 = copy(A, Z1, n2, n)
    pre2 = copy(Z1, Z2, d2, d)

    return pre1 + pre2 + [
        (Z3, o1 * Z2),
        (Z3, o2 * Z2),
        (Z2, Z3),
        (A0, Z2),

        (o2 * A2, n2 * d2 * A0),
        (A0, A2),
        (X1, d2 * A0),
        (o1 * T1, A0),
        (d2 * T2, o2 * T1),
        (T1, T2),
        (A0, T1),
        (X2, d2 * X1),
        (X1, X2),
        (B, X1)
    ] + destroy(n2) + destroy(d2)

def multiply(begin: State,
             end: State,
             x: Var,
             y: Var,
             o: Var) -> list[Fraction]:
    """ [begin] (x, y, o) -> [end] (x, y, xy) """
    Z1, Z2, Z3, A0, A2, T1, T2 = uniques(7)
    x2, y2, p = uniques(3)
    A, B = begin, end

    pre1 = copy(A, Z1, x2, x)
    pre2 = copy(Z1, Z2, y2, y)

    return pre1 + pre2 + [
        (Z3, o * Z2),
        (Z2, Z3),
        (A0, Z2),
        (y2 * A2, p * A0),
        (T1, x2 * A0),
        (A2, y2 * A0),
        (A0, A2),
        (o * p * T2, y2 * T1),
        (T1, T2),
        (A0, T1),
        (B, A0)
    ] + destroy(x2) + destroy(y2) + destroy(p)

def multiply_on(begin: State,
                end: State,
                dst: Var,
                src: Var) -> list[Fraction]:
    """ [begin] (dst, src) -> [end] (dst * src, src) """

    A, B, E = begin, end, unique()
    temp = unique()

    automata = [
        multiply(A, E, dst, src, temp),
        copy(E, B, dst, temp),
        destroy(temp)
    ]

    return [ f for fs in automata for f in fs ]

def automata_sum(begin: State,
                 end: State,
                 i: Var,
                 o: Var) -> list[Fraction]:
    """ [begin] (i, o) -> [end] (0, 1 + 2 + ... + i) """
    E0, E1, E2, E3 = uniques(4)
    A, B = begin, end

    automata = [
        clear(A, E0, o),
        goto(E0, E1),
        branch(E1, E2, B, i),
        accumulate(E2, E3, o, i),
        branch_then_decrement(E3, E1, B, i)
    ]

    return [ f for fs in automata for f in fs ]

def automata_fibonacci(begin: State,
                       end: State,
                       n: Var,
                       o: Var) -> list[Fraction]:
    """ [begin] (n, o) -> [end] (0, fib(n)) """
    E = uniques(6)
    A, B = begin, end
    a, c = uniques(2)
    b = o

    automata = [
        clear(A, E[0], b),
        increment(E[0], E[1], b),
        branch_then_decrement(E[1], E[2], B, n),
        add(E[2], E[3], c, a, b),
        copy(E[3], E[4], a, b),
        copy(E[4], E[5], b, c),
        goto(E[5], E[1]),
        destroy(a),
        destroy(c)
    ]

    return [ f for fs in automata for f in fs ]

def automata_collatz(begin: State,
                     end: State,
                     n: Var,
                     o: Var) -> list[Fraction]:
    """ [begin] (n, o) -> [end] (0, collatz(n)) """
    # Preuve de terminaison du programme associé laissée au lecteur

    two, three, q, r = uniques(4)
    A, B = begin, end
    E = uniques(11)
    i = o

    automata = [
        clear(A, E[0], i),
        increment_times(E[0], E[1], two, 2),
        increment_times(E[1], E[2], three, 3),
        branch_then_decrement(E[2], E[3], B, n),
        branch(E[3], E[4], B, n),
        increment(E[4], E[5], n),
        increment(E[5], E[6], i),
        euclidian_division(E[6], E[7], n, two, q, r),
        branch_then_decrement(E[7], E[8], E[10], r),
        multiply_on(E[8], E[9], n, three),
        increment(E[9], E[2], n),
        copy(E[10], E[2], n, q),
        destroy(two),
        destroy(three),
        destroy(q),
        destroy(r)
    ]

    return [ f for fs in automata for f in fs ]

def automata_sqrt(begin: State,
                  end: State,
                  n: Var,
                  o: Var) -> list[Fraction]:
    """ [begin] (n, o) -> [end] (n, floor(sqrt(n))) """
    A, B = begin, end
    E = uniques(8)
    res = o
    t, m = uniques(2)

    automata = [
        clear(A, E[0], res),
        increment(E[0], E[1], res),
        copy(E[1], E[2], t, res),
        copy(E[2], E[3], m, n),
        multiply_on(E[3], E[4], t, t),
        decrement(E[4], E[5], t),
        branch_gt(E[5], E[6], E[7], m, t),
        increment(E[6], E[1], res),
        decrement(E[7], B, res),
        destroy(t),
        destroy(m)
    ]

    return [ f for fs in automata for f in fs ]

def automata_factorial(begin: State,
                       end: State,
                       n: Var) -> list[Fraction]:
    """ [begin] (n) = [end] (n!) """
    A, B = begin, end
    E1, E2, E3, E4 = uniques(4)
    m = unique()

    automata = [
        copy(A, E1, m, n),
        decrement(E1, E2, m),
        branch(E2, E3, B, m),
        multiply_on(E3, E4, n, m),
        decrement(E4, E2, m),
        destroy(m)
    ]

    return [ f for fs in automata for f in fs ]

def make_sum():
    i, o, A, B = uniques(4)
    return automata_sum(A, B, i, o) + destroy(B)

def make_fibonacci():
    n, o, A, B = uniques(4)
    return automata_fibonacci(A, B, n, o) + destroy(B)

def make_collatz():
    n, o, A, B = uniques(4)
    return automata_collatz(A, B, n, o) + destroy(B)

def make_sqrt():
    n, o, A, B = uniques(4)
    return automata_sqrt(A, B, n, o) + destroy(B)

def make_factorial():
    n, A, B = uniques(3)
    return automata_factorial(A, B, n) + destroy(B)

if __name__ == "__main__":
    """
    How to run this program:

    1) change the behaviour of the code below according to you
       (what program do you want as your output?)
    2) run "./circuits.py <output_filename>"
    """

    if len(sys.argv) == 2:
        outfile = sys.argv[1]
        program = make_factorial()

        with open(outfile, "w", encoding="utf-8") as file:
            for num, den in program:
                file.write(f"{num} / {den}\n")
    else:
        print("Retry with a filename as argument (= the output). This file will be overwritten!")
