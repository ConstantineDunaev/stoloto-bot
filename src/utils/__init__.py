def mask_from_values(values: list[int]) -> int:
    mask = 0
    for value in values:
        mask |= 1 << (value - 1)
    return mask
