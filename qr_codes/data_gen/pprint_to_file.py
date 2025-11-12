import io
from pprint import pprint


def pprint_to_file(data, var_name, OUTPUT_FILE:str, write_method="w"):
    output = io.StringIO()
    p = pprint(data, width=80, indent=4, sort_dicts=False, stream=output)
    fp = output.getvalue()

    with open(OUTPUT_FILE, write_method) as f:
        s = f"{var_name} = {fp}"
        f.write(s)
        print("Success")
        return
