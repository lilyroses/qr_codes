 # mask_patterns.py
"""QR code readabilty can be improved by using one of eight mask patterns.
Each mask pattern uses a specific formula (detailed below) which is applied to
each bit in the QR matrix. The formula uses each bit's coordinates and current
value and returns a 1 or 0. If the value produced by the formula is 0, the
opposite bit is used at that coordinate. If the value produced by the formula is
1, the bit's value is left as is.

EX: if we use a mask pattern formula on a bit with a value of 1, and the formula
produces a 0, the bit's value is now a 1. If the formula had produced a 1, the
bit's value would have been left as is.
"""
from bit_operations import switch_bit


# MASK 0
def mask_0(bit_coordinate:tuple[int]):
    column, row = bit_coordinate
    return (row + column) % 2 == 0
        # switch_bit(bit_coordinate)


# MASK 1
def mask_1(bit_coordinate:tuple[int]):
    row = bit_coordinate[1]
    return row % 2 == 0
        # switch_bit(bit_coordinate)


# MASK 2
def mask_2(bit_coordinate:tuple[int]):
    column = bit_coordinate[0]
    return column % 3 == 0
        # switch_bit(bit_coordinate)


# MASK 3
def mask_3(bit_coordinate:tuple[int]):
    column, row = bit_coordinate
    return (row + column) % 3 == 0
        # switch_bit(bit_coordinate)


# MASK 4
def mask_4(bit_coordinate:tuple[int]):
    column, row = bit_coordinate
    return ((row // 2) + (column // 3)) % 2 == 0
        # switch_bit(bit_coordinate)


# MASK 5
def mask_5(bit_coordinate:tuple[int]):
    column, row = bit_coordinate
    return ((row * column) % 2) + ((row * column) % 3) == 0
        # switch_bit(bit_coordinate)


# MASK 6
def mask_6(bit_coordinate:tuple[int]):
    column, row = bit_coordinate
    return (((row * column) % 2) + ((row * column) % 3)) % 2 == 0
        # switch_bit(bit_coordinate)


# MASK 7
def mask_7(bit_coordinate:tuple[int]):
    column, row = bit_coordinate
    return (((row + column) % 2) + ((row * column) % 3)) % 2 == 0
        # switch_bit(bit_coordinate)
