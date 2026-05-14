from itertools import combinations
from json import dumps


def generate_combination(length: int) -> list[tuple]:
    values = [str(i).rjust(2, "0") for i in range(1, 21)]
    return [(dumps(item), length) for item in combinations(values, length)]
