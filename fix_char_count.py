# fix
import json

with open("character_count_indicators.json", "r") as f:
  d = json.load(f)

fx = {}
for v, m in d.items():
  fx[v] = {}
  for mode, val in m.items():
    if mode == "NUM":
      mode = "NUMERIC"
    elif mode == "ALPHANUM":
      mode = "ALPHANUMERIC"
    fx[v][mode] = val

with open("character_count_indicators.json", "w") as f:
  json.dump(fx, f)
