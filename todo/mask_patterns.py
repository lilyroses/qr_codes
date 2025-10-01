# mask_patterns.py
"""QR code readabilty can be improved by using one of eight mask patterns.
Each mask pattern uses a specific formula (detailed below) which is applied to
each bit in the QR matrix. The formula produces a value of 1 or 0 using each
bit's coordinates and current value. If the value produced by the formula is
0, the opposite bit is used at that coordinate. E.g., if the bit for
coordinate (0,0) is a 1, and the formula equals to 0 for that coordinate, the
bit at (0,0) is now a 0 instead.

bit_coordinate = (x,y) (column, row)
"""
from bit_operations import switch_bit


# MASK 0
def mask_0(bit_coordinate:tuple[int]):
    column, row = bit_coordinate
    if (row + column) % 2 == 0:
        switch_bit(bit_coordinate)


# MASK 1
def mask_1(bit_coordinate:tuple[int]):
    row = bit_coordinate[1]
    if row % 2 == 0:
        switch_bit(bit_coordinate)


# MASK 2
def mask_2(bit_coordinate:tuple[int]):
    column = bit_coordinate[0]
    if column % 3 == 0:
        switch_bit(bit_coordinate)


# MASK 3
def mask_3(bit_coordinate:tuple[int]):
    column, row = bit_coordinate
    if (row + column) % 3 == 0:
        switch_bit(bit_coordinate)


# MASK 4
def mask_4(bit_coordinate:tuple[int]):
    column, row = bit_coordinate
    if ((row // 2) + (column // 3)) % 2 == 0:
        switch_bit(bit_coordinate)


# MASK 5
def mask_5(bit_coordinate:tuple[int]):
    column, row = bit_coordinate
    if ((row * column) % 2) + ((row * column) % 3) == 0:
        switch_bit(bit_coordinate)


# MASK 6
def mask_6(bit_coordinate:tuple[int]):
    column, row = bit_coordinate
    if (((row * column) % 2) + ((row * column) % 3)) % 2 == 0:
        switch_bit(bit_coordinate)


# MASK 7
def mask_4(bit_coordinate:tuple[int]):
    column, row = bit_coordinate
    if (((row + column) % 2) + ((row * column) % 3)) % 2 == 0:
        switch_bit(bit_coordinate)
