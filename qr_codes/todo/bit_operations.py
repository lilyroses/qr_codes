# bit_operations.py

# TODO!
# decide if bit_coordinate tuple is (row,col) or (col,row) - go by x,y
# graph type coordinate (col,row) or array indexing (row,col)?
# find out how the bits are indexed when using masking operations

def get_bit(bit_coordinate:tuple[int]):
    """
    Determine bit value within QR matrix. 0 indicates a white pixel, 
    while a 1 indicates a black pixel. 
    """
    assert len(bit_coordinate) == 2, "bit_coordinate should be 2 values."
    column, row = bit_coordinate
    bit_value = matrix[column][row]
    return bit_value


def update_bit(bit_value: int, bit_coordinate:tuple[int]):
    column, row = bit_coordinate
    matrix[column][row] = bit_value



def switch_bit(bit_coordinate:tuple[int]):
    """
    Change the bit at the bit_coordinate location within the QR matrix
    to the opposite value. E.g. if the bit_value is 1, change it to 0.
    Used when applying bitmask operations.
    """
    bit_value = get_bit(bit_coordinate)
    new_bit_value = int(not bit_value)
    update_bit(new_bit_value, bit_coordinate)


def XOR(val1, val2):
    """
    Perform simple XOR ^ operation on two binary values (0 or 1).
    """
    # assert (bit_value_1 in (0,1) and bit_value_2 in (0,1)), "Bit values must be either 0 or 1"

    bin_1 = bin(val1)[2:]
    bin_2 = bin(val2)[2:]

    x = len(bin_1)
    y = len(bin_2)

    if x != y:
        n = max(x,y)
        pad_zeroes = "0" * abs(x-y)
        if x == n:
            bin_2 = pad_zeroes + bin_2
        elif y == n:
            bin_1 = pad_zeroes + bin_1

    bits_1 = [int(b) for b in bin_1]
