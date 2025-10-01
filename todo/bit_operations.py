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



def get_binary_digits(val, bit_len=''):
    bits = [int(n) for n in str(bin(val))[2:]]
    if bit_len and len(bits) != bit_len:



def XOR(bit_value_1, bit_value_2):
    """
    Perform simple XOR ^ operation on two binary values (0 or 1).
    """
    # assert (bit_value_1 in (0,1) and bit_value_2 in (0,1)), "Bit values must be either 0 or 1"
    bin_1 = [int(n) for n in str(bin(bit_value_1))[2:]]
    bin_2 = [int(n) for n in str(bin(bit_value_2))[2:]]

    x = len(bin_1)
    y = len(bin_2)
    if x != y:
        n = max(x,y)
        missing_digits = abs(x-y)
        for i in range(missing_digits):
            # if bin_1 has the most digits, update bin_2 with 0s
            if x == n:
                bin_2.insert(0)
            elif y == n:
                bin_1.insert(0)




bit_value_1 = 256
bit_value_2 = 285

bin_1 = [int(n) for n in str(bin(bit_value_1))[2:]]
bin_2 = [int(n) for n in str(bin(bit_value_2))[2:]]

print(bin_1)
print(bin_2)

x, y = len(bin_1), len(bin_2)


xor_vals = []
for i in range(x):
    a = bin_1[i]
    b = bin_2[i]
    xor_vals.append(XOR(a, b))

b = "".join([str(n) for n in xor_vals])

print(int(b,2))