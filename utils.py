# utils.py
import json
from string import digits


# QR CODE VERSION NUMBERS
#   QR code version numbers directly relate to the QR code's matrix size, in
#   pixel height and width.
#      VERSION_NUMBER_SIZES.keys(): version numbers
#      VERSION_NUMBER_SIZES.values(): pixel height AND width for QR matrix
#   E.g., VERSION_NUMBER_SIZES[1] = 21 indicates that the matrix for a version
#   1 QR code is 21 x 21 pixels.
#   QR code versions are 1-40. Matrix size starts at 21 for version 1 and 
#   increments by 4 for each successive version, capping at 177 pixels for
#   version 40.
VERSION_NUMBERS = range(1,41)
VERSION_SIZES = range(21, 21+(4*len(VERSION_NUMBERS)), 4)
VERSION_NUMBER_SIZES = dict(zip(VERSION_NUMBERS, VERSION_SIZES))


# ERROR CORRECTION LEVELS
#   There are four error correction levels: L, M, Q, and H. Each has its own
#   number of error code words as well as specific bit strings that must be
#   encoded within the matrix.
ERROR_CORRECTION_LEVELS = list("LMQH")
ERROR_CORRECTION_PERCENTS = [7, 15, 25, 30]
ERROR_CORRECTION_LEVEL_PERCENTS = dict(zip(
    ERROR_CORRECTION_LEVELS, ERROR_CORRECTION_PERCENTS))

# MODE NAMES
MODE_NAMES = "NUM ALPHANUM BYTE KANJI ECI".split()
MODE_INDICATOR_BITS = ["0001", "0010", "0100", "1000", "0111"]
MODE_NAME_INDICATOR_BITS = dict(zip(MODE_NAMES, MODE_INDICATOR_BITS))


# ENCODING SCHEMES
#   This is only for NUMERIC and ALPHANUMERIC encodings. Anything message that
#   cannot be encoded with either NUMERIC or ALPHANUMERIC encoding will be encoded
#   with BYTE mode encoding.
NUM = tuple(digits)
ALPHANUM = ("0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," ","$","%","*","+","-",".","/",":")
ALPHANUM_MAP = dict(zip(ALPHANUM, range(len(ALPHANUM))))
