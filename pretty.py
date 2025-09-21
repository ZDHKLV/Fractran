import primes
from collections import Counter

def pretty_prime_factors_to_int(s: str) -> int:
    s = s.replace(" ", "")
    output = 1
    for factor in s.split("*"):
        if '^' in factor:
            a, b = map(int, factor.split("^"))
        else:
            a, b = int(factor), 1
        output *= a**b
    return output

def int_to_pretty_prime_factors(n: int) -> str:
    factors = primes.prime_factors(n)
    counter = Counter(factors)
    return " * ".join(map(
        lambda item : f"{item[0]}" if item[1] == 1 else f"{item[0]}^{item[1]}",
        counter.items()
    ))

def int_to_pretty_registers(n: int,
                            names: dict[int, str] = {},
                            show_states: bool = False) -> str:
    factors = primes.prime_factors(n)
    counter = Counter(factors)

    states = set()
    variables = set()

    for k, v in counter.items():
        if k in names and names[k][0].isupper() and v == 1 and show_states:
            states.add(names[k])
        elif k in names:
            variables.add((names[k], v))
        else:
            variables.add((f"x{k}", v))

    if len(states) == 0 and show_states:
        unnamed_states = []
        for k, v in counter.items():
            if v == 1 and k not in names:
                unnamed_states.append(f"E{k}")

        if len(unnamed_states) == 1:
            states.add(unnamed_states[0])
            variables.remove((f"x{unnamed_states[0][1:]}", 1))
        else:
            states.add("?")

    states_desc = "[" + ", ".join(states) + "]"
    vars_desc = "{{" + ", ".join(map(
        lambda item : f"{item[0]} = {item[1]}",
        variables
    )) + "}}"

    return f"{states_desc} {vars_desc}" if show_states else vars_desc