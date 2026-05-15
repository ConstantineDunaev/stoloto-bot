from itertools import combinations


def generate_combination(length: int) -> list[tuple]:
    values = [i for i in range(1, 21)]
    return [
        (combination_id, length, value)
        for combination_id, combiantion in enumerate(combinations(values, length), start=1)
        for value in combiantion
    ]
