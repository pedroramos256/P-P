import numpy as np

lines = open('../example_scenario.txt').readlines()

def process_scenario(lines):
    ix = 0
    while lines[ix][0] == "#":
        ix += 1
    A = int(lines[ix])
    str_out = f"A={A};\nstart=["
    for l in lines[ix+2:A+2]:
        i = int(l[0])
        j = int(l[2])
        str_out += f"{j}"
        if i < A:
            str_out += ","
    str_out += "];\n"
    str_out += "end=["
    for l in lines[A+3:]:
        i = int(l[0])
        j = int(l[2])
        str_out += f"{j}"
        if i < A:
            str_out += ","

    str_out += "];\n"
    print(str_out)

process_scenario(lines)