import os


TERMINAL_WIDTH = os.get_terminal_size()[0]
CORNER = "+"
PIPE = "|"
DASH = "-"
SPACE = " "


def create_ascii_table(row_data:list) -> str:
  """Create an ascii table given a list of lists of cell entries.
  E.g.:

  row_data = [
    ["name", "number", "dob"],
    ["Lily", 42, "11-09-1994"],
    ["Sebastian", 100, "02-18-1985"],
    ["Gabriel", 99, "12-12-1965"]
  ]


  Table produced:

  +-----------+--------+------------+
  |    NAME   | NUMBER |    DOB     |
  +-----------+--------+------------+
  |    Lily   |   42   | 11-09-1994 |
  +-----------+--------+------------+
  | Sebastian |  100   | 02-18-1985 |
  +-----------+--------+------------+
  |  Gabriel  |   99   | 12-12-1965 |
  +-----------+--------+------------+

  """

  cols = len(row_data[0])
  rows = len(row_data)

  # Ensure at least 2 rows
  if rows < 2:
    return "Error: Not enough rows to create ASCII table (must have 2 or more rows)."

  # Ensure data columns do not exceed number of header colums.
  for row in row_data[1:]:
    if len(row) > cols:
      return "Error: Columns per row cannot exceed number of table headers."

  # Format row data so that each cell contains only strings.
  row_data = [[str(e) for e in row] for row in row_data]

  # Capitalize the header columns.
  headers = [entry.upper() for entry in row_data[0]]
  row_data = [headers] + row_data[1:]

  # Add empty cells where needed so all rows have equal number of cols.
  for row in row_data:
    missing_cols = cols - len(row)
    for i in range(missing_cols):
      row.append("")  # placeholder for empty cell

  # For each col, find longest entry length. Add 2 for space padding.
  col_widths = [0 for i in range(cols)]  # max col widths
  for row in row_data:
    for i, entry in enumerate(row):
      n = len(entry) + 2  # add 2 for space char padding on either side
      col_widths[i] = max(col_widths[i], n)

  # Ensure each row fits in table (later may implement functionality to split
  # one col across multiple lines).
  total_row_len = sum(col_widths) + (cols+1)  # account for pipe chars
  if total_row_len > TERMINAL_WIDTH:
    return f"Error: Terminal size too small to render table."

  # Create horizontal border string.
  horiz_border = CORNER + CORNER.join([DASH*w for w in col_widths]) + CORNER

  # Create row strings.
  row_strs = []
  for row in row_data:
    row_strs.append("".join([PIPE + row[i].center(col_widths[i], SPACE)
                             for i in range(cols)]) + PIPE)

  # Bring it all together
  table = ""
  for row_str in row_strs:
    table += f"{horiz_border}\n{row_str}\n"
  table += horiz_border

  return f"\n\n{table}\n\n"
  return table



if __name__ == "__main__":


  row_data = [
  ["ec lvl", "% dmg", "etc"],
  ["L", 7],
  ["M",'15','16 17'],
  ["Q",25],
  ["H",30]
]
  print(create_ascii_table(row_data))


  row_data = [
     ["name", "number", "dob"],
     ["lily", 42, "11-09-1994"],
     ["sebastian", 100, "02-18-1985"],
     ["gabriel", 99, "12-12-1965"]
   ]
  print(create_ascii_table(row_data))


  row_data = [
  ["ec lvl", "% dmg"],
  ["L", 7],
  ["M", 15],
  ["Q", 25],
  ["H", 30]
]
  print(create_ascii_table(row_data))


  row1 = ["1", "Q", "5", "18", "2", "19", "0", "0"]
  row2 = row1[::-1]
  row3 = row1[:len(row1)//2][::-1] + row1[len(row1)//2:]
  row4 = row3[::-1]
  rows = [row1, row2, row3, row4]
  print(create_ascii_table(rows))
