# data.py
import json

# QR CODE VERSION NUMBERS
# Version number determines QR matrix size in pixel height/width.
# 	VERSION_NUMBER_SIZES_MAP.keys(): version numbers
#   	VERSION_NUMBER_SIZES_MAP.values(): a single integer that represents both
#           the height and width of the matrix, in pixels.
VERSION_NUMBERS = range(1,41)
VERSION_SIZES = range(21, 21+(4*len(VERSION_NUMBERS)), 4)
VERSION_NUMBER_SIZES = dict(zip(VERSION_NUMBERS, VERSION_SIZES))

# ERROR CORRECTION LEVELS
ERROR_CORRECTION_LEVELS = list("LMQH")
ERROR_CORRECTION_PERCENTS = [7, 15, 25, 30]
ERROR_CORRECTION_LEVEL_PERCENTS = dict(zip(
    ERROR_CORRECTION_LEVELS, ERROR_CORRECTION_PERCENTS))

# MODES (ENCODING SCHEMES)
#	Charsets for NUMERIC and ALPHANUMERIC encodings.
NUMERIC_CHARSET = tuple("0123456789")
ALPHANUMERIC_CHARSET = ("0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," ","$","%","*","+","-",".","/",":")
ALPHANUMERIC_CHARSET_VALUES = dict(zip(ALPHANUMERIC_CHARSET, range(len(ALPHANUMERIC_CHARSET))))
# 	Mode names and indicator bits
MODE_NAMES = "NUMERIC ALPHANUMERIC BYTE KANJI ECI".split()
MODE_INDICATOR_BITS = ["0001", "0010", "0100", "1000", "0111"]
MODE_NAME_INDICATOR_BITS = dict(zip(MODE_NAMES, MODE_INDICATOR_BITS))

# CHARACTER CAPACITIES
with open("character_capacities.json", "r") as f:
    CHARACTER_CAPACITIES = json.load(f)

# CHARACTER COUNT INDICATOR LENGTHS
with open("character_count_indicators.json", "r") as f:
    CHARACTER_COUNT_INDICATORS = json.load(f)
