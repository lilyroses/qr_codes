import json

fx = {}

with open("character_capacities.json", "r") as f:
  cc = json.load(f)
  for v, info in cc.items():
    fx[v] = {}

    for ec_lvl, mode in info.items():
      fx[v][ec_lvl] = {}

      for m, val in mode.items():
        if m == "NUM":
          m = "NUMERIC"
        elif m == "ALPHANUM":
          m = "ALPHANUMERIC"
        fx[v][ec_lvl][m] = val


for k, v in fx.items():
  print(f"{k}:")
  for x, y in v.items():
    print(f"\t{x}:")
    for m, n in y.items():
      print(f"\t\t{m}: {n}")


with open("character_capacities.json", "w") as f:
  json.dump(fx, f)
