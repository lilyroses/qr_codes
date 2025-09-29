+-----------+-----------+----------+-------+-----------+
| version # | size      | EC level | mode  | max chars |
+-----------+-----------+----------+-------+-----------+
| 1         | 21 x 21   | L        | NUM   | 7089      |
|           |           |          | ALPHA | 4296      |
|           |           |          | BYTE  | 2953      |
|           |           |          | KANJI | 1817      |
+-----------+-----------+----------+-------+-----------+
| 2         | 25 x 25   |          |       |           |
| ... (+1)  | ... (+4)  |          |       |           |
| 40        | 177 x 177 |          |       |           |
+-----------+-----------+----------+-------+-----------+


+----------+---------------+
| EC level | EC capability |
+----------+---------------+
| L        |  7% recovery  |
| M        | 15% recovery  |
| Q        | 25% recovery  |
| H        | 30% recovery  |
+----------+---------------+

+----------+-----------+
| MODE     | BIT       |
|          | INDICATOR |
+----------+-----------+
| NUM      | 0001      |
| ALPHANUM | 0010      |
| BYTE     | 0100      |
| KANJI    | 1000      |
| ECI      | 0111      |
+----------+-----------+

---

## STEPS TO CREATING QR CODE

1. DATA ANALYSIS
    - figure out how to encode message w/ shortest amount of bits
    - NUMERIC? (0-9)
    - ALPHANUMERIC? (0-9 and UPPERCASE letters plus a few symbols)
    - BYTE (for everything else)
    - `encoding_scheme = get_encoding_scheme(msg)`

2. DATA ENCODING
    - ENCODE MESSAGE USING 
    - STRING OF BITS SPLIT UP INTO **8-BIT LONG DATA CODEWORDS**

`encoded_msg = encode_msg(msg, encoding_scheme)`

`def encode_msg(msg, encoding_scheme):`
    `


3. 