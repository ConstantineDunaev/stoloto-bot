from itertools import combinations


def generate_combination(length: int) -> list[tuple]:
    values = [i for i in range(1, 21)]
    return [
        (length, index, item)
        for index, combiantion in enumerate(combinations(values, length))
        for item in combiantion
    ]
