t = 2
m = 285
x = 256

powers = []

log_table = {}
antilog_table = {}


for i in range(x):
  if i == 0:
    val = t**i
  else:
    val = powers[-1] * 2
    if val >= x:
      val = val ^ m
  powers.append(val)
  log_table[i] = val

  if val not in antilog_table:
    antilog_table[val] = i

with open("log_table.py", "w") as f:
  f.write(f"""log_table = {log_table}""")

with open("antilog_table.py", "w") as f:
  f.write(f"""antilog_table = {antilog_table}""")

